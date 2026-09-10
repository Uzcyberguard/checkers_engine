# Checkers Royale

Russian draughts (shashki) in the browser, played against a real alpha-beta
search engine written in Python.

This directory sits inside the `checkers_engine` repository and adds a web
interface on top of the engine in its root, along with the rules and search
work described further down. Nothing in the parent directory is modified: the
original `main.py` still runs exactly as before.

Live at **https://checkers-royale.vercel.app**.

> Deploying from Git: this is not the repository root, so set the Vercel
> project's **Root Directory** to `checkers-royale/`. The `vercel.json` beside
> this file then describes both services.

## Rules

Russian draughts, not American checkers:

- men step one square diagonally forward,
- men capture in **all four** diagonal directions, forward and backward,
- kings **fly**: they slide any distance along a clear diagonal and may land on
  any empty square beyond the piece they capture,
- captures are **compulsory**, and a capture sequence must be continued while
  further captures are available,
- a man that reaches the far rank **mid-capture** is crowned and carries on
  capturing as a king,
- **Turkish strike**: captured pieces stay on the board as obstacles until the
  whole move completes, and can never be jumped twice.

## Layout

One Vercel project built from two **services**: a Next.js frontend and a
Python backend, sharing a domain.

```
vercel.json          service definitions and the routing between them
engine/              Python service
  main.py              ASGI entrypoint (FastAPI); transport only
  _lib/rules.py        move generation and rules
  _lib/evaluate.py     positional evaluation, in centipawns
  _lib/search.py       alpha-beta, iterative deepening, transposition table
  _lib/service.py      request handling
web/                 Next.js 16 frontend (React 19, Tailwind 4, Motion)
  app/ components/ lib/ public/
tests/               engine tests, including perft
devserver.py         serves the same endpoints locally on port 5328
```

> **Why services, and not `api/*.py` next to the Next.js app?** That older
> layout no longer produces functions when a framework is detected: Next.js
> claims the whole build and `/api/new` just returns the HTML shell. Vercel now
> routes a polyglot project through `services` in `vercel.json`, which is what
> this repository uses. `/api/(.*)` goes to the engine, everything else to the
> frontend, and the backend receives the original path — so the FastAPI routes
> are declared with their `/api` prefix rather than stripped.

The API is stateless: the client holds the position and posts it with each
request, which suits serverless functions and makes undo trivial.

| Endpoint       | Purpose                                                        |
| -------------- | -------------------------------------------------------------- |
| `POST /api/new`     | the opening position and its legal moves                  |
| `POST /api/state`   | legal moves, status and evaluation for any position       |
| `POST /api/ai`      | the engine's move **and** the replies you then face       |
| `POST /api/analyse` | the engine's preferred move, used for hints               |

`/api/ai` returns the resulting position too, so a full turn costs one round
trip. Every legal move arrives with the board it produces, which lets the
interface highlight and apply moves without waiting on the network.

## Running it

```bash
npm install
python devserver.py          # engine API on :5328
npm run dev                  # interface on :3000
```

`next.config.ts` proxies `/api/*` to the Python server in development. On
Vercel each file in `api/` is its own function, so no proxy is involved.

```bash
python tests/test_engine.py  # engine tests
npm run build                # production build
```

## What changed in the engine

The original move generator was already correct on the hard parts, and its
perft counts from the opening position match the published values for Russian
draughts. The rewrite keeps its behaviour and fixes three things:

- **`int(-a/3)` treated empty squares as enemies.** For a man, `a` is 1, so
  `int(-1/3)` evaluates to `0`, and `is_there_captures` reported a capture for
  a lone man on an empty board. It was only ever reached with kings, so it was
  a latent fault rather than a live one, but the ownership test is now explicit.
- **Landing squares went missing.** When a flying king could stop on several
  squares after a capture, any square that did not allow a further capture was
  discarded if another square did. Those are legal moves.
- **The Turkish strike rule was not implemented.** Captured pieces were removed
  immediately, so a king could pass back over a square it had already cleared.

Search-side changes:

- The root now shares one alpha window across sibling moves. The original
  passed a fresh `-inf, +inf` to every root move, which threw away nearly all
  of its root pruning.
- Iterative deepening with a **time budget** instead of a fixed depth, which is
  what a serverless function needs.
- A transposition table, move ordering (transposition move, then captures by
  size, then killers and history), and capture extensions.
- Randomised tie-breaking, so the engine no longer replays an identical game
  every time.

Move generation is about six times faster, mostly by not copying the board for
pieces that have no capture available.

Measured on the opening position: perft(6) = 37,986 in 0.31s, and a one-second
budget reaches depth 8–9.

## Credits

**Hasan Normamatov** ([Uzcyberguard](https://github.com/Uzcyberguard)) — the
search engine: board representation, move generation, evaluation and the
alpha-beta search this project is built on.

**Asadbek Abduxalilov** — the web interface: game design and direction, the
board and piece rendering, interaction and animation, the HTTP API that fronts
the engine, the rules and search work described above, and the deployment.

Board palettes are sampled from the board art in the original repository. The
sound effects were synthesised for this project, so there is no third-party
audio.
