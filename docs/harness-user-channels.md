# Operator-visible message channels in the Claude Code harness · `spec:harness:user-channels`

This document records every channel the estate has for putting a message in front of the operator, with the measured visibility properties of each. The core distinction is **who receives the bytes**: some channels render for the operator without ever entering the model's context (operator-only), some are injected into the model's context as instructions (model-visible), and some render nowhere at all on the current desktop build. These facts were established empirically on 2026-09-01 against the live desktop app (Claude Code CLI 2.1.251/2.1.252 era) — re-verify on major harness upgrades, since at least one channel (non-blocking hook stderr) demonstrably changed behavior across builds.

## Hook-script channels (script-side, fire on harness events) · `sec:harness:hook-channels`

A hook script receives the event payload on stdin and answers with an exit code, stderr, and optionally a JSON object on stdout. The JSON fields below are part of the hooks output contract.

|Channel|Operator sees|Prominence|Model sees|Side effect|
|-------|-------------|----------|----------|-----------|
|`{"systemMessage": "..."}` on stdout, exit 0|yes|collapsed system line in the chat|**no** (proven)|none|
|`{"continue": false, "stopReason": "..."}` on stdout|**no** (measured live, twice)|—|**yes** — delivered as the stop-continuation note in the model's context|**halts the agent's turn**|
|stderr + exit 2 (block)|yes|prominent feedback line|**yes** — injected as an instruction the model must act on|blocks the event|
|stderr + exit 1 (non-blocking error)|**no** on the current desktop build (proven: fired and rendered nowhere)|—|no|none|
|`permissionDecision: "ask"` + reason (PreToolUse)|yes|dialog demanding a click|partially, after the decision|gates the tool call|

Choosing between them:

- `systemMessage` is the passive FYI register: visible, ignorable, collapsed by default. Right for notices the operator may read later.
- `continue: false` + `stopReason` halts the turn and tells the AGENT why — the upstream documentation claims the reason is shown to the user and not to Claude, and live measurement (twice, on the real session and on an isolated one-shot) proved the exact inverse on this build: the operator sees nothing, and the reason arrives in the model's context as the stop-continuation note. It is therefore a halt-plus-agent-notice, not an operator channel. A verdict that must reach every audience carries BOTH fields in one JSON object — `stopReason` for the halt and the agent, `systemMessage` for the operator — the shape the (since abandoned) conducted-compaction witness used ("superloop wound down — will compact now…").
- exit 2 + stderr is not an operator channel at all: the operator sees it, but so does the model — it is the instruction-injection channel (the guard's prepare prompt uses it, deliberately).
- exit 1 + stderr should be treated as a dead channel and never relied on; it silently renders nowhere on the current build.

## What does NOT work (measured dead ends) · `sec:harness:dead-ends`

- **Appending `type:"system"` records to the session transcript**: structurally invisible to the model (correct) but ALSO invisible to the operator — the desktop app renders its own conversation store and never re-reads the transcript file, so externally appended records (including whole conducted turns) never appear in the app, even after relaunch. The record remains useful solely as a durable audit artifact in the file.
- **The Messages-API "mid-conversation system message"** (`{"role": "system"}` appended to `messages[]`): despite the name, this is the opposite of an operator channel — it is an operator *instruction to the model*, model-visible by design. Never reach for it when the goal is operator-only display.
- **`PushNotification` while the operator is at the terminal**: the harness deliberately suppresses it as redundant ("terminal is active"). It is the away-channel only.

## Agent-side calls that render in or beside the chat · `sec:harness:agent-side-renders`

Available to the agent as tools, not to scripts: the background-task **chip** (`spawn_task`, withdrawable via `dismiss_task`), **chapter dividers** (`mark_chapter`), **file cards** (`SendUserFile`), **artifacts** (side-panel pages), and **interactive widgets** (`show_widget`). All render for the operator; the agent knows only its own call and the tool result. These are agent-initiated, so they cannot serve script-side automation like the conductor.

## Out-of-chat channels · `sec:harness:out-of-chat`

- **Desktop notification** (`notify-send`, `gdbus` fallback): prominent, immediate, works regardless of which window the operator watches — and the only real-time channel that reaches the operator during a HEADLESS conducted ritual, whose hook feedback renders in no window. The conductor uses it at compact trigger.
- **`PushNotification`** (harness tool): reaches the operator when away (desktop, plus phone under Remote Control); suppressed while they are watching.

## Standing consequences · `sec:harness:channel-consequences`

- The conducted-compaction witness verdict carries `continue: false` + `stopReason` + `systemMessage` in one JSON object: the halt is the ritual's own next step, the stop reason tells the agent why its turn ended, and the systemMessage puts "will compact now" in front of the operator — with the desktop notification covering headless conduction.
- Any design that needs "a chat line the operator sees but the model does not" has exactly ONE in-chat channel on the current build: `systemMessage`. `stopReason` is the reverse (model-visible), and every other candidate measured dead.
