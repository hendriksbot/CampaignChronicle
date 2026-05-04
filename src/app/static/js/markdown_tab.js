function switchTab(tab, markdownRawId, markdownPreviewId) {
  const textarea = document.getElementById(markdownRawId);
  const preview = document.getElementById(markdownPreviewId);

  // Tabs reset
  document.querySelectorAll(".editor-tabs .tab").forEach((t) => t.classList.remove("active"));

  // Activate correct tab
  document.querySelector(`[data-tab="${tab}"]`).classList.add("active");

  if (tab === "edit") {
    textarea.classList.remove("hidden");
    preview.classList.add("hidden");
  } else {
    textarea.classList.add("hidden");
    preview.classList.remove("hidden");

    // Backend rendering trigger
    socket.emit("render_markdown", {
      content: textarea.value,
    });
  }
}
