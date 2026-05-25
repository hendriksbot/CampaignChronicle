import { NewPersonModal } from "../modals/new_person.js";

const socket = io();
document.addEventListener("DOMContentLoaded", () => {
  socket.emit("request_people_list");
});

socket.on("updated_people_list", function (data) {
  renderPeople(data);
});

function renderPeople(data) {
  const grid = document.getElementById("people-container");
  grid.innerHTML = "";
  data.people.forEach((person) => {
    const card = createPersonCard(person);
    grid.appendChild(card);
  });
}

function createPersonCard(person) {
  const card = document.createElement("a");
  card.className = "person-card disabled";
  card.href = "/people";

  const name = document.createElement("h3");
  name.textContent = person.name;

  card.appendChild(name);

  return card;
}

const modal = new NewPersonModal(socket);
document.getElementById("new-person-btn").addEventListener("click", () => {
  modal.open();
});
