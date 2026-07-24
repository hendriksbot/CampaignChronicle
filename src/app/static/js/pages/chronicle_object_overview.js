import { NewChronicleObjectModal } from "../modals/new_chronicle_object.js";
const socket = io();
const container = document.getElementById("page-config");
const resourceType = container.dataset.resourceType;

document.addEventListener("DOMContentLoaded", () => {
  socket.emit("request_object_overview_list", { type: resourceType });
});

socket.on("updated_people_list", function (data) {
  renderObjectList(data);
});

function renderObjectList(data) {
  const grid = document.getElementById("chronicle-object-overview-container");
  grid.innerHTML = "";
  data.objects.forEach((obj) => {
    const card = createObjectCard(obj);
    grid.appendChild(card);
  });
}

function createObjectCard(chrObj) {
  const card = document.createElement("a");
  card.className = "chronicle-object-card";
  card.href = "/" + recourceType + "/" + chrObj.id;

  const name = document.createElement("h1");
  name.textContent = chrObj.name;

  card.appendChild(name);

  return card;
}

const modal = new NewChronicleObjectModal(socket);
document.getElementById("new-chronicle-object-btn").addEventListener("click", () => {
  console.log("clicked card");
  modal.open();
});
