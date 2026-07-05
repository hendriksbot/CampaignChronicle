export class RelationshipGraph {
  constructor(containerId) {
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
          "text-overflow-wrap": "ellipsis",
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

    const menu = new RelationContextMenu(this.cy);

    this.contextMenus.set(key, menu);
  }

  #destroyContextMenus() {
    for (const menu of this.contextMenus.values()) {
      menu.destroy();
    }

    this.contextMenus.clear();
  }

  #bindInteractions() {
    this.cy.on("tap", "node", function () {
      try {
        // your browser may block popups
        window.open(this.data("href"));
      } catch (e) {
        // fall back on url change
        window.location.href = this.data("href");
      }
    });
    this.cxtmenu = new RelationContextMenu(this.cy);
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
}

const styles = getComputedStyle(document.documentElement);

const COLORS = {
  text: styles.getPropertyValue("--text-color").trim(),
  border: styles.getPropertyValue("--border-color").trim(),
  person: styles.getPropertyValue("--node-person-color").trim(),
};

class RelationContextMenu {
  constructor(cy) {
    this.cy = cy;
    this.menu = this.cy.cxtmenu({
      outsideMenuCancel: 1, // number cancels, true doesn't
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
            console.log("clicked add relationsship");
          },
        },
      ],
    });
  }

  destroy() {
    this.menu.destroy();
  }
}
