import { NewPersonModal } from "../modals/new_person.js";

const socket = io();
document.getElementById("set-path-btn").addEventListener("click", setPath);

function setPath() {
  const input = document.getElementById("campaign-path-input");

  socket.emit("request_set_campaign_folder");
}

document.addEventListener("DOMContentLoaded", () => {
  socket.emit("request_reload_index");
});

socket.on("campaign_set_status", function (data) {
  document.querySelectorAll(".nav-requires-campaign").forEach((el) => {
    el.classList.toggle("nav-disabled", !data.is_active);
  });

  document.querySelectorAll(".requires-campaign").forEach((el) => {
    el.classList.toggle("disabled", !data.is_active);
  });
  const warning = document.getElementById("warning-no-campaign");
  if (data.is_active) {
    warning.style.display = "none";
  } else {
    warning.style.display = "block";
  }
});

const modal = new NewPersonModal(socket);
document.getElementById("new-person-btn").addEventListener("click", () => {
  modal.open();
});
