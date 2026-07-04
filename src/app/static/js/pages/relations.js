import { RelationshipGraph } from "../graphs/relationship_graph.js";

const socket = io();
const graph = new RelationshipGraph("relationship-graph");

document.addEventListener("DOMContentLoaded", () => {
  socket.emit("request_init_relations_data");
});

socket.on("initialized_relations", (data) => {
  graph.setConfigurations(data.config);
  graph.setData(data.nodes, data.edges);
});

socket.on("updated_relations", (data) => {
  graph.setData(data.nodes, data.edges);
});
