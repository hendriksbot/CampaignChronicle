import { Modal } from "./modal.js";

export class ModifyMarkdownModal {
  constructor(socket, type, id) {
    this.root = document.getElementById("modify-markdown-modal");
    this.socket = socket;
    this.type = type;
    this.id = id;
    this.modal = new Modal(this.root);
    this.editor = new MardownEditor(this.root, socket);
    this.saveButton = this.root.querySelector(".save-btn");
    this.setupEvents();
  }

  open() {
    this.editor.reinit();
    this.modal.open();
  }

  close() {
    this.modal.close();
  }

  setupEvents() {
    this.saveButton?.addEventListener("click", () => this.save());
  }

  save() {
    const markdown_raw = this.editor.getContent();
    this.socket.emit("save_markdown", {
      type: this.type,
      id: this.id,
      content: markdown_raw,
    });
    this.close();
  }

  setContent(markdown_raw) {
    this.editor.setContent(markdown_raw);
  }
}

class MardownEditor {
  constructor(rootElement, socket = null) {
    this.root = rootElement;
    this.socket = socket;

    this.input = this.root.querySelector(".editor-input");
    this.preview = this.root.querySelector(".editor-preview");

    this.tabEdit = this.root.querySelector('[data-action="edit"]');
    this.tabPreview = this.root.querySelector('[data-action="preview"]');

    this.mode = "edit";
    this.setupEvents();
  }
  setupEvents() {
    this.tabEdit.addEventListener("click", () => {
      this.switchTab("edit");
    });

    this.tabPreview.addEventListener("click", () => {
      this.switchTab("preview");
    });
  }

  reinit() {
    this.switchTab("edit");
  }

  async switchTab(tab) {
    this.mode = tab;

    if (tab === "edit") {
      this.input.classList.remove("hidden");
      this.preview.classList.add("hidden");

      this.tabEdit.classList.add("active");
      this.tabPreview.classList.remove("active");
    }

    if (tab === "preview") {
      await this.render();
      this.input.classList.add("hidden");
      this.preview.classList.remove("hidden");

      this.tabEdit.classList.remove("active");
      this.tabPreview.classList.add("active");
    }
  }

  async render() {
    const markdown = this.input.value;

    const response = await fetch("/api/render-markdown", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        markdown,
      }),
    });

    const data = await response.json();

    this.preview.innerHTML = data.html;
  }

  setContent(value) {
    this.input.value = value;
    this.render();
  }

  getContent() {
    return this.input.value;
  }
}
