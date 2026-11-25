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
  }
];
