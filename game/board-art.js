"use strict";

// Project-owned stroke glyphs from src/kenken/rendering/typography.py.
// The terms are recorded in src/kenken/rendering/VECTOR_FONT_LICENSE.txt.
const boardGlyphs = {
  "0": [
    [[100,0],[400,0],[500,100],[500,600],[400,700],[100,700],[0,600],[0,100],[100,0]],
    [[80,620],[420,80]],
  ],
  "1": [[[100,150],[250,0],[250,700]],[[80,700],[430,700]]],
  "2": [[[0,120],[100,0],[400,0],[500,120],[500,260],[0,700],[500,700]]],
  "3": [
    [[0,80],[100,0],[400,0],[500,100],[500,250],[400,350],[200,350]],
    [[400,350],[500,450],[500,600],[400,700],[100,700],[0,620]],
  ],
  "4": [[[400,700],[400,0],[0,470],[500,470]]],
  "5": [[[500,0],[0,0],[0,330],[400,330],[500,430],[500,600],[400,700],[100,700],[0,620]]],
  "6": [[[500,80],[400,0],[120,0],[0,150],[0,580],[120,700],[400,700],[500,580],[500,430],[400,330],[0,330]]],
  "7": [[[0,0],[500,0],[160,700]]],
  "8": [[[100,350],[0,250],[0,100],[100,0],[400,0],[500,100],[500,250],[400,350],[100,350],[0,450],[0,600],[100,700],[400,700],[500,600],[500,450],[400,350]]],
  "9": [[[500,370],[100,370],[0,270],[0,100],[100,0],[400,0],[500,120],[500,550],[380,700],[100,700],[0,620]]],
  "−": [[[50,350],[450,350]]],
  "+": [[[50,350],[450,350]],[[250,150],[250,550]]],
  "×": [[[70,150],[430,550]],[[430,150],[70,550]]],
  "÷": [[[50,350],[450,350]],[[250,110],[250,130]],[[250,570],[250,590]]],
};

// Worksheet units and palette from src/kenken/rendering/puzzle.py.
const cellSize = 1000;
const coordinateGutter = 360;
const boardMargin = 60;
const cageFills = ["#ebf6eb", "#e8f3fb", "#f3edfa", "#fcf4e1", "#fbebee"];

function svgElement(name, attributes = {}) {
  const element = document.createElementNS("http://www.w3.org/2000/svg", name);
  for (const [attribute, value] of Object.entries(attributes)) {
    element.setAttribute(attribute, value);
  }
  return element;
}

function strokePath(path, width, className) {
  return svgElement("path", {
    class: className,
    d: path,
    fill: "none",
    stroke: "currentColor",
    "stroke-width": width,
    "stroke-linecap": "round",
    "stroke-linejoin": "round",
  });
}

function glyphWidth(text, height) {
  return Math.floor(((text.length - 1) * 600 + 500) * height / 700);
}

function glyphPath(text, x, y, height) {
  let path = "";
  const scale = coordinate => Math.floor(coordinate * height / 700);
  for (const character of text) {
    for (const stroke of boardGlyphs[character]) {
      path += "M" + stroke.map(([px, py]) => `${x + scale(px)},${y + scale(py)}`).join("L");
    }
    x += scale(600);
  }
  return path;
}

function centeredGlyphPath(text, center, y, height) {
  return glyphPath(text, center - Math.floor(glyphWidth(text, height) / 2), y, height);
}

function cageClue(text) {
  let height = 225;
  while (glyphWidth(text, height) > 840) height -= 5;
  return strokePath(glyphPath(text, 80, 75, height), Math.max(24, Math.floor(height / 8)), "clue");
}

function cageColors(size, cages, cellCages) {
  const colors = new Map();
  cages.forEach((cage, cageIndex) => {
    const unavailable = new Set();
    for (const index of cage.indexes) {
      const row = Math.floor(index / size);
      const column = index % size;
      for (const [r, c] of [[row - 1, column], [row + 1, column], [row, column - 1], [row, column + 1]]) {
        if (r >= 0 && r < size && c >= 0 && c < size) {
          unavailable.add(colors.get(cellCages[r * size + c]));
        }
      }
    }
    const color = cageFills.find(candidate => !unavailable.has(candidate));
    colors.set(cage, color ?? cageFills[cageIndex % cageFills.length]);
  });
  return colors;
}

function drawBoardArt(frame, artwork, size, cages, cellCages) {
  const start = coordinateGutter;
  const end = start + size * cellSize;
  const extent = end + boardMargin;
  frame.style.setProperty("--board-start", `${100 * start / extent}%`);
  frame.style.setProperty("--board-end", `${100 * boardMargin / extent}%`);
  artwork.setAttribute("viewBox", `0 0 ${extent} ${extent}`);

  const colors = cageColors(size, cages, cellCages);
  const fills = svgElement("g", { class: "cage-fills" });
  let grid = "";
  let boundaries = "";
  let coordinates = "";

  cellCages.forEach((cage, index) => {
    const row = Math.floor(index / size);
    const column = index % size;
    const x = start + column * cellSize;
    const y = start + row * cellSize;
    fills.append(svgElement("rect", { x, y, width: cellSize, height: cellSize, fill: colors.get(cage) }));
    if (column + 1 < size && cage !== cellCages[index + 1]) {
      boundaries += `M${x + cellSize},${y}v${cellSize}`;
    }
    if (row + 1 < size && cage !== cellCages[index + size]) {
      boundaries += `M${x},${y + cellSize}h${cellSize}`;
    }
  });

  for (let index = 0; index < size; index++) {
    const offset = start + index * cellSize;
    if (index > 0) grid += `M${offset},${start}V${end}M${start},${offset}H${end}`;
    const number = String(index + 1);
    coordinates += centeredGlyphPath(number, offset + cellSize / 2, 95, 190);
    coordinates += centeredGlyphPath(number, start / 2, offset + 405, 190);
  }

  artwork.replaceChildren(
    fills,
    strokePath(grid, 14, "cell-lines"),
    strokePath(boundaries, 40, "cage-lines"),
    strokePath(`M${start},${start}H${end}V${end}H${start}Z`, 48, "cage-lines"),
    strokePath(coordinates, 24, "coordinates"),
  );
}
