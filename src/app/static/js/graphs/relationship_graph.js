import { EventEmitter } from "../utils/event_emitter.js";

export class RelationshipGraph extends EventEmitter {
  constructor(containerId) {
    super();
    this.cy = cytoscape({
      container: document.getElementById(containerId),

      elements: [],

      style: [],

      layout: {
        name: "cose",
        nodeRepulsion: 10000,
        idealEdgeLength: 120,
        randomize: false,
        gravity: 0.25,
        fit: true,
        componentSpacing: 200,
      },
    });
    this.relationshipDefinitions = new Map();
    this.contextMenus = new Map();
    this.mode = "default";
    this.cy.on("tap", "node", this.#onNodeTap.bind(this));
    this.pendingRelation = {
      source: null,
    };
  }

  destroy() {
    this.#destroyContextMenus();
    this.cy.destroy();
  }

  setConfigurations(config) {
    this.relationshipDefinitions.clear();
    for (const def of config.relation_definitions) {
      this.relationshipDefinitions.set(def.type, def);
    }
    const styles = [
      // Default node style
      {
        selector: "node",
        style: {
          label: "data(label)",
          "background-color": "#6a707a",
          color: COLORS.text,
          "text-valign": "bottom",
          "font-size": 8,
          "text-wrap": "wrap",
          "text-max-width": 60,
        },
      },
      // Person node style
      {
        selector: "node[type='person']",
        style: {
          "background-color": COLORS.person,
        },
      },

      // Default edge style
      {
        selector: "edge",
        style: {
          label: "data(label)",
          "font-size": 8,
          "curve-style": "bezier",
          color: COLORS.text,
          "line-color": COLORS.border,
          "line-style": "solid",
        },
      },

      {
        selector: "node.relation-source",
        style: {
          "overlay-opacity": 0.3,
          "overlay-color": COLORS.hoverPrime,
          "overlay-padding": 10,
        },
      },
    ];

    for (const def of this.relationshipDefinitions.values()) {
      styles.push({
        selector: `edge[type='${def.type}']`,
        style: {
          "line-color": def.style?.["line-color"] || COLORS.border,
          "line-style": def.style?.["line-style"] || "solid",
          "source-arrow-shape": def.style?.["source-arrow-shape"] || "none",
          "target-arrow-shape": def.style?.["target-arrow-shape"] || "none",
          "target-arrow-color": def.style?.["line-color"] || COLORS.border,
          "source-arrow-color": def.style?.["line-color"] || COLORS.border,
        },
      });
    }

    this.cy.style().resetToDefault();
    this.cy.style(styles);
    console.log("[Graph] Configuration loaded:", config);
    this.#bindInteractions();
  }

  #createContextMenu(key, options) {
    this.contextMenus.get(key)?.destroy();

    const menu = new RelationContextMenu(this.cy, options);

    this.contextMenus.set(key, menu);
  }

  #destroyContextMenus() {
    for (const menu of this.contextMenus.values()) {
      menu.destroy();
    }

    this.contextMenus.clear();
  }

  #createContextMenus() {
    const options = {
      selector: "node",
      commands: [
        {
          content: "✏ Edit",
          select: (node) => {
            console.log("clicked edit");
          },
        },
        {
          content: "➕ Add Relationship",
          select: (node) => {
            this.#startRelationSelection(node);
            console.log("clicked add relationsship");
          },
        },
      ],
    };
    this.#createContextMenu("node", options);
  }

  #onNodeTap(event) {
    switch (this.mode) {
      case "default":
        this.#handleDefaultNodeTap(event.target);
        break;

      case "create-relation":
        this.#finishRelationSelection(event.target);
        break;

      default:
        break;
    }
  }

  #switchInteractionMode(mode) {
    const graphBanner = document.getElementById("graph-mode-banner");
    switch (mode) {
      case "create-relation":
        this.mode = mode;
        this.#destroyContextMenus();
        graphBanner.classList.remove("hidden");
        break;
      default:
        this.mode = "default";
        this.#bindInteractions();
        graphBanner.classList.add("hidden");
        break;
    }
    requestAnimationFrame(() => {
      this.cy.resize();
      this.cy.fit();
    });
    console.log("[graph] mode: " + mode);
  }

  #bindCreateRelationInteractions() {
    this.cy.on("tap", "node", (event) => {
      const targetNode = event.target;
      this.#finishRelationSelection(targetNode);
    });
  }

  #handleDefaultNodeTap() {
    this.cy.on("tap", "node", function () {
      try {
        // your browser may block popups
        window.open(this.data("href"));
      } catch (e) {
        // fall back on url change
        window.location.href = this.data("href");
      }
    });
  }

  #bindInteractions() {
    this.#createContextMenus();
  }

  setData(nodes, edges) {
    this.cy.elements().remove();

    this.cy.add(nodes);
    this.cy.add(edges);

    console.log("nodes", nodes);
    console.log("edges", edges);
    console.log("container size", document.getElementById("relationship-graph").offsetHeight);

    this.cy
      .layout({
        name: "cose",
        animate: true,
      })
      .run();
  }

  #startRelationSelection(sourceNode) {
    this.#switchInteractionMode("create-relation");

    this.pendingRelation = {
      source: sourceNode,
    };
    sourceNode.addClass("relation-source");

    console.log("Select target node");
  }

  #finishRelationSelection(targetNode) {
    const sourceNode = this.pendingRelation.source;
    sourceNode.removeClass("relation-source");

    this.#switchInteractionMode("default");
    this.pendingRelation.source = null;

    if (sourceNode.id() === targetNode.id()) {
      return;
    }

    console.log(sourceNode);
    console.log(targetNode);
    this.emit("createRelation", {
      source: {
        id: sourceNode.data("id"),
        label: sourceNode.data("label"),
      },
      target: {
        id: targetNode.data("id"),
        label: targetNode.data("label"),
      },
    });
  }
}

const styles = getComputedStyle(document.documentElement);

const COLORS = {
  text: styles.getPropertyValue("--text-color").trim(),
  border: styles.getPropertyValue("--border-color").trim(),
  person: styles.getPropertyValue("--node-person-color").trim(),
  hoverPrime: styles.getPropertyValue("--btn-primary-hover-color").trim(),
};

class RelationContextMenu {
  constructor(cy, options) {
    this.cy = cy;
    this.menu = this.cy.cxtmenu({
      outsideMenuCancel: 1, // number cancels, true doesn't
      ...options,
    });
  }

  destroy() {
    this.menu.destroy();
  }
}
