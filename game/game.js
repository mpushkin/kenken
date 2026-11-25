"use strict";

const workspace = document.querySelector(".workspace");
const sizePicker = document.querySelector("#size");
const difficultyPicker = document.querySelector("#difficulty");
const board = document.querySelector("#board");
const boardFrame = document.querySelector(".board-frame");
const artwork = document.querySelector("#board-art");
const keypad = document.querySelector("#keypad");
const progress = document.querySelector("#progress");
const feedback = document.querySelector("#status");
const randomButton = document.querySelector("#random");
const shareButton = document.querySelector("#share");
const sharePanel = document.querySelector("#share-panel");
const shareUrl = document.querySelector("#share-url");
const shareStatus = document.querySelector("#share-status");
const unknownPuzzle = document.querySelector("#unknown-puzzle");
const solvedList = document.querySelector("#solved-list");
const solvedEmpty = document.querySelector("#solved-empty");
const symbols = { given: "", add: "+", multiply: "×", subtract: "−", divide: "÷" };
const storagePrefix = "kenken.game.v1:";
const boards = new Map();
const selectedByPair = new Map();
const solved = new Map();
const solvedDate = new Intl.DateTimeFormat(undefined, { dateStyle: "medium" });

const pairKey = (size, profile) => `${size}:${profile}`;
const puzzlePair = record => pairKey(record.size, record.provenance.profile);
const puzzleGroups = new Map();
const puzzlesById = new Map();
for (const record of PUZZLES) {
  if (puzzlesById.has(record.id)) continue;
  puzzlesById.set(record.id, record);
  const key = puzzlePair(record);
  if (!puzzleGroups.has(key)) puzzleGroups.set(key, []);
  puzzleGroups.get(key).push(record);
}

const set21 = Array.isArray(globalThis.KENKEN_SET_21) ? globalThis.KENKEN_SET_21 : [];
for (const record of set21) {
  if (record?.schema === "kenken.puzzle/v1" &&
      /^kk-([45])x\1-[0-9a-f]{16}$/.test(record.id) &&
      record.id.startsWith(`kk-${record.size}x${record.size}-`) &&
      puzzleGroups.has(pairKey(record.size, record.provenance?.profile)) &&
      !puzzlesById.has(record.id)) {
    puzzlesById.set(record.id, record);
  }
}

let puzzle;
let cages;
let cellCages;
let values;
let cells;
let selected;
let conflicts = new Set();

function readSaved(key) {
  try {
    return JSON.parse(localStorage.getItem(storagePrefix + key));
  } catch {
    return null;
  }
}

function save(key, value) {
  try {
    localStorage.setItem(storagePrefix + key, JSON.stringify(value));
  } catch {
    // Keep playing with the in-memory board when storage is unavailable.
  }
}

function initialValues(saved) {
  return cellCages.map((cage, index) => {
    if (cage.operator === "given") return cage.target;
    const value = Array.isArray(saved) ? saved[index] : 0;
    return Number.isInteger(value) && value >= 1 && value <= puzzle.size ? value : 0;
  });
}

function storeBoard() {
  boards.set(puzzle.id, values);
  save(puzzle.id, values);
}

function setFeedback(message = "", state) {
  feedback.textContent = message;
  if (state) {
    feedback.dataset.state = state;
  } else {
    delete feedback.dataset.state;
  }
}

function button(label, className) {
  const element = document.createElement("button");
  element.type = "button";
  element.textContent = label;
  if (className) element.className = className;
  return element;
}

