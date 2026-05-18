export class Modal {
  constructor(element) {
    this.element = element;
    this.closeButton = this.element.querySelector(".modal-close");
    this.cancelButton = this.element.querySelector(".cancel-btn");
    this.handleKeydown = this.handleKeydown.bind(this);
    document.addEventListener("keydown", this.handleKeydown);
    this.setupEvents();
  }

  open() {
    this.element.classList.remove("hidden");
  }

  close() {
    this.element.classList.add("hidden");
  }

  setupEvents() {
    this.closeButton?.addEventListener("click", () => this.close());

    this.cancelButton?.addEventListener("click", () => this.close());
  }

  handleKeydown(e) {
    if (e.key === "Escape") {
      this.close();
    }
  }

  destroy() {
    document.removeEventListener("keydown", this.handleKeydown);
  }
}
