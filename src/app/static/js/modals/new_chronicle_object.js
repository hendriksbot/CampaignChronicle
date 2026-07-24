import { Modal } from "./modal.js";

export class NewChronicleObjectModal {
  constructor(socket) {
    this.root = document.getElementById("new-chronicle-object-modal");
    this.nameInput = document.getElementById("chronicle-object-name");
    this.saveButton = this.root.querySelector(".save-btn");
    this.socket = socket;
    this.modal = new Modal(this.root);
    this.setupEvents();
  }

  open() {
    this.modal.open();
    this.#resetInputFields();
  }

  close() {
    this.modal.close();
  }

  setupEvents() {
    this.saveButton?.addEventListener("click", () => this.save());
  }

  #resetInputFields() {
    this.nameInput.value = "";
    this.#setFieldError(this.nameInput, "");
  }

  #setFieldError(inputEl, message) {
    const inputId = inputEl.id;
    const errorEl = document.getElementById(`${inputId}-error`);
    if (message) {
      inputEl.classList.add("error");
      inputEl.parentElement.classList.add("error");
      errorEl.textContent = message;
    } else {
      inputEl.classList.remove("error");
      inputEl.parentElement.classList.remove("error");
      errorEl.textContent = "";
    }
  }

  #isValidInput() {
    let isValid = true;
    if (!this.nameInput.value) {
      isValid = false;
      this.#setFieldError(this.nameInput, "Der Name fehlt.");
    } else {
      this.#setFieldError(this.nameInput, "");
    }
    return isValid;
  }

  save() {
    if (!this.#isValidInput()) {
      return;
    }
    this.socket.emit("request_create_person", {
      name: this.nameInput.value,
      markdown: "",
    });
    this.close();
  }
}
