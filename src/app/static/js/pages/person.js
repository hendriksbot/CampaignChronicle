import { ModifyMarkdownModal } from "../modals/markdown_editor.js";

const socket = io();

socket.emit("request_person", {
  id: PERSON_ID,
});

const modal = new ModifyMarkdownModal(socket);
document.getElementById("person-edit-btn").addEventListener("click", () => {
  modal.open();
});

socket.on("updated_person", (person) => {
  if (person.id === PERSON_ID) {
    document.getElementById("person-container").dataset.loaded = "true";
    document.getElementById("person-text-container").innerHTML = person.markdown_rendered;
    modal.setContent(person.markdown_raw);
  }
});
