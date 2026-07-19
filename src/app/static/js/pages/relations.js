import { RelationshipGraph } from "../graphs/relationship_graph.js";
import { NewRelationModal } from "../modals/new_relation.js";

const socket = io();
const graph = new RelationshipGraph("relationship-graph");
const relationModal = new NewRelationModal(socket);

graph.on("createRelation", ({ source, target }) => {
  relationModal.open(source, target, graph.relationshipDefinitions);
});

graph.on("deleteRelation", (data) => {
  socket.emit("request_delete_relation", data);
});

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
