import { Modal } from "./modal.js";

export class NewRelationModal {
  constructor(socket) {
    this.socket = socket;

    this.root = document.getElementById("new-relation-modal");
    this.modal = new Modal(this.root);

    this.sourceInput = this.root.querySelector("#relation-source");
    this.targetInput = this.root.querySelector("#relation-target");

    this.typeSelect = this.root.querySelector("#relation-type");
    this.directionGroup = this.root.querySelector("#relation-direction-group");
    this.directionSelect = this.root.querySelector("#relation-direction");

    this.saveButton = this.root.querySelector(".save-btn");

    this.sourceInfo = null;
    this.targetInfo = null;
    this.relationshipDefinitions = new Map();

    this.setupEvents();
  }

  setupEvents() {
    this.saveButton.addEventListener("click", () => this.save());

    this.typeSelect.addEventListener("change", () => this.updateDirectionVisibility());
  }

  open(sourceInfo, targetInfo, relationshipDefinitions) {
    this.sourceInfo = sourceInfo;
    this.targetInfo = targetInfo;

    this.relationshipDefinitions = relationshipDefinitions;

    this.sourceInput.value = sourceInfo.label;
    this.targetInput.value = targetInfo.label;

    this.fillRelationshipTypes();
    this.updateDirectionVisibility();

    this.modal.open();
  }

  close() {
    this.modal.close();
  }

  fillRelationshipTypes() {
    this.typeSelect.replaceChildren();

    for (const def of this.relationshipDefinitions.values()) {
      this.typeSelect.add(new Option(def.label, def.type));
    }
  }

  updateDirectionVisibility() {
    const definition = this.relationshipDefinitions.get(this.typeSelect.value);

    if (!definition) return;

    if (!definition.directed) {
      this.directionGroup.classList.add("hidden");
    } else {
      this.directionGroup.classList.remove("hidden");

      this.directionSelect.replaceChildren();

      this.directionSelect.add(
        new Option(
          `${this.sourceInfo.label} — ${definition.label} → ${this.targetInfo.label}`,
          "forward"
        )
      );

      this.directionSelect.add(
        new Option(
          `${this.targetInfo.label} — ${definition.label} → ${this.sourceInfo.label}`,
          "reverse"
        )
      );
    }
  }

  save() {
    let sourceId = this.sourceInfo.id;
    let targetId = this.targetInfo.id;

    if (this.directionSelect.value === "reverse") {
      [sourceId, targetId] = [targetId, sourceId];
    }

    this.socket.emit("request_create_relation", {
      source_id: sourceId,
      target_id: targetId,
      type: this.typeSelect.value,
    });

    this.close();
  }
}
