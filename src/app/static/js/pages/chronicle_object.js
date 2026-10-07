import { ModifyMarkdownModal } from "../modals/markdown_editor.js";

const socket = io();
const container = document.getElementById("page-config");
const resourceType = container.dataset.resourceType;
const objectId = container.dataset.objectId;

socket.emit("request_chronicle_object", {
  type: resourceType,
  id: objectId,
});

const modal = new ModifyMarkdownModal(socket, resourceType, objectId);
document.getElementById("chronicle-object-edit-btn").addEventListener("click", () => {
  modal.open();
});

socket.on("updated_chronicle_object", (object) => {
  if (object.id === objectId && object.type == resourceType) {
    document.getElementById("chronicle-object-container").dataset.loaded = "true";
    document.getElementById("chronicle-object-text-container").innerHTML = object.markdown_rendered;
    modal.setContent(object.markdown_raw);
  }
});
