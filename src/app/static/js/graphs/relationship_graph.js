export class RelationshipGraph {
  constructor(containerId) {
    this.cy = cytoscape({
      container: document.getElementById(containerId),

      elements: [],

      style: [
        {
          selector: "node",
          style: {
            label: "data(label)",
            "background-color": "#6a707a",
            color: COLORS.text,
            "text-valign": "bottom",
            "font-size": 8,
          },
        },
        {
          selector: "node[type='person']",
          style: {
            "background-color": COLORS.person,
          },
        },
        {
          selector: "edge",
          style: {
            label: "data(relation)",
            "font-size": 8,
            "curve-style": "bezier",
            color: COLORS.text,
            "line-color": COLORS.border,
            "target-arrow-color": COLORS.border,
            "target-arrow-shape": "none",
          },
        },
      ],

      layout: {
        name: "cose",
      },
    });
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
