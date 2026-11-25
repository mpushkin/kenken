"use strict";

const workspace = document.querySelector(".workspace");
const picker = document.querySelector("#puzzle");
const board = document.querySelector("#board");
const keypad = document.querySelector("#keypad");
const progress = document.querySelector("#progress");
const feedback = document.querySelector("#status");
const symbols = { given: "", add: "+", multiply: "×", subtract: "−", divide: "÷" };
const storagePrefix = "kenken.game.v1:";
const boards = new Map();

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
      gridCell.classList.toggle("edge-right", column + 1 < size && cage !== cellCages[index + 1]);
      gridCell.classList.toggle("edge-bottom", row + 1 < size && cage !== cellCages[index + size]);

      const cellButton = button("", given ? "cell given" : "cell");
      cellButton.dataset.index = index;
      if (!given && cage.indexes[0] === index) {
        const clue = document.createElement("span");
        clue.className = "clue";
        clue.setAttribute("aria-hidden", "true");
        clue.textContent = cage.target + symbols[cage.operator];
        cellButton.append(clue);
      }
      const value = document.createElement("span");
      value.className = "value";
      value.setAttribute("aria-hidden", "true");
      cellButton.append(value);
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
    value.textContent = digit || "";
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
    const indexes = cells.map(({ row, column }) => row * puzzle.size + column);
    const cage = { operator, target, indexes };
    indexes.forEach(index => { cellCages[index] = cage; });
    return cage;
  });

  values = boards.get(puzzle.id) ?? initialValues(readSaved(puzzle.id));
  selected = cellCages.findIndex(cage => cage.operator !== "given");
  conflicts.clear();
  setFeedback();
  picker.value = puzzle.id;
  save("selected", puzzle.id);
  document.querySelector("#number-range").textContent = `1 to ${puzzle.size}`;
  document.querySelector("#print-name").textContent = `KenKen · ${picker.selectedOptions[0].textContent}`;
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
    setFeedback("Solved! Every row, column and cage checks out.", "solved");
  }
  renderState();
}

function resetBoard() {
  values = initialValues();
  selected = cellCages.findIndex(cage => cage.operator !== "given");
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

picker.addEventListener("change", () => {
  playPuzzle(PUZZLES.find(candidate => candidate.id === picker.value));
});
document.querySelector("#check").addEventListener("click", checkBoard);
document.querySelector("#reset").addEventListener("click", resetBoard);
document.querySelector("#print").addEventListener("click", () => window.print());

for (const { id, size, provenance } of PUZZLES) {
  const profile = provenance.profile;
  picker.add(new Option(`${size}×${size} · ${profile[0].toUpperCase() + profile.slice(1)}`, id));
}
const savedId = readSaved("selected");
playPuzzle(PUZZLES.find(candidate => candidate.id === savedId) ?? PUZZLES[0]);
workspace.hidden = false;