function buildBoard() {
  const { size } = puzzle;
  drawBoardArt(boardFrame, artwork, size, cages, cellCages);
  board.style.setProperty("--size", size);
  board.replaceChildren();
  cells = [];

  for (let row = 0; row < size; row++) {
    const rowElement = document.createElement("div");
    rowElement.className = "board-row";
    rowElement.setAttribute("role", "row");
    for (let column = 0; column < size; column++) {
      const index = row * size + column;
      const cage = cellCages[index];
      const given = cage.operator === "given";
      const gridCell = document.createElement("div");
      gridCell.className = "grid-cell";
      gridCell.setAttribute("role", "gridcell");

      const cellButton = button("", given ? "cell given" : "cell");
      cellButton.dataset.index = index;
      const drawing = svgElement("svg", {
        viewBox: `0 0 ${cellSize} ${cellSize}`,
        "aria-hidden": "true",
        focusable: "false",
      });
      if (!given && cage.indexes[0] === index) {
        drawing.append(cageClue(cage.target + symbols[cage.operator]));
      }
      const value = strokePath("", 45, "value");
      drawing.append(value);
      cellButton.append(drawing);
      gridCell.append(cellButton);
      rowElement.append(gridCell);

      const position = `Row ${row + 1}, column ${column + 1}`;
      const clueLabel = given ? "" : `, cage target ${cage.target}, ${cage.operator}`;
      cells.push({ gridCell, cellButton, value, given, label: position + clueLabel });
    }
    board.append(rowElement);
  }
}

function buildKeypad() {
  keypad.replaceChildren();
  for (let digit = 1; digit <= puzzle.size; digit++) {
    const key = button(digit);
    key.dataset.digit = digit;
    keypad.append(key);
  }
  const clear = button("Clear", "clear");
  clear.dataset.digit = 0;
  keypad.append(clear);
}

function renderState() {
  let filled = 0;
  let editable = 0;
  cells.forEach(({ gridCell, cellButton, value, given, label }, index) => {
    const digit = values[index];
    const conflict = conflicts.has(index);
    value.setAttribute("d", digit ? centeredGlyphPath(String(digit), 500, given ? 270 : 390, 460) : "");
    gridCell.setAttribute("aria-selected", index === selected);
    cellButton.tabIndex = index === selected ? 0 : -1;
    cellButton.classList.toggle("in-cage", cellCages[index] === cellCages[selected]);
    cellButton.classList.toggle("conflict", conflict);

    const entry = given ? `given ${digit}` : digit || "empty";
    cellButton.setAttribute("aria-label", `${label}, ${entry}${conflict ? ", conflict" : ""}`);
    if (!given) {
      editable++;
      if (digit) filled++;
    }
  });
  progress.textContent = `${filled} / ${editable} entered`;
}

function playPuzzle(next) {
  puzzle = next;
  cellCages = new Array(puzzle.size ** 2);
  cages = puzzle.cages.map(({ operator, target, cells }) => {
    const indexes = cells.map(({ row, column }) => row * puzzle.size + column).sort((a, b) => a - b);
    return { operator, target, indexes };
  }).sort((a, b) => a.indexes[0] - b.indexes[0]);
  for (const cage of cages) {
    for (const index of cage.indexes) cellCages[index] = cage;
  }

  values = boards.get(puzzle.id) ?? initialValues(readSaved(puzzle.id));
  boards.set(puzzle.id, values);
  selected = Math.max(0, cellCages.findIndex(cage => cage.operator !== "given"));
  conflicts.clear();
  setFeedback();
  sharePanel.hidden = true;
  shareButton.setAttribute("aria-expanded", "false");
  shareUrl.value = "";
  shareStatus.textContent = "";
  sizePicker.value = puzzle.size;
  difficultyPicker.value = puzzle.provenance.profile;
  const key = puzzlePair(puzzle);
  selectedByPair.set(key, puzzle.id);
  save(`selected:${key}`, puzzle.id);
  save("selected", puzzle.id);
  randomButton.disabled = !puzzleGroups.get(key).some(record => record.id !== puzzle.id);
  document.querySelector("#number-range").textContent = `1 to ${puzzle.size}`;
  const sizeLabel = sizePicker.selectedOptions[0].textContent;
  const difficultyLabel = difficultyPicker.selectedOptions[0].textContent;
  document.querySelector("#print-name").textContent = `KenKen · ${sizeLabel} · ${difficultyLabel}`;
  document.querySelector("#print-id").textContent = puzzle.id;
  buildBoard();
  buildKeypad();
  renderState();
}

