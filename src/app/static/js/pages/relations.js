import { RelationshipGraph } from "../graphs/relationship_graph.js";

const socket = io();
const graph = new RelationshipGraph("relationship-graph");

document.addEventListener("DOMContentLoaded", () => {
  socket.emit("request_relations_data");
});

socket.on("updated_relations", (data) => {
  graph.setData(data.nodes, data.edges);
});
