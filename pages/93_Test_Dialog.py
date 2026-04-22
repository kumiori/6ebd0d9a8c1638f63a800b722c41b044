from __future__ import annotations

import streamlit as st

from services.css_demo import render_css_demo
from ui import apply_theme, heading, set_page


set_page("Test Dialog", "🧪")
apply_theme()
heading(
    "css expansion",
    "Native dialog",
    "A controlled replacement candidate for the access-key and consent modals.",
)

render_css_demo(
    r"""
<style>
dialog {
  width: min(620px, calc(100vw - 32px));
  border: 2px solid var(--pink);
  border-radius: 8px;
  background: #060606;
  color: var(--ink);
  padding: 24px;
}
dialog::backdrop {
  background: rgba(0, 0, 0, 0.72);
  backdrop-filter: blur(3px);
}
.dialog-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 18px;
}
</style>
<main class="demo-shell">
  <div>
    <div class="kicker">native modal</div>
    <h1>Real focus trap</h1>
    <p>The browser handles the modal layer, Escape close, and focus containment.</p>
  </div>
  <section class="panel">
    <button id="open-dialog">Open access dialog</button>
    <dialog id="native-dialog">
      <h2>Create access key</h2>
      <p>This is the candidate pattern for replacing the fragile Streamlit dialog.</p>
      <label>Name or handle<input placeholder="anonymous" /></label>
      <div class="dialog-actions">
        <button class="secondary" onclick="this.closest('dialog').close()">Cancel</button>
        <button onclick="this.closest('dialog').close('mint')">Mint key</button>
      </div>
    </dialog>
  </section>
</main>
<script>
document.getElementById("open-dialog").addEventListener("click", () => {
  document.getElementById("native-dialog").showModal();
});
</script>
""",
    height=560,
)