function selectCell(index) {
  selected = index;
  renderState();
  cells[index].cellButton.focus();
}

function enterDigit(digit) {
  if (cellCages[selected].operator === "given") {
    setFeedback("This number is given. Select another cell.", "given");
    return;
  }
  values[selected] = digit;
  conflicts.clear();
  setFeedback();
  storeBoard();
  renderState();
}

function cageMatches(operator, target, digits) {
  switch (operator) {
    case "given": return digits[0] === target;
    case "add": return digits.reduce((sum, digit) => sum + digit, 0) === target;
    case "multiply": return digits.reduce((product, digit) => product * digit, 1) === target;
    case "subtract": return Math.abs(digits[0] - digits[1]) === target;
    case "divide": return Math.max(...digits) === target * Math.min(...digits);
    default: return false;
  }
}

function markRepeats(indexes) {
  const seen = new Map();
  for (const index of indexes) {
    const digit = values[index];
    if (!digit) continue;
    if (seen.has(digit)) {
      conflicts.add(seen.get(digit));
      conflicts.add(index);
    } else {
      seen.set(digit, index);
    }
  }
}

function savedSolveDate(id) {
  const date = readSaved(`solved:${id}`);
  return typeof date === "string" && Number.isFinite(Date.parse(date)) ? date : null;
}

function renderSolved() {
  solvedList.replaceChildren();
  const latestFirst = [...solved].sort((a, b) => Date.parse(b[1]) - Date.parse(a[1]));
  for (const [id, date] of latestFirst) {
    const record = puzzlesById.get(id);
    const item = document.createElement("li");
    const identity = document.createElement("span");
    identity.className = "solved-id";
    identity.textContent = id;
    const details = document.createElement("span");
    const { size, provenance: { profile } } = record;
    const difficulty = difficultyPicker.querySelector(`option[value="${profile}"]`).textContent;
    const time = document.createElement("time");
    time.dateTime = date;
    time.textContent = solvedDate.format(new Date(date));
    details.append(`${size}×${size} · ${difficulty} · `, time);
    item.append(identity, details);
    solvedList.append(item);
  }
  solvedEmpty.hidden = solved.size > 0;
  solvedList.hidden = solved.size === 0;
}

function recordSolve() {
  const { id } = puzzle;
  if (solved.has(id)) return;
  const saved = savedSolveDate(id);
  const date = saved ?? new Date().toISOString();
  solved.set(id, date);
  if (!saved) save(`solved:${id}`, date);
  renderSolved();
}

function checkBoard() {
  conflicts.clear();
  const { size } = puzzle;
  for (let line = 0; line < size; line++) {
    markRepeats(Array.from({ length: size }, (_, offset) => line * size + offset));
    markRepeats(Array.from({ length: size }, (_, offset) => offset * size + line));
  }
  for (const cage of cages) {
    const digits = cage.indexes.map(index => values[index]);
    if (digits.every(Boolean) && !cageMatches(cage.operator, cage.target, digits)) {
      cage.indexes.forEach(index => conflicts.add(index));
    }
  }

  const empty = values.filter(digit => digit === 0).length;
  if (conflicts.size) {
    setFeedback("Incorrect. Marked cells repeat a number or share a cage with the wrong result.", "incorrect");
  } else if (empty) {
    setFeedback(`Incomplete. ${empty} ${empty === 1 ? "cell" : "cells"} left to fill.`, "incomplete");
  } else {
    recordSolve();
    setFeedback("Solved! Every row, column and cage checks out.", "solved");
  }
  renderState();
}

function resetBoard() {
  values = initialValues();
  selected = Math.max(0, cellCages.findIndex(cage => cage.operator !== "given"));
  conflicts.clear();
  storeBoard();
  setFeedback("Puzzle reset.", "reset");
  renderState();
}

