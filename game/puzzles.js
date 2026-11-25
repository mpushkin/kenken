// Original kenken.puzzle/v1 records from tests/fixtures/collections/puzzles.jsonl.
const PUZZLES = [
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-4x4-11d54b73038abba8",
    "size": 4,
    "provenance": {"accepted_attempt":3,"generator_version":"0.3.0","profile":"easy","seed":"2026072704"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":1,"row":0}],"operator":"divide","target":2},
      {"cells":[{"column":2,"row":0},{"column":3,"row":0},{"column":3,"row":1}],"operator":"add","target":8},
      {"cells":[{"column":0,"row":1},{"column":1,"row":1},{"column":2,"row":1}],"operator":"add","target":9},
      {"cells":[{"column":0,"row":2}],"operator":"given","target":2},
      {"cells":[{"column":1,"row":2},{"column":1,"row":3}],"operator":"multiply","target":4},
      {"cells":[{"column":2,"row":2},{"column":3,"row":2}],"operator":"divide","target":3},
      {"cells":[{"column":0,"row":3}],"operator":"given","target":3},
      {"cells":[{"column":2,"row":3},{"column":3,"row":3}],"operator":"subtract","target":2}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-4x4-498d84013f87cacd",
    "size": 4,
    "provenance": {"accepted_attempt":12,"generator_version":"0.3.0","profile":"medium","seed":"2026072701"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":0,"row":1}],"operator":"subtract","target":1},
      {"cells":[{"column":1,"row":0}],"operator":"given","target":3},
      {"cells":[{"column":2,"row":0},{"column":1,"row":1},{"column":2,"row":1}],"operator":"multiply","target":4},
      {"cells":[{"column":3,"row":0},{"column":3,"row":1},{"column":3,"row":2}],"operator":"add","target":9},
      {"cells":[{"column":0,"row":2},{"column":0,"row":3}],"operator":"add","target":5},
      {"cells":[{"column":1,"row":2},{"column":2,"row":2},{"column":1,"row":3}],"operator":"multiply","target":16},
      {"cells":[{"column":2,"row":3},{"column":3,"row":3}],"operator":"subtract","target":2}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-4x4-b01e77f36f89a30c",
    "size": 4,
    "provenance": {"accepted_attempt":1547,"generator_version":"0.2.0","profile":"hard","seed":"2026072509"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":0,"row":1},{"column":0,"row":2},{"column":0,"row":3}],"operator":"multiply","target":24},
      {"cells":[{"column":1,"row":0},{"column":2,"row":0},{"column":3,"row":0},{"column":2,"row":1}],"operator":"add","target":9},
      {"cells":[{"column":1,"row":1},{"column":1,"row":2}],"operator":"subtract","target":1},
      {"cells":[{"column":3,"row":1},{"column":3,"row":2}],"operator":"divide","target":3},
      {"cells":[{"column":2,"row":2},{"column":1,"row":3},{"column":2,"row":3},{"column":3,"row":3}],"operator":"multiply","target":48}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-5x5-8aac7efaf4f1da6b",
    "size": 5,
    "provenance": {"accepted_attempt":2,"generator_version":"0.3.0","profile":"easy","seed":"2026072701"},
    "cages": [
      {"cells":[{"column":0,"row":0}],"operator":"given","target":3},
      {"cells":[{"column":1,"row":0},{"column":2,"row":0},{"column":1,"row":1}],"operator":"add","target":7},
      {"cells":[{"column":3,"row":0},{"column":3,"row":1}],"operator":"subtract","target":3},
      {"cells":[{"column":4,"row":0},{"column":4,"row":1}],"operator":"divide","target":4},
      {"cells":[{"column":0,"row":1},{"column":0,"row":2},{"column":1,"row":2}],"operator":"add","target":8},
      {"cells":[{"column":2,"row":1},{"column":2,"row":2}],"operator":"add","target":8},
      {"cells":[{"column":3,"row":2},{"column":4,"row":2},{"column":4,"row":3}],"operator":"add","target":12},
      {"cells":[{"column":0,"row":3},{"column":1,"row":3}],"operator":"multiply","target":12},
      {"cells":[{"column":2,"row":3}],"operator":"given","target":2},
      {"cells":[{"column":3,"row":3},{"column":3,"row":4},{"column":4,"row":4}],"operator":"add","target":6},
      {"cells":[{"column":0,"row":4},{"column":1,"row":4}],"operator":"add","target":6},
      {"cells":[{"column":2,"row":4}],"operator":"given","target":4}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-5x5-a1d7293f722f81fb",
    "size": 5,
    "provenance": {"accepted_attempt":66,"generator_version":"0.3.0","profile":"medium","seed":"2026072701"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":0,"row":1},{"column":1,"row":1},{"column":2,"row":1}],"operator":"add","target":9},
      {"cells":[{"column":1,"row":0}],"operator":"given","target":5},
      {"cells":[{"column":2,"row":0},{"column":3,"row":0},{"column":3,"row":1}],"operator":"add","target":9},
      {"cells":[{"column":4,"row":0},{"column":4,"row":1},{"column":4,"row":2}],"operator":"multiply","target":10},
      {"cells":[{"column":0,"row":2},{"column":0,"row":3}],"operator":"subtract","target":1},
      {"cells":[{"column":1,"row":2},{"column":1,"row":3}],"operator":"subtract","target":1},
      {"cells":[{"column":2,"row":2},{"column":2,"row":3}],"operator":"subtract","target":3},
      {"cells":[{"column":3,"row":2},{"column":3,"row":3},{"column":3,"row":4}],"operator":"multiply","target":20},
      {"cells":[{"column":4,"row":3},{"column":4,"row":4}],"operator":"multiply","target":12},
      {"cells":[{"column":0,"row":4}],"operator":"given","target":5},
      {"cells":[{"column":1,"row":4},{"column":2,"row":4}],"operator":"divide","target":2}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-5x5-5b00d6b1c7a0b5ec",
    "size": 5,
    "provenance": {"accepted_attempt":342,"generator_version":"0.3.0","profile":"hard","seed":"2026072701"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":1,"row":0},{"column":0,"row":1},{"column":1,"row":1}],"operator":"multiply","target":30},
      {"cells":[{"column":2,"row":0},{"column":3,"row":0},{"column":4,"row":0},{"column":3,"row":1}],"operator":"add","target":13},
      {"cells":[{"column":2,"row":1},{"column":2,"row":2}],"operator":"subtract","target":1},
      {"cells":[{"column":4,"row":1},{"column":3,"row":2},{"column":4,"row":2}],"operator":"multiply","target":15},
      {"cells":[{"column":0,"row":2},{"column":0,"row":3},{"column":0,"row":4},{"column":1,"row":4}],"operator":"add","target":13},
      {"cells":[{"column":1,"row":2}],"operator":"given","target":2},
      {"cells":[{"column":1,"row":3},{"column":2,"row":3},{"column":3,"row":3}],"operator":"multiply","target":20},
      {"cells":[{"column":4,"row":3},{"column":2,"row":4},{"column":3,"row":4},{"column":4,"row":4}],"operator":"multiply","target":12}
    ]
  },
  // Additional original records, grouped by size and difficulty.
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-4x4-de6ac2e5846ea9ca",
    "size": 4,
    "provenance": {"accepted_attempt":1,"generator_version":"0.3.0","profile":"easy","seed":"2026081106"},
    "cages": [
      {"cells":[{"column":0,"row":0}],"operator":"given","target":2},
      {"cells":[{"column":1,"row":0},{"column":2,"row":0}],"operator":"add","target":4},
      {"cells":[{"column":3,"row":0},{"column":3,"row":1}],"operator":"multiply","target":4},
      {"cells":[{"column":0,"row":1},{"column":1,"row":1},{"column":1,"row":2}],"operator":"add","target":11},
      {"cells":[{"column":2,"row":1}],"operator":"given","target":2},
      {"cells":[{"column":0,"row":2},{"column":0,"row":3}],"operator":"subtract","target":2},
      {"cells":[{"column":2,"row":2},{"column":3,"row":2}],"operator":"subtract","target":1},
      {"cells":[{"column":1,"row":3}],"operator":"given","target":2},
      {"cells":[{"column":2,"row":3},{"column":3,"row":3}],"operator":"add","target":7}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-4x4-640868c3b5fb1c49",
    "size": 4,
    "provenance": {"accepted_attempt":1,"generator_version":"0.3.0","profile":"easy","seed":"2026081107"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":1,"row":0}],"operator":"add","target":3},
      {"cells":[{"column":2,"row":0},{"column":1,"row":1},{"column":2,"row":1}],"operator":"add","target":9},
      {"cells":[{"column":3,"row":0}],"operator":"given","target":3},
      {"cells":[{"column":0,"row":1},{"column":0,"row":2}],"operator":"divide","target":3},
      {"cells":[{"column":3,"row":1}],"operator":"given","target":2},
      {"cells":[{"column":1,"row":2},{"column":1,"row":3}],"operator":"multiply","target":6},
      {"cells":[{"column":2,"row":2},{"column":3,"row":2}],"operator":"add","target":6},
      {"cells":[{"column":0,"row":3}],"operator":"given","target":4},
      {"cells":[{"column":2,"row":3},{"column":3,"row":3}],"operator":"subtract","target":2}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-4x4-0f4ad6c8a3788562",
    "size": 4,
    "provenance": {"accepted_attempt":1,"generator_version":"0.3.0","profile":"easy","seed":"2026081108"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":0,"row":1}],"operator":"subtract","target":2},
      {"cells":[{"column":1,"row":0},{"column":1,"row":1}],"operator":"divide","target":2},
      {"cells":[{"column":2,"row":0}],"operator":"given","target":3},
      {"cells":[{"column":3,"row":0}],"operator":"given","target":4},
      {"cells":[{"column":2,"row":1},{"column":3,"row":1}],"operator":"multiply","target":3},
      {"cells":[{"column":0,"row":2},{"column":0,"row":3}],"operator":"divide","target":3},
      {"cells":[{"column":1,"row":2},{"column":1,"row":3}],"operator":"subtract","target":1},
      {"cells":[{"column":2,"row":2},{"column":3,"row":2}],"operator":"subtract","target":2},
      {"cells":[{"column":2,"row":3},{"column":3,"row":3}],"operator":"subtract","target":1}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-4x4-dc2d47e816d3bb02",
    "size": 4,
    "provenance": {"accepted_attempt":1,"generator_version":"0.3.0","profile":"easy","seed":"2026081201"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":0,"row":1}],"operator":"divide","target":2},
      {"cells":[{"column":1,"row":0},{"column":2,"row":0},{"column":1,"row":1}],"operator":"add","target":10},
      {"cells":[{"column":3,"row":0},{"column":3,"row":1}],"operator":"subtract","target":1},
      {"cells":[{"column":2,"row":1}],"operator":"given","target":1},
      {"cells":[{"column":0,"row":2},{"column":0,"row":3}],"operator":"subtract","target":2},
      {"cells":[{"column":1,"row":2},{"column":2,"row":2}],"operator":"subtract","target":2},
      {"cells":[{"column":3,"row":2},{"column":2,"row":3},{"column":3,"row":3}],"operator":"add","target":9},
      {"cells":[{"column":1,"row":3}],"operator":"given","target":1}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-4x4-c74849710dfdf177",
    "size": 4,
    "provenance": {"accepted_attempt":2,"generator_version":"0.3.0","profile":"easy","seed":"2026081202"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":0,"row":1},{"column":1,"row":1}],"operator":"add","target":6},
      {"cells":[{"column":1,"row":0},{"column":2,"row":0}],"operator":"add","target":3},
      {"cells":[{"column":3,"row":0},{"column":3,"row":1}],"operator":"subtract","target":1},
      {"cells":[{"column":2,"row":1}],"operator":"given","target":4},
      {"cells":[{"column":0,"row":2}],"operator":"given","target":4},
      {"cells":[{"column":1,"row":2},{"column":2,"row":2}],"operator":"add","target":4},
      {"cells":[{"column":3,"row":2},{"column":2,"row":3},{"column":3,"row":3}],"operator":"add","target":6},
      {"cells":[{"column":0,"row":3},{"column":1,"row":3}],"operator":"divide","target":2}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-4x4-f36bf2187c5f7386",
    "size": 4,
    "provenance": {"accepted_attempt":1,"generator_version":"0.3.0","profile":"easy","seed":"2026081203"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":1,"row":0},{"column":2,"row":0}],"operator":"add","target":6},
      {"cells":[{"column":3,"row":0},{"column":3,"row":1}],"operator":"divide","target":2},
      {"cells":[{"column":0,"row":1},{"column":0,"row":2}],"operator":"multiply","target":8},
      {"cells":[{"column":1,"row":1},{"column":1,"row":2}],"operator":"divide","target":4},
      {"cells":[{"column":2,"row":1}],"operator":"given","target":3},
      {"cells":[{"column":2,"row":2},{"column":3,"row":2}],"operator":"subtract","target":2},
      {"cells":[{"column":0,"row":3}],"operator":"given","target":3},
      {"cells":[{"column":1,"row":3},{"column":2,"row":3},{"column":3,"row":3}],"operator":"add","target":7}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-4x4-02785319ef2b089a",
    "size": 4,
    "provenance": {"accepted_attempt":1,"generator_version":"0.3.0","profile":"easy","seed":"2026081204"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":1,"row":0},{"column":0,"row":1}],"operator":"add","target":7},
      {"cells":[{"column":2,"row":0},{"column":3,"row":0}],"operator":"add","target":5},
      {"cells":[{"column":1,"row":1},{"column":2,"row":1},{"column":2,"row":2}],"operator":"add","target":8},
      {"cells":[{"column":3,"row":1},{"column":3,"row":2}],"operator":"multiply","target":12},
      {"cells":[{"column":0,"row":2},{"column":0,"row":3}],"operator":"subtract","target":2},
      {"cells":[{"column":1,"row":2},{"column":1,"row":3},{"column":2,"row":3}],"operator":"add","target":8},
      {"cells":[{"column":3,"row":3}],"operator":"given","target":1}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-4x4-ff0a6cd4774f3373",
    "size": 4,
    "provenance": {"accepted_attempt":3,"generator_version":"0.3.0","profile":"easy","seed":"2026081205"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":0,"row":1}],"operator":"divide","target":4},
      {"cells":[{"column":1,"row":0},{"column":2,"row":0}],"operator":"multiply","target":12},
      {"cells":[{"column":3,"row":0},{"column":2,"row":1},{"column":3,"row":1}],"operator":"add","target":6},
      {"cells":[{"column":1,"row":1},{"column":1,"row":2}],"operator":"subtract","target":1},
      {"cells":[{"column":0,"row":2}],"operator":"given","target":3},
      {"cells":[{"column":2,"row":2},{"column":3,"row":2},{"column":2,"row":3}],"operator":"add","target":10},
      {"cells":[{"column":0,"row":3},{"column":1,"row":3}],"operator":"subtract","target":1},
      {"cells":[{"column":3,"row":3}],"operator":"given","target":1}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-4x4-25237adc993291aa",
    "size": 4,
    "provenance": {"accepted_attempt":1,"generator_version":"0.3.0","profile":"easy","seed":"2026081206"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":1,"row":0}],"operator":"divide","target":2},
      {"cells":[{"column":2,"row":0},{"column":3,"row":0}],"operator":"subtract","target":1},
      {"cells":[{"column":0,"row":1}],"operator":"given","target":1},
      {"cells":[{"column":1,"row":1}],"operator":"given","target":3},
      {"cells":[{"column":2,"row":1},{"column":3,"row":1},{"column":2,"row":2}],"operator":"add","target":8},
      {"cells":[{"column":0,"row":2},{"column":1,"row":2},{"column":1,"row":3}],"operator":"add","target":9},
      {"cells":[{"column":3,"row":2},{"column":2,"row":3},{"column":3,"row":3}],"operator":"add","target":5},
      {"cells":[{"column":0,"row":3}],"operator":"given","target":4}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-4x4-2f2617d404e4fcce",
    "size": 4,
    "provenance": {"accepted_attempt":1,"generator_version":"0.3.0","profile":"easy","seed":"2026081207"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":1,"row":0}],"operator":"multiply","target":6},
      {"cells":[{"column":2,"row":0},{"column":3,"row":0},{"column":3,"row":1}],"operator":"add","target":9},
      {"cells":[{"column":0,"row":1},{"column":0,"row":2},{"column":0,"row":3}],"operator":"add","target":7},
      {"cells":[{"column":1,"row":1},{"column":2,"row":1}],"operator":"subtract","target":1},
      {"cells":[{"column":1,"row":2}],"operator":"given","target":4},
      {"cells":[{"column":2,"row":2}],"operator":"given","target":1},
      {"cells":[{"column":3,"row":2}],"operator":"given","target":3},
      {"cells":[{"column":1,"row":3},{"column":2,"row":3},{"column":3,"row":3}],"operator":"add","target":6}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-4x4-6c7f7691bb7af035",
    "size": 4,
    "provenance": {"accepted_attempt":1,"generator_version":"0.3.0","profile":"easy","seed":"2026081208"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":0,"row":1}],"operator":"divide","target":2},
      {"cells":[{"column":1,"row":0},{"column":2,"row":0},{"column":1,"row":1}],"operator":"add","target":8},
      {"cells":[{"column":3,"row":0},{"column":2,"row":1},{"column":3,"row":1}],"operator":"add","target":6},
      {"cells":[{"column":0,"row":2}],"operator":"given","target":1},
      {"cells":[{"column":1,"row":2},{"column":0,"row":3},{"column":1,"row":3}],"operator":"add","target":8},
      {"cells":[{"column":2,"row":2},{"column":2,"row":3},{"column":3,"row":3}],"operator":"add","target":9},
      {"cells":[{"column":3,"row":2}],"operator":"given","target":2}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-4x4-2ec9ca0528bc8c69",
    "size": 4,
    "provenance": {"accepted_attempt":410,"generator_version":"0.3.0","profile":"medium","seed":"2026081002"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":1,"row":0},{"column":0,"row":1},{"column":1,"row":1}],"operator":"add","target":9},
      {"cells":[{"column":2,"row":0}],"operator":"given","target":1},
      {"cells":[{"column":3,"row":0},{"column":2,"row":1},{"column":3,"row":1}],"operator":"add","target":10},
      {"cells":[{"column":0,"row":2},{"column":0,"row":3},{"column":1,"row":3}],"operator":"add","target":9},
      {"cells":[{"column":1,"row":2},{"column":2,"row":2},{"column":2,"row":3}],"operator":"add","target":7},
      {"cells":[{"column":3,"row":2},{"column":3,"row":3}],"operator":"subtract","target":2}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-4x4-d941dcb026d3ff24",
    "size": 4,
    "provenance": {"accepted_attempt":5,"generator_version":"0.3.0","profile":"medium","seed":"2026081003"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":1,"row":0},{"column":2,"row":0},{"column":1,"row":1}],"operator":"add","target":9},
      {"cells":[{"column":3,"row":0},{"column":3,"row":1}],"operator":"subtract","target":1},
      {"cells":[{"column":0,"row":1},{"column":0,"row":2},{"column":0,"row":3}],"operator":"add","target":7},
      {"cells":[{"column":2,"row":1}],"operator":"given","target":4},
      {"cells":[{"column":1,"row":2},{"column":2,"row":2},{"column":3,"row":2},{"column":1,"row":3}],"operator":"multiply","target":48},
      {"cells":[{"column":2,"row":3},{"column":3,"row":3}],"operator":"add","target":4}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-4x4-99d21f395f943441",
    "size": 4,
    "provenance": {"accepted_attempt":356,"generator_version":"0.3.0","profile":"medium","seed":"2026081004"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":0,"row":1},{"column":0,"row":2},{"column":0,"row":3}],"operator":"add","target":10},
      {"cells":[{"column":1,"row":0},{"column":1,"row":1},{"column":1,"row":2}],"operator":"add","target":6},
      {"cells":[{"column":2,"row":0},{"column":3,"row":0}],"operator":"subtract","target":1},
      {"cells":[{"column":2,"row":1},{"column":3,"row":1}],"operator":"multiply","target":8},
      {"cells":[{"column":2,"row":2}],"operator":"given","target":1},
      {"cells":[{"column":3,"row":2},{"column":3,"row":3}],"operator":"add","target":5},
      {"cells":[{"column":1,"row":3},{"column":2,"row":3}],"operator":"multiply","target":12}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-4x4-af2862f41107ed28",
    "size": 4,
    "provenance": {"accepted_attempt":225,"generator_version":"0.3.0","profile":"medium","seed":"2026081101"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":0,"row":1},{"column":1,"row":1}],"operator":"multiply","target":12},
      {"cells":[{"column":1,"row":0},{"column":2,"row":0}],"operator":"divide","target":4},
      {"cells":[{"column":3,"row":0},{"column":3,"row":1},{"column":3,"row":2}],"operator":"multiply","target":6},
      {"cells":[{"column":2,"row":1},{"column":2,"row":2}],"operator":"subtract","target":1},
      {"cells":[{"column":0,"row":2},{"column":1,"row":2}],"operator":"multiply","target":8},
      {"cells":[{"column":0,"row":3},{"column":1,"row":3},{"column":2,"row":3}],"operator":"multiply","target":6},
      {"cells":[{"column":3,"row":3}],"operator":"given","target":4}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-4x4-15cb63b7311acea1",
    "size": 4,
    "provenance": {"accepted_attempt":2,"generator_version":"0.3.0","profile":"medium","seed":"2026081102"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":1,"row":0},{"column":0,"row":1},{"column":0,"row":2}],"operator":"multiply","target":24},
      {"cells":[{"column":2,"row":0},{"column":3,"row":0},{"column":3,"row":1}],"operator":"multiply","target":12},
      {"cells":[{"column":1,"row":1},{"column":2,"row":1}],"operator":"divide","target":4},
      {"cells":[{"column":1,"row":2},{"column":0,"row":3},{"column":1,"row":3}],"operator":"multiply","target":6},
      {"cells":[{"column":2,"row":2},{"column":3,"row":2}],"operator":"add","target":5},
      {"cells":[{"column":2,"row":3},{"column":3,"row":3}],"operator":"multiply","target":12}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-4x4-a200db5f33fea950",
    "size": 4,
    "provenance": {"accepted_attempt":23,"generator_version":"0.3.0","profile":"medium","seed":"2026081103"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":1,"row":0}],"operator":"add","target":5},
      {"cells":[{"column":2,"row":0},{"column":3,"row":0},{"column":3,"row":1}],"operator":"multiply","target":8},
      {"cells":[{"column":0,"row":1},{"column":0,"row":2}],"operator":"multiply","target":3},
      {"cells":[{"column":1,"row":1},{"column":2,"row":1},{"column":1,"row":2}],"operator":"add","target":9},
      {"cells":[{"column":2,"row":2},{"column":3,"row":2},{"column":2,"row":3},{"column":3,"row":3}],"operator":"add","target":9},
      {"cells":[{"column":0,"row":3},{"column":1,"row":3}],"operator":"add","target":6}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-4x4-ed0b23d00bc5593b",
    "size": 4,
    "provenance": {"accepted_attempt":118,"generator_version":"0.3.0","profile":"medium","seed":"2026081104"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":1,"row":0},{"column":0,"row":1}],"operator":"add","target":9},
      {"cells":[{"column":2,"row":0},{"column":3,"row":0},{"column":3,"row":1}],"operator":"add","target":6},
      {"cells":[{"column":1,"row":1},{"column":1,"row":2}],"operator":"subtract","target":2},
      {"cells":[{"column":2,"row":1},{"column":2,"row":2}],"operator":"divide","target":2},
      {"cells":[{"column":0,"row":2},{"column":0,"row":3},{"column":1,"row":3},{"column":2,"row":3}],"operator":"multiply","target":24},
      {"cells":[{"column":3,"row":2},{"column":3,"row":3}],"operator":"subtract","target":1}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-4x4-77f7936595c224ad",
    "size": 4,
    "provenance": {"accepted_attempt":40,"generator_version":"0.3.0","profile":"medium","seed":"2026081201"},
    "cages": [
      {"cells":[{"column":0,"row":0}],"operator":"given","target":4},
      {"cells":[{"column":1,"row":0},{"column":2,"row":0},{"column":1,"row":1}],"operator":"multiply","target":12},
      {"cells":[{"column":3,"row":0},{"column":2,"row":1},{"column":3,"row":1}],"operator":"multiply","target":12},
      {"cells":[{"column":0,"row":1},{"column":0,"row":2}],"operator":"add","target":3},
      {"cells":[{"column":1,"row":2},{"column":0,"row":3},{"column":1,"row":3}],"operator":"add","target":8},
      {"cells":[{"column":2,"row":2},{"column":3,"row":2}],"operator":"subtract","target":2},
      {"cells":[{"column":2,"row":3},{"column":3,"row":3}],"operator":"divide","target":2}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-4x4-956f6d4e64805b3d",
    "size": 4,
    "provenance": {"accepted_attempt":19,"generator_version":"0.3.0","profile":"medium","seed":"2026081202"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":0,"row":1},{"column":0,"row":2}],"operator":"add","target":7},
      {"cells":[{"column":1,"row":0}],"operator":"given","target":3},
      {"cells":[{"column":2,"row":0},{"column":3,"row":0},{"column":3,"row":1},{"column":3,"row":2}],"operator":"add","target":8},
      {"cells":[{"column":1,"row":1},{"column":2,"row":1}],"operator":"subtract","target":1},
      {"cells":[{"column":1,"row":2},{"column":2,"row":2}],"operator":"add","target":5},
      {"cells":[{"column":0,"row":3}],"operator":"given","target":3},
      {"cells":[{"column":1,"row":3},{"column":2,"row":3},{"column":3,"row":3}],"operator":"multiply","target":8}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-4x4-dd0f379f92bf3359",
    "size": 4,
    "provenance": {"accepted_attempt":41,"generator_version":"0.3.0","profile":"medium","seed":"2026081203"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":0,"row":1},{"column":1,"row":1}],"operator":"multiply","target":6},
      {"cells":[{"column":1,"row":0},{"column":2,"row":0}],"operator":"add","target":5},
      {"cells":[{"column":3,"row":0},{"column":3,"row":1},{"column":3,"row":2}],"operator":"multiply","target":8},
      {"cells":[{"column":2,"row":1},{"column":1,"row":2},{"column":2,"row":2}],"operator":"multiply","target":12},
      {"cells":[{"column":0,"row":2},{"column":0,"row":3},{"column":1,"row":3},{"column":2,"row":3}],"operator":"add","target":11},
      {"cells":[{"column":3,"row":3}],"operator":"given","target":3}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-4x4-6424d50eb47d1f81",
    "size": 4,
    "provenance": {"accepted_attempt":51,"generator_version":"0.3.0","profile":"medium","seed":"2026081204"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":1,"row":0},{"column":2,"row":0},{"column":0,"row":1}],"operator":"add","target":12},
      {"cells":[{"column":3,"row":0},{"column":3,"row":1}],"operator":"subtract","target":1},
      {"cells":[{"column":1,"row":1},{"column":2,"row":1},{"column":2,"row":2}],"operator":"add","target":7},
      {"cells":[{"column":0,"row":2},{"column":1,"row":2}],"operator":"multiply","target":6},
      {"cells":[{"column":3,"row":2},{"column":2,"row":3},{"column":3,"row":3}],"operator":"add","target":8},
      {"cells":[{"column":0,"row":3},{"column":1,"row":3}],"operator":"subtract","target":1}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-4x4-302367e796b99402",
    "size": 4,
    "provenance": {"accepted_attempt":820,"generator_version":"0.3.0","profile":"hard","seed":"2026081004"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":1,"row":0},{"column":0,"row":1}],"operator":"add","target":6},
      {"cells":[{"column":2,"row":0},{"column":3,"row":0},{"column":3,"row":1}],"operator":"add","target":9},
      {"cells":[{"column":1,"row":1},{"column":2,"row":1},{"column":1,"row":2},{"column":2,"row":2}],"operator":"add","target":12},
      {"cells":[{"column":0,"row":2},{"column":0,"row":3}],"operator":"add","target":5},
      {"cells":[{"column":3,"row":2},{"column":3,"row":3}],"operator":"multiply","target":2},
      {"cells":[{"column":1,"row":3},{"column":2,"row":3}],"operator":"subtract","target":1}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-4x4-cc7cfc5d570995fb",
    "size": 4,
    "provenance": {"accepted_attempt":999,"generator_version":"0.3.0","profile":"hard","seed":"2026081009"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":0,"row":1}],"operator":"divide","target":2},
      {"cells":[{"column":1,"row":0},{"column":2,"row":0},{"column":1,"row":1},{"column":1,"row":2}],"operator":"add","target":10},
      {"cells":[{"column":3,"row":0},{"column":2,"row":1},{"column":3,"row":1},{"column":2,"row":2}],"operator":"multiply","target":24},
      {"cells":[{"column":0,"row":2},{"column":0,"row":3},{"column":1,"row":3},{"column":2,"row":3}],"operator":"multiply","target":48},
      {"cells":[{"column":3,"row":2},{"column":3,"row":3}],"operator":"subtract","target":1}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-4x4-f148c88cc4bab73c",
    "size": 4,
    "provenance": {"accepted_attempt":635,"generator_version":"0.3.0","profile":"hard","seed":"2026081011"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":1,"row":0}],"operator":"add","target":6},
      {"cells":[{"column":2,"row":0},{"column":3,"row":0}],"operator":"divide","target":3},
      {"cells":[{"column":0,"row":1},{"column":1,"row":1}],"operator":"add","target":5},
      {"cells":[{"column":2,"row":1},{"column":2,"row":2},{"column":2,"row":3},{"column":3,"row":3}],"operator":"add","target":11},
      {"cells":[{"column":3,"row":1},{"column":3,"row":2}],"operator":"add","target":5},
      {"cells":[{"column":0,"row":2},{"column":1,"row":2},{"column":0,"row":3}],"operator":"add","target":6},
      {"cells":[{"column":1,"row":3}],"operator":"given","target":3}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-4x4-dd93e479e0d86e07",
    "size": 4,
    "provenance": {"accepted_attempt":1808,"generator_version":"0.3.0","profile":"hard","seed":"2026081101"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":1,"row":0},{"column":2,"row":0},{"column":3,"row":0}],"operator":"multiply","target":24},
      {"cells":[{"column":0,"row":1},{"column":1,"row":1},{"column":2,"row":1}],"operator":"multiply","target":6},
      {"cells":[{"column":3,"row":1},{"column":3,"row":2},{"column":3,"row":3}],"operator":"multiply","target":12},
      {"cells":[{"column":0,"row":2},{"column":1,"row":2},{"column":1,"row":3}],"operator":"add","target":9},
      {"cells":[{"column":2,"row":2},{"column":2,"row":3}],"operator":"subtract","target":1},
      {"cells":[{"column":0,"row":3}],"operator":"given","target":2}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-4x4-71531cb5b3ca97ad",
    "size": 4,
    "provenance": {"accepted_attempt":1569,"generator_version":"0.3.0","profile":"hard","seed":"2026081107"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":1,"row":0}],"operator":"subtract","target":1},
      {"cells":[{"column":2,"row":0},{"column":3,"row":0},{"column":2,"row":1}],"operator":"add","target":8},
      {"cells":[{"column":0,"row":1},{"column":1,"row":1}],"operator":"divide","target":4},
      {"cells":[{"column":3,"row":1},{"column":2,"row":2},{"column":3,"row":2},{"column":3,"row":3}],"operator":"multiply","target":48},
      {"cells":[{"column":0,"row":2},{"column":0,"row":3},{"column":1,"row":3},{"column":2,"row":3}],"operator":"add","target":8},
      {"cells":[{"column":1,"row":2}],"operator":"given","target":3}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-4x4-d3f92a65542bc39e",
    "size": 4,
    "provenance": {"accepted_attempt":945,"generator_version":"0.3.0","profile":"hard","seed":"2026081109"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":0,"row":1},{"column":1,"row":1},{"column":2,"row":1}],"operator":"multiply","target":32},
      {"cells":[{"column":1,"row":0}],"operator":"given","target":3},
      {"cells":[{"column":2,"row":0},{"column":3,"row":0},{"column":3,"row":1}],"operator":"multiply","target":6},
      {"cells":[{"column":0,"row":2},{"column":1,"row":2}],"operator":"subtract","target":1},
      {"cells":[{"column":2,"row":2},{"column":0,"row":3},{"column":1,"row":3},{"column":2,"row":3}],"operator":"add","target":9},
      {"cells":[{"column":3,"row":2},{"column":3,"row":3}],"operator":"multiply","target":8}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-4x4-d89b6416c2106de8",
    "size": 4,
    "provenance": {"accepted_attempt":40,"generator_version":"0.3.0","profile":"hard","seed":"2026081114"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":0,"row":1}],"operator":"subtract","target":1},
      {"cells":[{"column":1,"row":0},{"column":1,"row":1},{"column":0,"row":2},{"column":1,"row":2}],"operator":"multiply","target":24},
      {"cells":[{"column":2,"row":0},{"column":3,"row":0},{"column":3,"row":1},{"column":3,"row":2}],"operator":"multiply","target":8},
      {"cells":[{"column":2,"row":1}],"operator":"given","target":3},
      {"cells":[{"column":2,"row":2},{"column":2,"row":3},{"column":3,"row":3}],"operator":"multiply","target":24},
      {"cells":[{"column":0,"row":3},{"column":1,"row":3}],"operator":"divide","target":2}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-4x4-8e937083fa6d7c68",
    "size": 4,
    "provenance": {"accepted_attempt":1225,"generator_version":"0.3.0","profile":"hard","seed":"2026081204"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":0,"row":1}],"operator":"subtract","target":3},
      {"cells":[{"column":1,"row":0},{"column":1,"row":1}],"operator":"subtract","target":1},
      {"cells":[{"column":2,"row":0},{"column":3,"row":0},{"column":2,"row":1}],"operator":"add","target":9},
      {"cells":[{"column":3,"row":1},{"column":3,"row":2},{"column":2,"row":3},{"column":3,"row":3}],"operator":"multiply","target":24},
      {"cells":[{"column":0,"row":2},{"column":1,"row":2},{"column":2,"row":2},{"column":1,"row":3}],"operator":"add","target":10},
      {"cells":[{"column":0,"row":3}],"operator":"given","target":3}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-4x4-9853098e471119ad",
    "size": 4,
    "provenance": {"accepted_attempt":1972,"generator_version":"0.3.0","profile":"hard","seed":"2026081208"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":0,"row":1},{"column":0,"row":2}],"operator":"add","target":9},
      {"cells":[{"column":1,"row":0},{"column":1,"row":1}],"operator":"subtract","target":1},
      {"cells":[{"column":2,"row":0},{"column":3,"row":0},{"column":2,"row":1}],"operator":"add","target":7},
      {"cells":[{"column":3,"row":1},{"column":2,"row":2},{"column":3,"row":2},{"column":3,"row":3}],"operator":"multiply","target":24},
      {"cells":[{"column":1,"row":2},{"column":0,"row":3},{"column":1,"row":3},{"column":2,"row":3}],"operator":"add","target":9}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-4x4-9c02ab43eac25bbe",
    "size": 4,
    "provenance": {"accepted_attempt":1438,"generator_version":"0.3.0","profile":"hard","seed":"2026081213"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":1,"row":0},{"column":2,"row":0}],"operator":"add","target":6},
      {"cells":[{"column":3,"row":0}],"operator":"given","target":4},
      {"cells":[{"column":0,"row":1},{"column":1,"row":1}],"operator":"multiply","target":4},
      {"cells":[{"column":2,"row":1},{"column":3,"row":1}],"operator":"subtract","target":1},
      {"cells":[{"column":0,"row":2},{"column":1,"row":2},{"column":2,"row":2},{"column":0,"row":3}],"operator":"add","target":12},
      {"cells":[{"column":3,"row":2},{"column":1,"row":3},{"column":2,"row":3},{"column":3,"row":3}],"operator":"multiply","target":12}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-4x4-46004877ecc0aca9",
    "size": 4,
    "provenance": {"accepted_attempt":1460,"generator_version":"0.3.0","profile":"hard","seed":"2026081214"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":1,"row":0}],"operator":"subtract","target":2},
      {"cells":[{"column":2,"row":0},{"column":3,"row":0},{"column":1,"row":1},{"column":2,"row":1}],"operator":"add","target":8},
      {"cells":[{"column":0,"row":1},{"column":0,"row":2},{"column":0,"row":3},{"column":1,"row":3}],"operator":"add","target":11},
      {"cells":[{"column":3,"row":1},{"column":3,"row":2},{"column":2,"row":3},{"column":3,"row":3}],"operator":"add","target":9},
      {"cells":[{"column":1,"row":2},{"column":2,"row":2}],"operator":"multiply","target":8}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-5x5-3021ea1914279046",
    "size": 5,
    "provenance": {"accepted_attempt":3,"generator_version":"0.3.0","profile":"easy","seed":"2026081002"},
    "cages": [
      {"cells":[{"column":0,"row":0}],"operator":"given","target":4},
      {"cells":[{"column":1,"row":0},{"column":2,"row":0},{"column":3,"row":0}],"operator":"add","target":8},
      {"cells":[{"column":4,"row":0},{"column":3,"row":1},{"column":4,"row":1}],"operator":"add","target":10},
      {"cells":[{"column":0,"row":1},{"column":0,"row":2}],"operator":"multiply","target":6},
      {"cells":[{"column":1,"row":1},{"column":2,"row":1},{"column":2,"row":2}],"operator":"add","target":9},
      {"cells":[{"column":1,"row":2}],"operator":"given","target":3},
      {"cells":[{"column":3,"row":2}],"operator":"given","target":1},
      {"cells":[{"column":4,"row":2},{"column":4,"row":3}],"operator":"subtract","target":4},
      {"cells":[{"column":0,"row":3},{"column":1,"row":3}],"operator":"subtract","target":3},
      {"cells":[{"column":2,"row":3},{"column":2,"row":4}],"operator":"multiply","target":6},
      {"cells":[{"column":3,"row":3},{"column":3,"row":4}],"operator":"subtract","target":1},
      {"cells":[{"column":0,"row":4},{"column":1,"row":4}],"operator":"divide","target":5},
      {"cells":[{"column":4,"row":4}],"operator":"given","target":4}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-5x5-5de30732d47f38ce",
    "size": 5,
    "provenance": {"accepted_attempt":9,"generator_version":"0.3.0","profile":"easy","seed":"2026081003"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":1,"row":0}],"operator":"add","target":6},
      {"cells":[{"column":2,"row":0}],"operator":"given","target":3},
      {"cells":[{"column":3,"row":0},{"column":4,"row":0}],"operator":"divide","target":5},
      {"cells":[{"column":0,"row":1}],"operator":"given","target":5},
      {"cells":[{"column":1,"row":1},{"column":2,"row":1}],"operator":"divide","target":4},
      {"cells":[{"column":3,"row":1},{"column":2,"row":2},{"column":3,"row":2}],"operator":"add","target":8},
      {"cells":[{"column":4,"row":1},{"column":4,"row":2}],"operator":"subtract","target":1},
      {"cells":[{"column":0,"row":2},{"column":1,"row":2},{"column":1,"row":3}],"operator":"add","target":10},
      {"cells":[{"column":0,"row":3},{"column":0,"row":4}],"operator":"subtract","target":3},
      {"cells":[{"column":2,"row":3},{"column":2,"row":4}],"operator":"subtract","target":3},
      {"cells":[{"column":3,"row":3},{"column":3,"row":4}],"operator":"multiply","target":12},
      {"cells":[{"column":4,"row":3},{"column":4,"row":4}],"operator":"subtract","target":1},
      {"cells":[{"column":1,"row":4}],"operator":"given","target":3}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-5x5-ab6a60835d96a5ea",
    "size": 5,
    "provenance": {"accepted_attempt":6,"generator_version":"0.3.0","profile":"easy","seed":"2026081004"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":0,"row":1}],"operator":"subtract","target":1},
      {"cells":[{"column":1,"row":0}],"operator":"given","target":2},
      {"cells":[{"column":2,"row":0},{"column":3,"row":0},{"column":3,"row":1}],"operator":"add","target":8},
      {"cells":[{"column":4,"row":0},{"column":4,"row":1}],"operator":"subtract","target":2},
      {"cells":[{"column":1,"row":1},{"column":2,"row":1}],"operator":"multiply","target":10},
      {"cells":[{"column":0,"row":2},{"column":0,"row":3},{"column":1,"row":3}],"operator":"add","target":9},
      {"cells":[{"column":1,"row":2}],"operator":"given","target":1},
      {"cells":[{"column":2,"row":2},{"column":3,"row":2},{"column":4,"row":2}],"operator":"add","target":12},
      {"cells":[{"column":2,"row":3},{"column":2,"row":4}],"operator":"subtract","target":1},
      {"cells":[{"column":3,"row":3},{"column":3,"row":4}],"operator":"multiply","target":2},
      {"cells":[{"column":4,"row":3},{"column":4,"row":4}],"operator":"multiply","target":10},
      {"cells":[{"column":0,"row":4},{"column":1,"row":4}],"operator":"subtract","target":2}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-5x5-4afe5a6637d1f6d7",
    "size": 5,
    "provenance": {"accepted_attempt":1,"generator_version":"0.3.0","profile":"easy","seed":"2026081101"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":0,"row":1}],"operator":"divide","target":2},
      {"cells":[{"column":1,"row":0},{"column":1,"row":1}],"operator":"subtract","target":4},
      {"cells":[{"column":2,"row":0}],"operator":"given","target":2},
      {"cells":[{"column":3,"row":0},{"column":4,"row":0},{"column":4,"row":1}],"operator":"add","target":11},
      {"cells":[{"column":2,"row":1},{"column":3,"row":1}],"operator":"divide","target":4},
      {"cells":[{"column":0,"row":2},{"column":1,"row":2},{"column":1,"row":3}],"operator":"add","target":8},
      {"cells":[{"column":2,"row":2}],"operator":"given","target":4},
      {"cells":[{"column":3,"row":2},{"column":3,"row":3}],"operator":"add","target":7},
      {"cells":[{"column":4,"row":2},{"column":4,"row":3},{"column":4,"row":4}],"operator":"add","target":7},
      {"cells":[{"column":0,"row":3},{"column":0,"row":4}],"operator":"divide","target":5},
      {"cells":[{"column":2,"row":3}],"operator":"given","target":5},
      {"cells":[{"column":1,"row":4},{"column":2,"row":4}],"operator":"multiply","target":12},
      {"cells":[{"column":3,"row":4}],"operator":"given","target":1}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-5x5-e307a5699cf03215",
    "size": 5,
    "provenance": {"accepted_attempt":1,"generator_version":"0.3.0","profile":"easy","seed":"2026081102"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":0,"row":1}],"operator":"add","target":6},
      {"cells":[{"column":1,"row":0},{"column":2,"row":0},{"column":2,"row":1}],"operator":"add","target":9},
      {"cells":[{"column":3,"row":0},{"column":3,"row":1}],"operator":"add","target":8},
      {"cells":[{"column":4,"row":0},{"column":4,"row":1}],"operator":"multiply","target":2},
      {"cells":[{"column":1,"row":1},{"column":1,"row":2}],"operator":"multiply","target":4},
      {"cells":[{"column":0,"row":2}],"operator":"given","target":4},
      {"cells":[{"column":2,"row":2},{"column":3,"row":2},{"column":4,"row":2}],"operator":"add","target":10},
      {"cells":[{"column":0,"row":3}],"operator":"given","target":2},
      {"cells":[{"column":1,"row":3},{"column":2,"row":3}],"operator":"add","target":8},
      {"cells":[{"column":3,"row":3},{"column":2,"row":4},{"column":3,"row":4}],"operator":"add","target":6},
      {"cells":[{"column":4,"row":3},{"column":4,"row":4}],"operator":"add","target":9},
      {"cells":[{"column":0,"row":4},{"column":1,"row":4}],"operator":"subtract","target":1}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-5x5-8234af033c951cde",
    "size": 5,
    "provenance": {"accepted_attempt":2,"generator_version":"0.3.0","profile":"easy","seed":"2026081103"},
    "cages": [
      {"cells":[{"column":0,"row":0}],"operator":"given","target":4},
      {"cells":[{"column":1,"row":0},{"column":1,"row":1}],"operator":"multiply","target":2},
      {"cells":[{"column":2,"row":0},{"column":2,"row":1}],"operator":"subtract","target":2},
      {"cells":[{"column":3,"row":0},{"column":4,"row":0}],"operator":"subtract","target":2},
      {"cells":[{"column":0,"row":1},{"column":0,"row":2}],"operator":"divide","target":5},
      {"cells":[{"column":3,"row":1},{"column":4,"row":1},{"column":3,"row":2}],"operator":"add","target":8},
      {"cells":[{"column":1,"row":2},{"column":1,"row":3}],"operator":"add","target":7},
      {"cells":[{"column":2,"row":2},{"column":2,"row":3}],"operator":"multiply","target":8},
      {"cells":[{"column":4,"row":2}],"operator":"given","target":5},
      {"cells":[{"column":0,"row":3},{"column":0,"row":4}],"operator":"add","target":5},
      {"cells":[{"column":3,"row":3}],"operator":"given","target":5},
      {"cells":[{"column":4,"row":3},{"column":3,"row":4},{"column":4,"row":4}],"operator":"add","target":8},
      {"cells":[{"column":1,"row":4},{"column":2,"row":4}],"operator":"add","target":6}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-5x5-8a9f36c0ae0f333b",
    "size": 5,
    "provenance": {"accepted_attempt":3,"generator_version":"0.3.0","profile":"easy","seed":"2026081104"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":0,"row":1},{"column":1,"row":1}],"operator":"add","target":12},
      {"cells":[{"column":1,"row":0}],"operator":"given","target":4},
      {"cells":[{"column":2,"row":0},{"column":2,"row":1}],"operator":"subtract","target":4},
      {"cells":[{"column":3,"row":0},{"column":4,"row":0},{"column":4,"row":1}],"operator":"add","target":6},
      {"cells":[{"column":3,"row":1},{"column":3,"row":2},{"column":3,"row":3}],"operator":"add","target":11},
      {"cells":[{"column":0,"row":2},{"column":1,"row":2}],"operator":"divide","target":2},
      {"cells":[{"column":2,"row":2}],"operator":"given","target":3},
      {"cells":[{"column":4,"row":2}],"operator":"given","target":4},
      {"cells":[{"column":0,"row":3},{"column":1,"row":3},{"column":2,"row":3}],"operator":"add","target":8},
      {"cells":[{"column":4,"row":3},{"column":3,"row":4},{"column":4,"row":4}],"operator":"add","target":9},
      {"cells":[{"column":0,"row":4},{"column":1,"row":4}],"operator":"subtract","target":1},
      {"cells":[{"column":2,"row":4}],"operator":"given","target":4}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-5x5-b368eaee1c82d546",
    "size": 5,
    "provenance": {"accepted_attempt":1,"generator_version":"0.3.0","profile":"easy","seed":"2026081201"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":1,"row":0}],"operator":"subtract","target":2},
      {"cells":[{"column":2,"row":0},{"column":3,"row":0}],"operator":"add","target":6},
      {"cells":[{"column":4,"row":0},{"column":4,"row":1},{"column":4,"row":2}],"operator":"add","target":10},
      {"cells":[{"column":0,"row":1}],"operator":"given","target":4},
      {"cells":[{"column":1,"row":1},{"column":1,"row":2},{"column":2,"row":2}],"operator":"add","target":10},
      {"cells":[{"column":2,"row":1}],"operator":"given","target":2},
      {"cells":[{"column":3,"row":1},{"column":3,"row":2}],"operator":"subtract","target":2},
      {"cells":[{"column":0,"row":2}],"operator":"given","target":1},
      {"cells":[{"column":0,"row":3},{"column":1,"row":3},{"column":0,"row":4}],"operator":"add","target":8},
      {"cells":[{"column":2,"row":3},{"column":3,"row":3}],"operator":"subtract","target":1},
      {"cells":[{"column":4,"row":3},{"column":4,"row":4}],"operator":"add","target":5},
      {"cells":[{"column":1,"row":4}],"operator":"given","target":4},
      {"cells":[{"column":2,"row":4},{"column":3,"row":4}],"operator":"divide","target":5}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-5x5-1f26ee000ca93014",
    "size": 5,
    "provenance": {"accepted_attempt":4,"generator_version":"0.3.0","profile":"easy","seed":"2026081202"},
    "cages": [
      {"cells":[{"column":0,"row":0}],"operator":"given","target":2},
      {"cells":[{"column":1,"row":0},{"column":2,"row":0}],"operator":"divide","target":3},
      {"cells":[{"column":3,"row":0},{"column":4,"row":0},{"column":4,"row":1}],"operator":"add","target":14},
      {"cells":[{"column":0,"row":1},{"column":0,"row":2}],"operator":"divide","target":4},
      {"cells":[{"column":1,"row":1},{"column":2,"row":1}],"operator":"multiply","target":6},
      {"cells":[{"column":3,"row":1},{"column":3,"row":2},{"column":4,"row":2}],"operator":"add","target":6},
      {"cells":[{"column":1,"row":2}],"operator":"given","target":4},
      {"cells":[{"column":2,"row":2},{"column":2,"row":3}],"operator":"add","target":9},
      {"cells":[{"column":0,"row":3},{"column":1,"row":3}],"operator":"subtract","target":3},
      {"cells":[{"column":3,"row":3},{"column":3,"row":4}],"operator":"multiply","target":12},
      {"cells":[{"column":4,"row":3},{"column":4,"row":4}],"operator":"add","target":3},
      {"cells":[{"column":0,"row":4},{"column":1,"row":4}],"operator":"subtract","target":2},
      {"cells":[{"column":2,"row":4}],"operator":"given","target":1}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-5x5-a7ec51bca15ef5c2",
    "size": 5,
    "provenance": {"accepted_attempt":2,"generator_version":"0.3.0","profile":"easy","seed":"2026081203"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":0,"row":1}],"operator":"subtract","target":1},
      {"cells":[{"column":1,"row":0},{"column":2,"row":0}],"operator":"add","target":9},
      {"cells":[{"column":3,"row":0},{"column":3,"row":1}],"operator":"subtract","target":1},
      {"cells":[{"column":4,"row":0},{"column":4,"row":1}],"operator":"divide","target":5},
      {"cells":[{"column":1,"row":1},{"column":2,"row":1},{"column":1,"row":2}],"operator":"add","target":10},
      {"cells":[{"column":0,"row":2},{"column":0,"row":3}],"operator":"add","target":6},
      {"cells":[{"column":2,"row":2},{"column":3,"row":2},{"column":4,"row":2}],"operator":"add","target":11},
      {"cells":[{"column":1,"row":3},{"column":2,"row":3}],"operator":"divide","target":2},
      {"cells":[{"column":3,"row":3},{"column":4,"row":3}],"operator":"subtract","target":1},
      {"cells":[{"column":0,"row":4},{"column":1,"row":4},{"column":2,"row":4}],"operator":"add","target":10},
      {"cells":[{"column":3,"row":4},{"column":4,"row":4}],"operator":"multiply","target":6}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-5x5-a936bfd6ffabe9d4",
    "size": 5,
    "provenance": {"accepted_attempt":1,"generator_version":"0.3.0","profile":"easy","seed":"2026081204"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":0,"row":1}],"operator":"add","target":7},
      {"cells":[{"column":1,"row":0},{"column":1,"row":1},{"column":2,"row":1}],"operator":"add","target":8},
      {"cells":[{"column":2,"row":0},{"column":3,"row":0},{"column":3,"row":1}],"operator":"add","target":8},
      {"cells":[{"column":4,"row":0}],"operator":"given","target":3},
      {"cells":[{"column":4,"row":1},{"column":4,"row":2}],"operator":"subtract","target":2},
      {"cells":[{"column":0,"row":2},{"column":0,"row":3},{"column":1,"row":3}],"operator":"add","target":8},
      {"cells":[{"column":1,"row":2},{"column":2,"row":2}],"operator":"subtract","target":2},
      {"cells":[{"column":3,"row":2}],"operator":"given","target":4},
      {"cells":[{"column":2,"row":3},{"column":2,"row":4}],"operator":"subtract","target":2},
      {"cells":[{"column":3,"row":3},{"column":3,"row":4},{"column":4,"row":4}],"operator":"add","target":8},
      {"cells":[{"column":4,"row":3}],"operator":"given","target":5},
      {"cells":[{"column":0,"row":4},{"column":1,"row":4}],"operator":"subtract","target":2}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-5x5-72f5382803bd2e70",
    "size": 5,
    "provenance": {"accepted_attempt":80,"generator_version":"0.3.0","profile":"medium","seed":"2026081002"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":0,"row":1},{"column":0,"row":2}],"operator":"multiply","target":8},
      {"cells":[{"column":1,"row":0},{"column":1,"row":1},{"column":1,"row":2}],"operator":"add","target":9},
      {"cells":[{"column":2,"row":0},{"column":3,"row":0},{"column":4,"row":0},{"column":2,"row":1}],"operator":"add","target":14},
      {"cells":[{"column":3,"row":1},{"column":4,"row":1},{"column":4,"row":2}],"operator":"add","target":11},
      {"cells":[{"column":2,"row":2}],"operator":"given","target":3},
      {"cells":[{"column":3,"row":2},{"column":3,"row":3},{"column":4,"row":3}],"operator":"add","target":8},
      {"cells":[{"column":0,"row":3}],"operator":"given","target":3},
      {"cells":[{"column":1,"row":3},{"column":2,"row":3}],"operator":"subtract","target":3},
      {"cells":[{"column":0,"row":4},{"column":1,"row":4},{"column":2,"row":4}],"operator":"multiply","target":40},
      {"cells":[{"column":3,"row":4},{"column":4,"row":4}],"operator":"subtract","target":2}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-5x5-b4f7b1b38757856c",
    "size": 5,
    "provenance": {"accepted_attempt":28,"generator_version":"0.3.0","profile":"medium","seed":"2026081003"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":1,"row":0},{"column":1,"row":1},{"column":2,"row":1}],"operator":"add","target":16},
      {"cells":[{"column":2,"row":0},{"column":3,"row":0},{"column":4,"row":0},{"column":3,"row":1}],"operator":"add","target":11},
      {"cells":[{"column":0,"row":1},{"column":0,"row":2}],"operator":"subtract","target":4},
      {"cells":[{"column":4,"row":1},{"column":3,"row":2},{"column":4,"row":2}],"operator":"add","target":6},
      {"cells":[{"column":1,"row":2},{"column":1,"row":3}],"operator":"divide","target":2},
      {"cells":[{"column":2,"row":2},{"column":2,"row":3},{"column":2,"row":4}],"operator":"add","target":8},
      {"cells":[{"column":0,"row":3},{"column":0,"row":4},{"column":1,"row":4}],"operator":"add","target":7},
      {"cells":[{"column":3,"row":3},{"column":3,"row":4},{"column":4,"row":4}],"operator":"add","target":12},
      {"cells":[{"column":4,"row":3}],"operator":"given","target":3}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-5x5-fea0782318a289be",
    "size": 5,
    "provenance": {"accepted_attempt":17,"generator_version":"0.3.0","profile":"medium","seed":"2026081004"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":1,"row":0},{"column":1,"row":1}],"operator":"add","target":10},
      {"cells":[{"column":2,"row":0},{"column":3,"row":0},{"column":4,"row":0},{"column":4,"row":1}],"operator":"add","target":10},
      {"cells":[{"column":0,"row":1}],"operator":"given","target":4},
      {"cells":[{"column":2,"row":1},{"column":3,"row":1},{"column":3,"row":2},{"column":4,"row":2}],"operator":"add","target":12},
      {"cells":[{"column":0,"row":2},{"column":1,"row":2},{"column":1,"row":3}],"operator":"multiply","target":12},
      {"cells":[{"column":2,"row":2}],"operator":"given","target":5},
      {"cells":[{"column":0,"row":3},{"column":0,"row":4},{"column":1,"row":4}],"operator":"add","target":8},
      {"cells":[{"column":2,"row":3},{"column":2,"row":4}],"operator":"multiply","target":12},
      {"cells":[{"column":3,"row":3},{"column":4,"row":3}],"operator":"multiply","target":10},
      {"cells":[{"column":3,"row":4},{"column":4,"row":4}],"operator":"divide","target":3}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-5x5-2be36fdfd854154d",
    "size": 5,
    "provenance": {"accepted_attempt":140,"generator_version":"0.3.0","profile":"medium","seed":"2026081101"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":1,"row":0},{"column":2,"row":0}],"operator":"multiply","target":10},
      {"cells":[{"column":3,"row":0},{"column":4,"row":0}],"operator":"multiply","target":12},
      {"cells":[{"column":0,"row":1},{"column":1,"row":1}],"operator":"add","target":5},
      {"cells":[{"column":2,"row":1},{"column":3,"row":1},{"column":4,"row":1},{"column":4,"row":2}],"operator":"add","target":15},
      {"cells":[{"column":0,"row":2},{"column":0,"row":3},{"column":0,"row":4}],"operator":"multiply","target":20},
      {"cells":[{"column":1,"row":2},{"column":1,"row":3}],"operator":"multiply","target":4},
      {"cells":[{"column":2,"row":2},{"column":3,"row":2}],"operator":"multiply","target":6},
      {"cells":[{"column":2,"row":3},{"column":3,"row":3}],"operator":"subtract","target":1},
      {"cells":[{"column":4,"row":3},{"column":4,"row":4}],"operator":"divide","target":2},
      {"cells":[{"column":1,"row":4}],"operator":"given","target":3},
      {"cells":[{"column":2,"row":4},{"column":3,"row":4}],"operator":"add","target":7}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-5x5-b5525d2c3a308224",
    "size": 5,
    "provenance": {"accepted_attempt":122,"generator_version":"0.3.0","profile":"medium","seed":"2026081102"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":1,"row":0},{"column":0,"row":1}],"operator":"add","target":10},
      {"cells":[{"column":2,"row":0},{"column":3,"row":0},{"column":2,"row":1}],"operator":"add","target":10},
      {"cells":[{"column":4,"row":0}],"operator":"given","target":3},
      {"cells":[{"column":1,"row":1},{"column":0,"row":2},{"column":1,"row":2}],"operator":"add","target":9},
      {"cells":[{"column":3,"row":1},{"column":4,"row":1}],"operator":"subtract","target":3},
      {"cells":[{"column":2,"row":2},{"column":3,"row":2},{"column":4,"row":2},{"column":2,"row":3}],"operator":"add","target":12},
      {"cells":[{"column":0,"row":3},{"column":1,"row":3}],"operator":"multiply","target":15},
      {"cells":[{"column":3,"row":3}],"operator":"given","target":1},
      {"cells":[{"column":4,"row":3},{"column":3,"row":4},{"column":4,"row":4}],"operator":"multiply","target":24},
      {"cells":[{"column":0,"row":4},{"column":1,"row":4},{"column":2,"row":4}],"operator":"add","target":8}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-5x5-d03e9558d2780813",
    "size": 5,
    "provenance": {"accepted_attempt":26,"generator_version":"0.3.0","profile":"medium","seed":"2026081103"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":1,"row":0}],"operator":"subtract","target":2},
      {"cells":[{"column":2,"row":0},{"column":3,"row":0},{"column":4,"row":0}],"operator":"multiply","target":40},
      {"cells":[{"column":0,"row":1},{"column":1,"row":1},{"column":2,"row":1}],"operator":"multiply","target":40},
      {"cells":[{"column":3,"row":1},{"column":4,"row":1},{"column":4,"row":2}],"operator":"multiply","target":15},
      {"cells":[{"column":0,"row":2},{"column":0,"row":3}],"operator":"multiply","target":10},
      {"cells":[{"column":1,"row":2},{"column":1,"row":3}],"operator":"add","target":3},
      {"cells":[{"column":2,"row":2},{"column":3,"row":2},{"column":2,"row":3},{"column":2,"row":4}],"operator":"multiply","target":60},
      {"cells":[{"column":3,"row":3},{"column":4,"row":3}],"operator":"multiply","target":12},
      {"cells":[{"column":0,"row":4},{"column":1,"row":4}],"operator":"subtract","target":1},
      {"cells":[{"column":3,"row":4},{"column":4,"row":4}],"operator":"add","target":3}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-5x5-fbacca21b6462568",
    "size": 5,
    "provenance": {"accepted_attempt":16,"generator_version":"0.3.0","profile":"medium","seed":"2026081104"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":1,"row":0}],"operator":"add","target":7},
      {"cells":[{"column":2,"row":0},{"column":3,"row":0},{"column":3,"row":1}],"operator":"add","target":6},
      {"cells":[{"column":4,"row":0},{"column":4,"row":1},{"column":4,"row":2}],"operator":"multiply","target":40},
      {"cells":[{"column":0,"row":1},{"column":0,"row":2},{"column":0,"row":3}],"operator":"add","target":8},
      {"cells":[{"column":1,"row":1},{"column":2,"row":1}],"operator":"multiply","target":10},
      {"cells":[{"column":1,"row":2}],"operator":"given","target":3},
      {"cells":[{"column":2,"row":2},{"column":3,"row":2},{"column":3,"row":3},{"column":3,"row":4}],"operator":"multiply","target":80},
      {"cells":[{"column":1,"row":3},{"column":0,"row":4},{"column":1,"row":4}],"operator":"add","target":10},
      {"cells":[{"column":2,"row":3},{"column":2,"row":4}],"operator":"add","target":5},
      {"cells":[{"column":4,"row":3},{"column":4,"row":4}],"operator":"divide","target":3}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-5x5-195429b1f39ccd2d",
    "size": 5,
    "provenance": {"accepted_attempt":25,"generator_version":"0.3.0","profile":"medium","seed":"2026081201"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":1,"row":0},{"column":0,"row":1}],"operator":"add","target":11},
      {"cells":[{"column":2,"row":0},{"column":1,"row":1},{"column":2,"row":1},{"column":2,"row":2}],"operator":"multiply","target":20},
      {"cells":[{"column":3,"row":0}],"operator":"given","target":5},
      {"cells":[{"column":4,"row":0},{"column":3,"row":1},{"column":4,"row":1}],"operator":"add","target":9},
      {"cells":[{"column":0,"row":2},{"column":1,"row":2},{"column":1,"row":3}],"operator":"add","target":8},
      {"cells":[{"column":3,"row":2},{"column":4,"row":2}],"operator":"subtract","target":1},
      {"cells":[{"column":0,"row":3},{"column":0,"row":4},{"column":1,"row":4}],"operator":"multiply","target":15},
      {"cells":[{"column":2,"row":3},{"column":3,"row":3},{"column":2,"row":4},{"column":3,"row":4}],"operator":"add","target":10},
      {"cells":[{"column":4,"row":3},{"column":4,"row":4}],"operator":"subtract","target":2}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-5x5-6606497a9285dc54",
    "size": 5,
    "provenance": {"accepted_attempt":103,"generator_version":"0.3.0","profile":"medium","seed":"2026081202"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":1,"row":0},{"column":2,"row":0}],"operator":"add","target":8},
      {"cells":[{"column":3,"row":0},{"column":4,"row":0},{"column":3,"row":1},{"column":3,"row":2}],"operator":"add","target":11},
      {"cells":[{"column":0,"row":1},{"column":1,"row":1},{"column":2,"row":1}],"operator":"add","target":9},
      {"cells":[{"column":4,"row":1}],"operator":"given","target":5},
      {"cells":[{"column":0,"row":2},{"column":0,"row":3},{"column":1,"row":3}],"operator":"multiply","target":15},
      {"cells":[{"column":1,"row":2},{"column":2,"row":2}],"operator":"multiply","target":8},
      {"cells":[{"column":4,"row":2},{"column":4,"row":3},{"column":4,"row":4}],"operator":"multiply","target":8},
      {"cells":[{"column":2,"row":3},{"column":3,"row":3},{"column":2,"row":4},{"column":3,"row":4}],"operator":"add","target":13},
      {"cells":[{"column":0,"row":4},{"column":1,"row":4}],"operator":"subtract","target":1}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-5x5-03494635706cf1dc",
    "size": 5,
    "provenance": {"accepted_attempt":75,"generator_version":"0.3.0","profile":"medium","seed":"2026081203"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":1,"row":0},{"column":2,"row":0},{"column":0,"row":1}],"operator":"add","target":11},
      {"cells":[{"column":3,"row":0},{"column":4,"row":0}],"operator":"divide","target":2},
      {"cells":[{"column":1,"row":1},{"column":2,"row":1}],"operator":"divide","target":5},
      {"cells":[{"column":3,"row":1},{"column":4,"row":1}],"operator":"subtract","target":1},
      {"cells":[{"column":0,"row":2},{"column":1,"row":2},{"column":0,"row":3}],"operator":"add","target":7},
      {"cells":[{"column":2,"row":2},{"column":3,"row":2},{"column":4,"row":2},{"column":3,"row":3}],"operator":"multiply","target":30},
      {"cells":[{"column":1,"row":3},{"column":2,"row":3},{"column":0,"row":4},{"column":1,"row":4}],"operator":"add","target":14},
      {"cells":[{"column":4,"row":3},{"column":2,"row":4},{"column":3,"row":4},{"column":4,"row":4}],"operator":"multiply","target":50}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-5x5-820a0ba45f8ab5ab",
    "size": 5,
    "provenance": {"accepted_attempt":32,"generator_version":"0.3.0","profile":"medium","seed":"2026081204"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":0,"row":1},{"column":0,"row":2}],"operator":"multiply","target":40},
      {"cells":[{"column":1,"row":0},{"column":1,"row":1},{"column":1,"row":2}],"operator":"multiply","target":6},
      {"cells":[{"column":2,"row":0},{"column":3,"row":0},{"column":3,"row":1}],"operator":"add","target":8},
      {"cells":[{"column":4,"row":0},{"column":4,"row":1}],"operator":"multiply","target":20},
      {"cells":[{"column":2,"row":1}],"operator":"given","target":2},
      {"cells":[{"column":2,"row":2},{"column":3,"row":2},{"column":2,"row":3}],"operator":"multiply","target":60},
      {"cells":[{"column":4,"row":2},{"column":4,"row":3},{"column":4,"row":4}],"operator":"add","target":6},
      {"cells":[{"column":0,"row":3},{"column":0,"row":4}],"operator":"add","target":4},
      {"cells":[{"column":1,"row":3},{"column":1,"row":4},{"column":2,"row":4}],"operator":"multiply","target":20},
      {"cells":[{"column":3,"row":3},{"column":3,"row":4}],"operator":"multiply","target":10}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-5x5-b79b300988cf89fb",
    "size": 5,
    "provenance": {"accepted_attempt":93,"generator_version":"0.3.0","profile":"hard","seed":"2026081002"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":1,"row":0},{"column":0,"row":1},{"column":0,"row":2}],"operator":"multiply","target":160},
      {"cells":[{"column":2,"row":0},{"column":2,"row":1},{"column":3,"row":1}],"operator":"add","target":10},
      {"cells":[{"column":3,"row":0},{"column":4,"row":0},{"column":4,"row":1},{"column":4,"row":2}],"operator":"multiply","target":30},
      {"cells":[{"column":1,"row":1},{"column":1,"row":2},{"column":2,"row":2},{"column":2,"row":3}],"operator":"add","target":10},
      {"cells":[{"column":3,"row":2},{"column":3,"row":3},{"column":2,"row":4},{"column":3,"row":4}],"operator":"multiply","target":20},
      {"cells":[{"column":0,"row":3},{"column":1,"row":3},{"column":1,"row":4}],"operator":"multiply","target":10},
      {"cells":[{"column":4,"row":3},{"column":4,"row":4}],"operator":"multiply","target":12},
      {"cells":[{"column":0,"row":4}],"operator":"given","target":3}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-5x5-9f54dae2e1c779b6",
    "size": 5,
    "provenance": {"accepted_attempt":410,"generator_version":"0.3.0","profile":"hard","seed":"2026081003"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":1,"row":0}],"operator":"subtract","target":1},
      {"cells":[{"column":2,"row":0},{"column":2,"row":1},{"column":3,"row":1},{"column":4,"row":1}],"operator":"multiply","target":48},
      {"cells":[{"column":3,"row":0},{"column":4,"row":0}],"operator":"add","target":6},
      {"cells":[{"column":0,"row":1},{"column":1,"row":1},{"column":1,"row":2}],"operator":"multiply","target":10},
      {"cells":[{"column":0,"row":2},{"column":0,"row":3}],"operator":"add","target":9},
      {"cells":[{"column":2,"row":2},{"column":3,"row":2},{"column":4,"row":2},{"column":3,"row":3}],"operator":"multiply","target":48},
      {"cells":[{"column":1,"row":3},{"column":0,"row":4},{"column":1,"row":4}],"operator":"add","target":8},
      {"cells":[{"column":2,"row":3},{"column":2,"row":4}],"operator":"multiply","target":5},
      {"cells":[{"column":4,"row":3},{"column":3,"row":4},{"column":4,"row":4}],"operator":"add","target":10}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-5x5-5aee68d53208e949",
    "size": 5,
    "provenance": {"accepted_attempt":215,"generator_version":"0.3.0","profile":"hard","seed":"2026081004"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":1,"row":0},{"column":2,"row":0},{"column":1,"row":1}],"operator":"add","target":12},
      {"cells":[{"column":3,"row":0},{"column":3,"row":1},{"column":3,"row":2}],"operator":"multiply","target":24},
      {"cells":[{"column":4,"row":0},{"column":4,"row":1},{"column":4,"row":2}],"operator":"multiply","target":10},
      {"cells":[{"column":0,"row":1},{"column":0,"row":2},{"column":1,"row":2},{"column":0,"row":3}],"operator":"multiply","target":60},
      {"cells":[{"column":2,"row":1},{"column":2,"row":2},{"column":2,"row":3}],"operator":"add","target":10},
      {"cells":[{"column":1,"row":3},{"column":0,"row":4},{"column":1,"row":4},{"column":2,"row":4}],"operator":"multiply","target":30},
      {"cells":[{"column":3,"row":3},{"column":4,"row":3},{"column":3,"row":4},{"column":4,"row":4}],"operator":"multiply","target":60}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-5x5-923376b99d37eac1",
    "size": 5,
    "provenance": {"accepted_attempt":523,"generator_version":"0.3.0","profile":"hard","seed":"2026081101"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":0,"row":1},{"column":1,"row":1},{"column":1,"row":2}],"operator":"add","target":9},
      {"cells":[{"column":1,"row":0},{"column":2,"row":0},{"column":3,"row":0},{"column":3,"row":1}],"operator":"multiply","target":120},
      {"cells":[{"column":4,"row":0},{"column":4,"row":1},{"column":4,"row":2}],"operator":"multiply","target":60},
      {"cells":[{"column":2,"row":1},{"column":2,"row":2},{"column":3,"row":2},{"column":3,"row":3}],"operator":"add","target":11},
      {"cells":[{"column":0,"row":2},{"column":0,"row":3},{"column":0,"row":4}],"operator":"add","target":10},
      {"cells":[{"column":1,"row":3},{"column":2,"row":3},{"column":1,"row":4}],"operator":"multiply","target":20},
      {"cells":[{"column":4,"row":3},{"column":2,"row":4},{"column":3,"row":4},{"column":4,"row":4}],"operator":"add","target":9}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-5x5-026a72a1a4f9b985",
    "size": 5,
    "provenance": {"accepted_attempt":215,"generator_version":"0.3.0","profile":"hard","seed":"2026081102"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":0,"row":1}],"operator":"add","target":6},
      {"cells":[{"column":1,"row":0},{"column":1,"row":1}],"operator":"multiply","target":5},
      {"cells":[{"column":2,"row":0},{"column":2,"row":1},{"column":3,"row":1},{"column":4,"row":1}],"operator":"add","target":13},
      {"cells":[{"column":3,"row":0},{"column":4,"row":0}],"operator":"multiply","target":6},
      {"cells":[{"column":0,"row":2},{"column":0,"row":3},{"column":0,"row":4}],"operator":"multiply","target":15},
      {"cells":[{"column":1,"row":2},{"column":2,"row":2},{"column":1,"row":3}],"operator":"multiply","target":24},
      {"cells":[{"column":3,"row":2},{"column":4,"row":2}],"operator":"subtract","target":4},
      {"cells":[{"column":2,"row":3}],"operator":"given","target":1},
      {"cells":[{"column":3,"row":3},{"column":1,"row":4},{"column":2,"row":4},{"column":3,"row":4}],"operator":"multiply","target":120},
      {"cells":[{"column":4,"row":3},{"column":4,"row":4}],"operator":"subtract","target":2}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-5x5-d81cb5b1c00eecdd",
    "size": 5,
    "provenance": {"accepted_attempt":26,"generator_version":"0.3.0","profile":"hard","seed":"2026081103"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":1,"row":0},{"column":0,"row":1},{"column":1,"row":1}],"operator":"add","target":9},
      {"cells":[{"column":2,"row":0},{"column":2,"row":1},{"column":3,"row":1}],"operator":"add","target":11},
      {"cells":[{"column":3,"row":0},{"column":4,"row":0},{"column":4,"row":1}],"operator":"add","target":10},
      {"cells":[{"column":0,"row":2},{"column":1,"row":2}],"operator":"multiply","target":20},
      {"cells":[{"column":2,"row":2},{"column":1,"row":3},{"column":2,"row":3},{"column":1,"row":4}],"operator":"add","target":13},
      {"cells":[{"column":3,"row":2},{"column":4,"row":2},{"column":4,"row":3}],"operator":"add","target":6},
      {"cells":[{"column":0,"row":3},{"column":0,"row":4}],"operator":"multiply","target":4},
      {"cells":[{"column":3,"row":3},{"column":2,"row":4},{"column":3,"row":4},{"column":4,"row":4}],"operator":"add","target":12}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-5x5-5a2248b69027790b",
    "size": 5,
    "provenance": {"accepted_attempt":618,"generator_version":"0.3.0","profile":"hard","seed":"2026081104"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":1,"row":0},{"column":0,"row":1}],"operator":"multiply","target":15},
      {"cells":[{"column":2,"row":0},{"column":1,"row":1},{"column":2,"row":1}],"operator":"multiply","target":12},
      {"cells":[{"column":3,"row":0},{"column":4,"row":0},{"column":3,"row":1},{"column":4,"row":1}],"operator":"multiply","target":80},
      {"cells":[{"column":0,"row":2},{"column":0,"row":3}],"operator":"divide","target":4},
      {"cells":[{"column":1,"row":2},{"column":2,"row":2},{"column":3,"row":2},{"column":1,"row":3}],"operator":"multiply","target":120},
      {"cells":[{"column":4,"row":2},{"column":2,"row":3},{"column":3,"row":3},{"column":4,"row":3}],"operator":"multiply","target":30},
      {"cells":[{"column":0,"row":4},{"column":1,"row":4},{"column":2,"row":4},{"column":3,"row":4}],"operator":"add","target":10},
      {"cells":[{"column":4,"row":4}],"operator":"given","target":5}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-5x5-66969d5836802339",
    "size": 5,
    "provenance": {"accepted_attempt":409,"generator_version":"0.3.0","profile":"hard","seed":"2026081201"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":1,"row":0},{"column":0,"row":1}],"operator":"add","target":9},
      {"cells":[{"column":2,"row":0}],"operator":"given","target":5},
      {"cells":[{"column":3,"row":0},{"column":4,"row":0},{"column":4,"row":1},{"column":4,"row":2}],"operator":"add","target":8},
      {"cells":[{"column":1,"row":1},{"column":2,"row":1}],"operator":"subtract","target":1},
      {"cells":[{"column":3,"row":1},{"column":2,"row":2},{"column":3,"row":2},{"column":2,"row":3}],"operator":"add","target":12},
      {"cells":[{"column":0,"row":2},{"column":1,"row":2},{"column":0,"row":3}],"operator":"add","target":9},
      {"cells":[{"column":1,"row":3},{"column":0,"row":4},{"column":1,"row":4}],"operator":"add","target":10},
      {"cells":[{"column":3,"row":3},{"column":4,"row":3},{"column":4,"row":4}],"operator":"add","target":11},
      {"cells":[{"column":2,"row":4},{"column":3,"row":4}],"operator":"divide","target":2}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-5x5-64b56d0cd1be88a9",
    "size": 5,
    "provenance": {"accepted_attempt":86,"generator_version":"0.3.0","profile":"hard","seed":"2026081202"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":1,"row":0},{"column":0,"row":1},{"column":0,"row":2}],"operator":"multiply","target":20},
      {"cells":[{"column":2,"row":0},{"column":3,"row":0}],"operator":"add","target":7},
      {"cells":[{"column":4,"row":0},{"column":2,"row":1},{"column":3,"row":1},{"column":4,"row":1}],"operator":"add","target":11},
      {"cells":[{"column":1,"row":1},{"column":1,"row":2},{"column":2,"row":2}],"operator":"add","target":10},
      {"cells":[{"column":3,"row":2},{"column":4,"row":2}],"operator":"multiply","target":12},
      {"cells":[{"column":0,"row":3},{"column":0,"row":4}],"operator":"add","target":7},
      {"cells":[{"column":1,"row":3},{"column":2,"row":3},{"column":1,"row":4}],"operator":"add","target":10},
      {"cells":[{"column":3,"row":3},{"column":4,"row":3},{"column":2,"row":4},{"column":3,"row":4}],"operator":"multiply","target":30},
      {"cells":[{"column":4,"row":4}],"operator":"given","target":2}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-5x5-f76675e34c58f758",
    "size": 5,
    "provenance": {"accepted_attempt":92,"generator_version":"0.3.0","profile":"hard","seed":"2026081203"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":1,"row":0},{"column":2,"row":0},{"column":1,"row":1}],"operator":"add","target":11},
      {"cells":[{"column":3,"row":0},{"column":3,"row":1}],"operator":"add","target":9},
      {"cells":[{"column":4,"row":0},{"column":4,"row":1}],"operator":"subtract","target":1},
      {"cells":[{"column":0,"row":1},{"column":0,"row":2},{"column":1,"row":2}],"operator":"multiply","target":6},
      {"cells":[{"column":2,"row":1},{"column":2,"row":2},{"column":2,"row":3}],"operator":"multiply","target":20},
      {"cells":[{"column":3,"row":2},{"column":4,"row":2},{"column":3,"row":3}],"operator":"add","target":8},
      {"cells":[{"column":0,"row":3},{"column":1,"row":3},{"column":0,"row":4},{"column":1,"row":4}],"operator":"add","target":16},
      {"cells":[{"column":4,"row":3},{"column":3,"row":4},{"column":4,"row":4}],"operator":"add","target":6},
      {"cells":[{"column":2,"row":4}],"operator":"given","target":2}
    ]
  },
  {
    "schema": "kenken.puzzle/v1",
    "id": "kk-5x5-887b71751b9935a2",
    "size": 5,
    "provenance": {"accepted_attempt":251,"generator_version":"0.3.0","profile":"hard","seed":"2026081204"},
    "cages": [
      {"cells":[{"column":0,"row":0},{"column":1,"row":0},{"column":2,"row":0},{"column":1,"row":1}],"operator":"add","target":10},
      {"cells":[{"column":3,"row":0},{"column":3,"row":1},{"column":3,"row":2}],"operator":"multiply","target":24},
      {"cells":[{"column":4,"row":0},{"column":4,"row":1},{"column":4,"row":2}],"operator":"multiply","target":60},
      {"cells":[{"column":0,"row":1},{"column":0,"row":2}],"operator":"subtract","target":2},
      {"cells":[{"column":2,"row":1},{"column":1,"row":2},{"column":2,"row":2},{"column":2,"row":3}],"operator":"add","target":12},
      {"cells":[{"column":0,"row":3},{"column":1,"row":3}],"operator":"add","target":5},
      {"cells":[{"column":3,"row":3},{"column":4,"row":3},{"column":4,"row":4}],"operator":"add","target":8},
      {"cells":[{"column":0,"row":4},{"column":1,"row":4},{"column":2,"row":4},{"column":3,"row":4}],"operator":"multiply","target":60}
    ]
  }
];
