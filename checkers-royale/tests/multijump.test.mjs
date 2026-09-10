/**
 * Proves the click-through logic for multi-jumps against real move lists from
 * the engine: pick a piece, click each landing square in turn, and confirm the
 * sequence resolves to exactly one legal move.
 */
import { nextStops, completedMove, movesFromSquare } from "../web/lib/game.ts";

const API = "http://127.0.0.1:5328/api/state";

async function legal(board, player) {
  const r = await fetch(API, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ board, player }),
  });
  return r.json();
}

const empty = () => Array.from({ length: 8 }, () => Array(8).fill(0));

let failures = 0;
function check(label, condition, extra = "") {
  console.log(`  ${condition ? "OK  " : "FAIL"}  ${label}${extra ? "  " + extra : ""}`);
  if (!condition) failures += 1;
}

// --- 1. a forced double capture for a white man --------------------------
{
  const b = empty();
  b[5][2] = 1;   // white man c3
  b[4][3] = -1;  // black man d4
  b[2][3] = -1;  // black man d6
  const state = await legal(b, 1);
  const from = state.moves[0].path[0];
  const mine = movesFromSquare(state.moves, from);

  let partial = [from];
  const visited = [];
  for (let guard = 0; guard < 6; guard += 1) {
    const stops = nextStops(mine, partial);
    if (stops.length === 0) break;
    partial = [...partial, stops[0]];
    visited.push(stops[0]);
    const done = completedMove(mine, partial);
    if (done) {
      check("double capture resolves by clicking each landing square",
        done.captured.length === 2, `notation ${done.notation}`);
      break;
    }
  }
  check("two landing squares were stepped through", visited.length === 2,
    `visited ${JSON.stringify(visited)}`);
}

// --- 2. a branching king capture: several landings, one must be chosen ----
{
  const b = empty();
  b[7][0] = 3;   // white king a1
  b[5][2] = -1;  // black man c3
  const state = await legal(b, 1);
  const from = state.moves[0].path[0];
  const mine = movesFromSquare(state.moves, from);
  const stops = nextStops(mine, [from]);
  check("flying king offers every square beyond its victim", stops.length >= 3,
    `${stops.length} landing squares`);

  const done = completedMove(mine, [from, stops[stops.length - 1]]);
  check("choosing the far landing square completes the move", done !== null,
    done ? done.notation : "");
}

// --- 3. a quiet move completes in one click ------------------------------
{
  const state = await legal(null, 1);
  const board = state.board;
  const fresh = await legal(board, 1);
  const from = fresh.moves[0].path[0];
  const mine = movesFromSquare(fresh.moves, from);
  const stops = nextStops(mine, [from]);
  const done = completedMove(mine, [from, stops[0]]);
  check("a plain step resolves on the first destination click", done !== null,
    done ? done.notation : "");
  check("a plain step captures nothing", done && done.captured.length === 0);
}

console.log(failures === 0 ? "\nALL MULTI-JUMP CHECKS PASSED" : `\n${failures} CHECK(S) FAILED`);
process.exit(failures === 0 ? 0 : 1);
