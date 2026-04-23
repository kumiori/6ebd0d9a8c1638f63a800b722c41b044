from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

from services.visual_primitives import apply_visual_lab_theme
from ui import set_page


ROOT = Path(__file__).resolve().parents[1]
CSS_PATH = ROOT / "assets" / "effects" / "fragment_board.css"
FRAGMENTS_PATH = ROOT / "assets" / "fragments" / "fragments_fr.json"


def _fragment_board_html() -> str:
    css = CSS_PATH.read_text(encoding="utf-8")
    source_fragments = json.loads(FRAGMENTS_PATH.read_text(encoding="utf-8"))
    html = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>__CSS__</style>
</head>
<body>
  <div id="app"></div>
  <script type="module">
    import React, { useMemo, useRef, useState } from "https://esm.sh/react@19";
    import { createRoot } from "https://esm.sh/react-dom@19/client";
    import {
      DndContext,
      PointerSensor,
      closestCenter,
      useSensor,
      useSensors,
    } from "https://esm.sh/@dnd-kit/core@6.3.1";
    import {
      SortableContext,
      arrayMove,
      rectSortingStrategy,
      useSortable,
    } from "https://esm.sh/@dnd-kit/sortable@10.0.0";
    import { CSS } from "https://esm.sh/@dnd-kit/utilities@3.2.2";

    const e = React.createElement;

    const sourceFragments = __FRAGMENTS_JSON__.map((fragment) => ({
      id: `source-${fragment.id}`,
      sourceId: String(fragment.id),
      number: String(fragment.id),
      text: fragment.text,
      tags: fragment.tags ?? [],
      kind: "source",
    }));
    const sourceByNumber = new Map(sourceFragments.map((fragment) => [fragment.number, fragment]));
    const storyPresets = {
      spine: {
        label: "Version A — Spine",
        steps: [
          ["1"],
          ["3"],
          ["5"],
          ["20"],
          ["18"],
          ["35+6"],
          ["6"],
          ["13 CUT 2"],
          ["14"],
          ["35+4"],
          ["20"],
          ["20 CUT"],
          ["8"],
          ["21"],
          ["23"],
          ["29"],
          ["XXX"],
          ["31 CUT"],
          ["35+9"],
          ["33"],
        ],
      },
      ritual: {
        label: "Version B — Ritual",
        steps: [
          ["1"],
          ["10"],
          ["20"],
          ["3"],
          ["5"],
          [],
          ["18"],
          ["16", "17"],
          ["20"],
          ["6"],
          ["14"],
          ["8"],
          ["35+4"],
          ["20"],
          ["35+3"],
          ["20"],
          ["21"],
          ["23", "20"],
          ["29"],
          ["37"],
          ["33"],
        ],
      },
      impact: {
        label: "Version C — Impact",
        steps: [
          ["1"],
          ["5"],
          ["18"],
          ["35+6"],
          ["16"],
          ["17"],
          ["6"],
          ["14"],
          ["35+4"],
          ["20"],
          ["35+8"],
          ["31"],
          ["29"],
          [],
          ["35+7"],
          ["37"],
          ["35+9"],
          ["33"],
        ],
      },
    };

    function buildOccurrence(ref, presetKey, stepIndex, partIndex) {
      const base = sourceByNumber.get(ref);
      if (base) {
        return {
          ...base,
          id: `${presetKey}-${String(stepIndex + 1).padStart(2, "0")}-${partIndex}-${ref}`,
          sourceId: ref,
          kind: "source",
        };
      }
      return {
        id: `${presetKey}-${String(stepIndex + 1).padStart(2, "0")}-${partIndex}-${ref}`,
        sourceId: ref,
        number: ref,
        text: ref === "XXX"
          ? "Point d'insertion XXX. Texte à préciser dans la version finale."
          : `Fragment ajouté ${ref}. Texte à compléter dans assets/fragments/fragments_fr.json.`,
        tags: ["added", "missing-text"],
        kind: "added",
      };
    }

    function buildPreset(presetKey) {
      const preset = storyPresets[presetKey];
      return preset.steps.flatMap((step, stepIndex) =>
        step.map((ref, partIndex) => buildOccurrence(ref, presetKey, stepIndex, partIndex)),
      );
    }

    function buildSourcePool() {
      return sourceFragments.map((fragment) => ({
        ...fragment,
        id: `pool-${fragment.sourceId}`,
      }));
    }

    function normalizeFragmentNumber(value) {
      return String(value ?? "").trim();
    }

    function makeLocalFragment(number, text, sequence) {
      const normalized = normalizeFragmentNumber(number);
      const source = sourceByNumber.get(normalized);
      const providedText = String(text ?? "").trim();

      if (source && !providedText) {
        return {
          ...source,
          id: `local-${sequence}-${normalized}`,
          kind: "source",
        };
      }

      return {
        id: `local-${sequence}-${normalized || "unnumbered"}`,
        sourceId: normalized,
        number: normalized || "?",
        text: providedText || (source?.text ?? `Fragment ${normalized || "sans numéro"}. Texte à compléter.`),
        tags: providedText ? ["local"] : ["local", "missing-text"],
        kind: providedText ? "local" : "added",
      };
    }

    function FragmentCard({ fragment, index, isReordered, onRemove }) {
      const {
        attributes,
        listeners,
        setNodeRef,
        transform,
        transition,
        isDragging,
      } = useSortable({ id: fragment.id });
      const style = {
        transform: CSS.Transform.toString(transform),
        transition,
      };

      return e(
        "li",
        {
          ref: setNodeRef,
          style,
          className: `fragment-card${isDragging ? " is-dragging" : ""}${fragment.kind === "added" ? " is-added" : ""}${isReordered ? " is-reordered" : ""}`,
          "data-component-id": `J-FRAGMENT-CARD-${fragment.number}`,
          ...attributes,
          ...listeners,
        },
        e(
          "div",
          { className: "fragment-number" },
          e("strong", null, fragment.number),
          e("span", { className: "fragment-position" }, `pos ${String(index + 1).padStart(2, "0")}`),
        ),
        e("p", { className: "fragment-text" }, fragment.text),
        e(
          "div",
          { className: "fragment-handle" },
          e("span", null, fragment.kind === "added" ? "added" : "drag"),
          e(
            "button",
            {
              className: "fragment-remove-button",
              type: "button",
              onPointerDown: (event) => event.stopPropagation(),
              onClick: (event) => {
                event.stopPropagation();
                onRemove(fragment.id);
              },
            },
            "remove",
          ),
        ),
      );
    }

    function App() {
      const [activePreset, setActivePreset] = useState("spine");
      const [fragments, setFragments] = useState(() => buildPreset("spine"));
      const [addNumber, setAddNumber] = useState("");
      const [removeNumber, setRemoveNumber] = useState("");
      const [editMessage, setEditMessage] = useState("Local edits are not persisted yet.");
      const localSequence = useRef(0);
      const sensors = useSensors(
        useSensor(PointerSensor, {
          activationConstraint: {
            distance: 5,
          },
        }),
      );
      const fragmentIds = useMemo(() => fragments.map((fragment) => fragment.id), [fragments]);
      const availableFragments = useMemo(
        () => {
          const listedNumbers = new Set(fragments.map((fragment) => fragment.number));
          return sourceFragments
            .map((fragment) => fragment.number)
            .filter((number) => !listedNumbers.has(number));
        },
        [fragments],
      );
      const originalIds = useMemo(
        () => (activePreset === "pool" ? buildSourcePool() : buildPreset(activePreset)).map((fragment) => fragment.id),
        [activePreset],
      );

      const sequenceText = useMemo(
        () => [
          `Preset: ${activePreset === "pool" ? "Source pool" : storyPresets[activePreset].label}`,
          "",
          ...fragments.map((fragment, index) => `${String(index + 1).padStart(2, "0")}. ${fragment.number} — ${fragment.text}`),
        ].join("\\n"),
        [activePreset, fragments],
      );

      const orderOnlyText = useMemo(
        () => fragments.map((fragment) => fragment.number).join("\\n"),
        [fragments],
      );

      function applyPreset(presetKey) {
        setActivePreset(presetKey);
        setFragments(presetKey === "pool" ? buildSourcePool() : buildPreset(presetKey));
        setEditMessage("Preset loaded. Local edits were reset.");
      }

      function handleDragEnd(event) {
        const { active, over } = event;
        if (!over || active.id === over.id) return;
        setFragments((items) => {
          const oldIndex = items.findIndex((fragment) => fragment.id === active.id);
          const newIndex = items.findIndex((fragment) => fragment.id === over.id);
          return arrayMove(items, oldIndex, newIndex);
        });
      }

      async function copyText(text, label) {
        try {
          await navigator.clipboard.writeText(text);
          setEditMessage(`${label} copied.`);
        } catch {
          window.prompt(`Copy ${label}`, text);
        }
      }

      function addFragment() {
        const normalized = normalizeFragmentNumber(addNumber);
        if (!normalized) {
          setEditMessage("Add failed: provide a fragment number.");
          return;
        }
        localSequence.current += 1;
        const nextFragment = makeLocalFragment(normalized, "", localSequence.current);
        setFragments((items) => [...items, nextFragment]);
        setAddNumber("");
        setEditMessage(`Added fragment ${nextFragment.number} at the end of the board.`);
      }

      function removeFragment(removeAll = false) {
        const normalized = normalizeFragmentNumber(removeNumber);
        if (!normalized) {
          setEditMessage("Remove failed: provide a fragment number.");
          return;
        }

        setFragments((items) => {
          const matches = items.filter((fragment) => fragment.number === normalized).length;
          if (!matches) {
            setEditMessage(`No fragment ${normalized} found in the current board.`);
            return items;
          }

          if (removeAll) {
            setEditMessage(`Removed ${matches} occurrence${matches > 1 ? "s" : ""} of fragment ${normalized}.`);
            return items.filter((fragment) => fragment.number !== normalized);
          }

          let removed = false;
          setEditMessage(`Removed the first occurrence of fragment ${normalized}.`);
          return items.filter((fragment) => {
            if (!removed && fragment.number === normalized) {
              removed = true;
              return false;
            }
            return true;
          });
        });
      }

      function removeFragmentById(fragmentId) {
        setFragments((items) => {
          const target = items.find((fragment) => fragment.id === fragmentId);
          if (!target) return items;
          setEditMessage(`Removed fragment ${target.number}.`);
          return items.filter((fragment) => fragment.id !== fragmentId);
        });
      }

      return e(
        "main",
        { className: "fragment-shell", "data-component-id": "J-FRAGMENT-BOARD-SHELL-001" },
        e(
          "section",
          { className: "fragment-main", "data-component-id": "J-FRAGMENT-BOARD-MAIN-001" },
          e(
            "header",
            { className: "fragment-header", "data-component-id": "J-FRAGMENT-BOARD-HEADER-001" },
            e(
              "div",
              null,
              e("p", { className: "kicker" }, "Reading order lab"),
              e("h1", null, "Fragment sequencing board"),
              e("p", { className: "intro-copy" }, "A working board for finalising the order of a reading. Load Spine, Ritual, or Impact, then drag fragments until the sequence holds."),
            ),
            e(
              "div",
              { className: "board-meta", "data-component-id": "J-FRAGMENT-COUNT-001" },
              e("span", { className: "board-count" }, fragments.length),
              e("span", null, activePreset === "pool" ? "source fragments" : storyPresets[activePreset].label),
            ),
          ),
          e(
            "aside",
            { className: "fragment-side", "data-component-id": "J-FRAGMENT-SIDE-001" },
            e(
              "section",
              { className: "side-panel", "data-component-id": "J-FRAGMENT-ORDER-RAIL-001" },
              e("h2", null, "Story version"),
              e(
                "div",
                { className: "preset-actions" },
                e("button", { className: `preset-button${activePreset === "spine" ? " active" : ""}`, type: "button", onClick: () => applyPreset("spine") }, "Spine"),
                e("button", { className: `preset-button${activePreset === "ritual" ? " active" : ""}`, type: "button", onClick: () => applyPreset("ritual") }, "Ritual"),
                e("button", { className: `preset-button${activePreset === "impact" ? " active" : ""}`, type: "button", onClick: () => applyPreset("impact") }, "Impact"),
                e("button", { className: `preset-button${activePreset === "pool" ? " active" : ""}`, type: "button", onClick: () => applyPreset("pool") }, "All"),
              ),
              e("p", { className: "hint" }, "Entries like 35+6 are treated as inserted fragments. CUT steps are omitted from the active preset."),
            ),
            e(
              "section",
              { className: "side-panel", "data-component-id": "J-FRAGMENT-ORDER-RAIL-002" },
              e("h2", null, "Current order"),
              e(
                "ol",
                { className: "order-list" },
                fragments.map((fragment, index) => e("li", { key: fragment.id, className: originalIds[index] !== fragment.id ? "is-reordered" : "" }, fragment.number)),
              ),
            ),
            e(
              "section",
              { className: "side-panel fragment-editor", "data-component-id": "J-FRAGMENT-EDITOR-001" },
              e("h2", null, "Fragment editing"),
              e(
                "div",
                { className: "available-fragments", "data-component-id": "J-FRAGMENT-AVAILABLE-001" },
                e("span", { className: "available-label" }, "Available fragments"),
                e(
                  "div",
                  { className: "available-strip" },
                  availableFragments.map((number) =>
                    e(
                      "button",
                      {
                        key: number,
                        className: "available-chip",
                        type: "button",
                        onClick: () => setAddNumber(number),
                        title: `Use fragment ${number}`,
                      },
                      number,
                    ),
                  ),
                ),
              ),
              e(
                "div",
                { className: "fragment-edit-grid" },
                e(
                  "label",
                  null,
                  e("span", null, "Add number"),
                  e("input", {
                    value: addNumber,
                    onChange: (event) => setAddNumber(event.target.value),
                    placeholder: "35+10",
                  }),
                ),
                e(
                  "label",
                  null,
                  e("span", null, "Remove number"),
                  e("input", {
                    value: removeNumber,
                    onChange: (event) => setRemoveNumber(event.target.value),
                    placeholder: "20",
                  }),
                ),
              ),
              e(
                "div",
                { className: "actions" },
                e("button", { className: "action-button primary", type: "button", onClick: addFragment }, "Add selected"),
                e("button", { className: "action-button", type: "button", onClick: () => removeFragment(false) }, "Remove selected"),
                e("button", { className: "action-button", type: "button", onClick: () => removeFragment(true) }, "Remove all"),
              ),
              e("p", { className: "hint" }, editMessage),
            ),
            e(
              "section",
              { className: "side-panel", "data-component-id": "J-FRAGMENT-ACTIONS-001" },
              e("h2", null, "Board actions"),
              e(
                "div",
                { className: "actions" },
                e("button", { className: "action-button primary", type: "button", onClick: () => copyText(orderOnlyText, "Order") }, "Copy order only"),
                e("button", { className: "action-button", type: "button", onClick: () => copyText(sequenceText, "Full sequence") }, "Copy full text"),
                e("button", { className: "action-button", type: "button", onClick: () => applyPreset(activePreset) }, "Reset"),
              ),
              e("p", { className: "hint" }, "The export below updates as cards move. It can become the handoff format for the final reading sequence."),
            ),
            e(
              "section",
              { className: "side-panel", "data-component-id": "J-FRAGMENT-EXPORT-001" },
              e("h2", null, "Sequence export"),
              e("textarea", { className: "order-export", readOnly: true, value: sequenceText }),
            ),
          ),
          e(
            DndContext,
            {
              sensors,
              collisionDetection: closestCenter,
              onDragEnd: handleDragEnd,
            },
            e(
              SortableContext,
              {
                items: fragmentIds,
                strategy: rectSortingStrategy,
              },
              e(
                "ol",
                {
                  className: "fragment-board",
                  "data-component-id": "J-FRAGMENT-BOARD-001",
                },
                fragments.map((fragment, index) =>
                  e(FragmentCard, {
                    key: fragment.id,
                    fragment,
                    index,
                    isReordered: originalIds[index] !== fragment.id,
                    onRemove: removeFragmentById,
                  }),
                ),
              ),
            ),
          ),
        ),
      );
    }

    createRoot(document.getElementById("app")).render(e(App));
  </script>
</body>
</html>
"""
    return html.replace("__CSS__", css).replace(
        "__FRAGMENTS_JSON__", json.dumps(source_fragments, ensure_ascii=False)
    )


set_page("Test Fragment Board", "🧩")
apply_visual_lab_theme("e")

st.markdown(
    "<div class='vl-component-id'>J-FRAGMENT-BOARD-PAGE-001</div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div class='vl-section-label'>visual test j / fragment board</div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<h1 class='vl-hero-title serif'>Order the reading fragments</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p class='vl-subtitle'>A larger draggable board for arranging numbered text fragments into a final sequence.</p>",
    unsafe_allow_html=True,
)

st.iframe(_fragment_board_html(), height=1180)