const moves = {
  ArrowUp: [-1, 0],
  ArrowDown: [1, 0],
  ArrowLeft: [0, -1],
  ArrowRight: [0, 1],
};

workspace.addEventListener("keydown", event => {
  if (event.altKey || event.ctrlKey || event.metaKey || !event.target.closest("#board, #keypad, .actions")) return;
  const { key } = event;
  const { size } = puzzle;
  if (Object.hasOwn(moves, key)) {
    const [down, across] = moves[key];
    const row = Math.floor(selected / size) + down;
    const column = selected % size + across;
    if (row >= 0 && row < size && column >= 0 && column < size) {
      selectCell(row * size + column);
    }
    event.preventDefault();
  } else if (key === "Backspace" || key === "Delete") {
    event.preventDefault();
    enterDigit(0);
  } else if (/^[1-9]$/.test(key) && Number(key) <= size) {
    event.preventDefault();
    enterDigit(Number(key));
  }
});

board.addEventListener("click", event => {
  const cell = event.target.closest(".cell");
  if (cell) selectCell(Number(cell.dataset.index));
});

keypad.addEventListener("click", event => {
  const key = event.target.closest("button");
  if (key) enterDigit(Number(key.dataset.digit));
});

function changePuzzle() {
  const key = pairKey(sizePicker.value, difficultyPicker.value);
  const remembered = puzzlesById.get(selectedByPair.get(key) ?? readSaved(`selected:${key}`));
  const next = remembered && puzzlePair(remembered) === key ? remembered : puzzleGroups.get(key)[0];
  if (next === puzzle) return;
  clearSharedId();
  playPuzzle(next);
}

function randomPuzzle() {
  const alternatives = puzzleGroups.get(puzzlePair(puzzle)).filter(record => record.id !== puzzle.id);
  if (!alternatives.length) return;
  clearSharedId();
  playPuzzle(alternatives[Math.floor(Math.random() * alternatives.length)]);
  setFeedback(`Opened ${puzzle.id}.`, "opened");
}

async function sharePuzzle() {
  const url = new URL(`/kenken/#${puzzle.id}`, location.href).href;
  shareUrl.value = url;
  sharePanel.hidden = false;
  shareButton.setAttribute("aria-expanded", "true");
  shareStatus.textContent = "";
  try {
    await navigator.clipboard.writeText(url);
    if (shareUrl.value === url) shareStatus.textContent = "Puzzle link copied.";
  } catch {
    if (shareUrl.value !== url) return;
    shareStatus.textContent = "Select and copy this link to share the puzzle.";
    shareUrl.focus();
    shareUrl.select();
  }
}

function clearSharedId() {
  if (location.hash) history.replaceState(null, "", location.pathname + location.search);
}

function openFromLocation() {
  const sharedId = location.hash.slice(1);
  const shared = puzzlesById.get(sharedId);
  if (sharedId && !shared) {
    workspace.hidden = true;
    unknownPuzzle.hidden = false;
    document.querySelector("#unknown-title").focus();
    return;
  }

  const next = shared ?? puzzle ?? puzzlesById.get(readSaved("selected")) ?? PUZZLES[0];
  if (next !== puzzle) playPuzzle(next);
  unknownPuzzle.hidden = true;
  workspace.hidden = false;
}

sizePicker.addEventListener("change", changePuzzle);
difficultyPicker.addEventListener("change", changePuzzle);
document.querySelector("#check").addEventListener("click", checkBoard);
document.querySelector("#reset").addEventListener("click", resetBoard);
document.querySelector("#print").addEventListener("click", () => window.print());
randomButton.addEventListener("click", randomPuzzle);
shareButton.addEventListener("click", sharePuzzle);
document.querySelector("#recover").addEventListener("click", () => {
  clearSharedId();
  openFromLocation();
  sizePicker.focus();
});
window.addEventListener("hashchange", openFromLocation);

for (const id of puzzlesById.keys()) {
  const date = savedSolveDate(id);
  if (date) solved.set(id, date);
}
renderSolved();
openFromLocation();
