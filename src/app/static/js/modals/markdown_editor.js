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

    this.toolbar = this.root.querySelector(".editor-toolbar");
    this.toolbarOverflow = this.root.querySelector(".toolbar-overflow");
    this.toolbarOverflowMenu = this.root.querySelector(".overflow-menu");

    this.toolbarButtons = [...this.toolbar.querySelectorAll(".toolbar-btn")].filter(
      (btn) => !btn.classList.contains("overflow-btn")
    );

    this.resizeObserver = new ResizeObserver(() => this.updateToolbar());
    this.resizeObserver.observe(this.root.querySelector(".editor-header"));

    this.mode = "edit";
    this.setupEvents();
    this.updateToolbar();
  }

  destroy() {
    document.removeEventListener("click", this.handleDocumentClick);
  }

  setupEvents() {
    this.tabEdit.addEventListener("click", () => {
      this.switchTab("edit");
    });

    this.tabPreview.addEventListener("click", () => {
      this.switchTab("preview");
    });

    const overflowBtn = this.root.querySelector(".overflow-btn");

    overflowBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      this.toggleOverflowMenu();
    });

    document.addEventListener("click", this.handleDocumentClick);
  }

  reinit() {
    this.switchTab("edit");
  }

  handleDocumentClick = (e) => {
    this.toolbarOverflowMenu.classList.add("hidden");
  };

  toggleOverflowMenu() {
    const isHidden = this.toolbarOverflowMenu.classList.contains("hidden");

    if (isHidden) {
      this.toolbarOverflowMenu.classList.remove("hidden");
    } else {
      this.toolbarOverflowMenu.classList.add("hidden");
    }
  }

  async switchTab(tab) {
    this.mode = tab;

    if (tab === "edit") {
      this.input.classList.remove("hidden");
      this.toolbar.classList.remove("hidden");
      this.preview.classList.add("hidden");

      this.tabEdit.classList.add("active");
      this.tabPreview.classList.remove("active");
    }

    if (tab === "preview") {
      await this.render();
      this.input.classList.add("hidden");
      this.toolbar.classList.add("hidden");
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

  updateToolbar() {
    requestAnimationFrame(() => {
      const toolbar = this.toolbar;

      // 1. Stelle sicher, dass alle Buttons im DOM sind (ohne Reset-Reihenfolge zu zerstören)
      for (const btn of this.toolbarButtons) {
        if (btn.parentElement !== toolbar && btn.parentElement !== this.toolbarOverflowMenu) {
          toolbar.insertBefore(btn, this.toolbarOverflow);
        }
      }

      // 2. Overflow erzeugen (von rechts nach links)
      for (let i = this.toolbarButtons.length - 1; i >= 0; i--) {
        const btn = this.toolbarButtons[i];

        if (btn.parentElement !== toolbar) continue;

        if (toolbar.scrollWidth > toolbar.clientWidth) {
          this.toolbarOverflow.classList.remove("hidden");
          this.toolbarOverflowMenu.prepend(btn);
        }
      }

      // 3. Rückholen (von links nach rechts → WICHTIG für Ordnung)
      for (const btn of this.toolbarButtons) {
        if (btn.parentElement !== this.toolbarOverflowMenu) continue;

        toolbar.insertBefore(btn, this.toolbarOverflow);

        if (toolbar.scrollWidth > toolbar.clientWidth) {
          // passt nicht → wieder zurück
          this.toolbarOverflowMenu.insertBefore(btn, this.toolbarOverflowMenu.firstChild);
          break; // wichtig: nur ein Schritt pro Layout-Phase
        }
      }

      // 4. Overflow verstecken wenn leer
      if (this.toolbarOverflowMenu.children.length === 0) {
        this.toolbarOverflow.classList.add("hidden");
      }
    });
  }

  setContent(value) {
    this.input.value = value;
    this.render();
  }

  getContent() {
    return this.input.value;
  }
}
