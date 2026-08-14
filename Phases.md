# Phases.md — LinuXpert Development Phases (6-Day Build)

**Status:** MVP planning — pre-implementation
**Companion documents:** [PRD.md](./PRD.md), [Architecture.md](./Architecture.md), [Rules.md](./Rules.md), [Design.md](./Design.md)

---

## Governing principle

**The security gate, safe execution model, and action boundaries are established by the end of Phase 3 (day 2), before the action list grows.** Every action added after that point reuses an already-proven pipeline, so the marginal cost per action drops sharply — the first three actions are expensive to build safely, the remaining seven are comparatively cheap. There is no dedicated "add security later" phase; there is no phase in this document where an action executes without going through risk classification, confirmation, and verification.

Phases are sequential and each has a **Definition of Done** that must be met before moving to the next — but see §"Scope Reduction Ladder" below for what to cut if a phase runs long.

---

## Phase 1 — Foundation & Safe Read-Only Actions
**Target: Day 1**

**Objective:** Stand up the CLI shell and prove the architecture's data types end-to-end using only zero-risk actions, so every later phase builds on a working skeleton rather than a plan.

**Features/components implemented:**
- Project scaffold (`pyproject.toml`, `linuxpert/` package structure per [Architecture.md](./Architecture.md) §20)
- `cli.py` REPL loop (`LinuXpert >` prompt, read-eval-print, exit command)
- Core types: `ActionRequest`, `ActionResult`, `RiskTier` enum, `Action` protocol (`core/base` per architecture)
- Distro detection (`core/distro.py`) reading `/etc/os-release`
- 4–5 SAFE actions wired directly (no LLM yet — hardcoded command-to-action mapping is acceptable temporarily for this phase only): `show_ram_usage`, `show_cpu_usage`, `show_disk_usage`, `find_large_files`, `show_top_processes`, via `psutil`

**Dependencies:** None (first phase).

**Expected output:** Running `linuxpert`, typing e.g. `ram` or a fixed test phrase, and getting a real RAM-usage readout sourced from `psutil` on the actual machine.

**Testing requirements:** Unit tests for each SAFE action's data-producing logic; manual run on a real Ubuntu/Debian environment (or WSL/VM) confirming numbers are plausible.

**Definition of done:**
- [ ] CLI starts, accepts input, exits cleanly.
- [ ] All 5 SAFE actions return real, correct data from the local machine.
- [ ] `ActionRequest`/`ActionResult`/`RiskTier` types exist and are used consistently.
- [ ] Distro detection correctly identifies Ubuntu/Debian and fails closed (clear message, no crash) on anything else.

**Do NOT attempt in this phase:** LLM integration, any MODERATE/DANGEROUS action, confirmation UI, real intent parsing. The temporary hardcoded phrase-to-action mapping is scaffolding, not a shortcut around Phase 2 — it gets replaced, not extended.

---

## Phase 2 — Intent Parsing
**Target: Day 2 (first half)**

**Objective:** Replace the temporary hardcoded mapping with real LLM-driven intent parsing, constrained to the action registry.

**Features/components implemented:**
- `nlu/prompts.py`: generates tool/function specs from the action registry (name, description, parameter schema) — one source of truth, not a hand-maintained duplicate
- `nlu/intent_parser.py`: sends user text + minimal system context to Claude via tool-use; parses the response into an `ActionRequest`; returns "no matching action" for anything that isn't a valid, schema-conforming tool call
- Registry entries for the 5 Phase 1 actions formalized in `actions/registry.py`, replacing the hardcoded mapping

**Dependencies:** Phase 1 (needs the action types and at least a few real actions to parse into).

**Expected output:** Typing natural-language variants ("show my ram usage", "how much memory am I using") correctly resolves to `show_ram_usage()` via the LLM, not string matching. An out-of-registry request ("hack the mainframe") is cleanly reported as unsupported.

**Testing requirements:** A fixture list of phrase → expected action pairs (covering the example phrasings in [PRD.md](./PRD.md) §12) run against the real intent parser; confirm correct resolution and confirm the unmapped-request path never falls through to execution of anything.

**Definition of done:**
- [ ] All Phase 1 actions are resolved correctly from varied natural-language phrasings.
- [ ] An unmapped request produces a clear refusal, never a fallback execution.
- [ ] LLM API failure (simulate by breaking the key) fails closed with a clear message, not a crash or a loosened path.

**Do NOT attempt in this phase:** Any action beyond the 5 already built; multi-step/compound request handling; risk classification logic (that's Phase 3, even though it's tempting to bolt it on here — keep the phases' concerns separated for testability).

---

## Phase 3 — Security Gate
**Target: Day 2 (second half)**

**Objective:** Build the full risk classification, confirmation, and block-pattern system — end to end — before any MODERATE or DANGEROUS action exists to execute through it. This is the phase [Rules.md](./Rules.md) §1 is entirely about, and it is the project's core differentiator; it does not get compressed if the schedule slips elsewhere.

**Features/components implemented:**
- `core/risk.py`: static risk-tier lookup table (per [Architecture.md](./Architecture.md) §7); block-pattern matcher covering the catastrophic patterns listed in [PRD.md](./PRD.md) §19
- Confirmation rendering in `cli.py` per [Design.md](./Design.md) (SAFE passthrough, MODERATE single-confirm, DANGEROUS explicit-typed-confirm, BLOCKED refusal screen)
- `core/executor.py`: the single `run_argv()` entry point, argument-list-only, with the one-place `sudo` prepending rule from [Architecture.md](./Architecture.md) §10 — built now even though only SAFE actions exist yet, so Phase 4's privileged actions have nowhere else to go but through it

**Dependencies:** Phase 2 (needs real `ActionRequest`s to classify).

**Expected output:** Every existing SAFE action now visibly passes through the risk gate (even though it still auto-executes); a temporary test-only MODERATE and DANGEROUS action (or reused stub) demonstrates the confirmation screens render correctly; a block-listed test phrase is refused with no confirmation shown at all.

**Testing requirements:** Table-driven tests for the full risk-tier table; block-pattern tests for every listed catastrophic pattern; a test asserting BLOCKED requests never reach the confirmation code path (structural test, not just an output check).

**Definition of done:**
- [ ] Risk tier for every currently-registered action matches [Architecture.md](./Architecture.md) §7 exactly.
- [ ] MODERATE and DANGEROUS confirmation screens render per [Design.md](./Design.md) and correctly cancel on decline.
- [ ] Every block-listed pattern is refused, unconditionally, with no path to override via confirmation.
- [ ] `run_argv()` is the only function in the codebase that calls `subprocess` for action execution (grep-verifiable).

**Do NOT attempt in this phase:** Building out the remaining 5 MODERATE/DANGEROUS actions themselves — this phase proves the *gate* works, not the full action list. Resist the urge to build `install_package` here just because the gate is ready; keep it to Phase 4 so this phase's tests stay focused.

---

## Phase 4 — Privileged Execution: Packages & Services
**Target: Day 3 – Day 4 (first half)**

**Objective:** Implement the two DANGEROUS/privileged actions — the ones that make the demo's centerpiece possible (a real `apt install`, a real `systemctl restart`) — now that the gate they run through is proven.

**Features/components implemented:**
- `core/package_manager.py`: `PackageManager` protocol + `AptPackageManager`
- `actions/packages.py`: `install_package` (git, google-chrome, python3, nodejs as the supported package names for MVP)
- `core/service_manager.py`: `ServiceManager` protocol + `SystemctlServiceManager`
- `actions/services.py`: `service_control` (start/stop/restart), restricted to an explicit service allowlist (nginx, +1 if time allows)
- Verification for both: package presence/version check; `systemctl is-active` check

**Dependencies:** Phase 3 (these are DANGEROUS actions and must go through the completed gate; building them earlier would mean executing privileged commands with no gate in front of them, which [Rules.md](./Rules.md) forbids even temporarily).

**Expected output:** `install git`, `install chrome`, `install python`, `install node`, `start/stop/restart nginx` all work end-to-end on a real Ubuntu VM, each requiring the DANGEROUS-tier explicit confirmation and each verified afterward.

**Testing requirements:** `plan()` argv tests for both actions (confirm exact command construction, confirm `sudo` only appears via the executor, not embedded in the action); manual runs on a clean Ubuntu VM/snapshot for each supported package and each service action.

**Definition of done:**
- [ ] All four install targets succeed and verify correctly on a clean VM.
- [ ] All three service operations (start/stop/restart) succeed and verify correctly.
- [ ] A deliberately wrong package name produces a clear, plain-language failure (not a crash, not a false success).
- [ ] `service_control` rejects any service name outside its allowlist before constructing a command.

**Do NOT attempt in this phase:** Fedora/`dnf` support; an unrestricted service name parameter; any package outside the four listed. If time is short, cut to git + chrome + python (drop nodejs) before cutting anything from Phase 3.

---

## Phase 5 — Moderate Filesystem & Dev-Environment Actions
**Target: Day 4 (second half)**

**Objective:** Round out the action registry to the 8–10 target with the remaining MODERATE-tier actions, which are lower-risk to build now that the pattern is well-established from Phase 4.

**Features/components implemented:**
- `actions/filesystem.py`: `create_folder`, `move_files` (pattern-based, e.g. `*.pdf` → target directory)
- `actions/dev_env.py`: `create_venv`
- Verification for each per [Architecture.md](./Architecture.md) §14

**Dependencies:** Phase 3 (gate) — these are MODERATE tier so single-confirm, but still go through the same gate.

**Expected output:** `create a folder called projects`, `move all pdf files to documents`, `create a python virtual environment` all work end-to-end with correct MODERATE-tier confirmation.

**Testing requirements:** `plan()`/`verify()` tests per action; an injection test specifically for `create_folder`/`move_files` (folder name containing shell metacharacters must be treated as a literal, per [Rules.md](./Rules.md) §1.4).

**Definition of done:**
- [ ] All three actions work end-to-end and verify correctly.
- [ ] `move_files` does not overwrite an existing destination file silently (at minimum: skip and report, rather than clobber).
- [ ] Injection test passes for both filesystem actions.

**Do NOT attempt in this phase:** Recursive/glob-unbounded move operations beyond a single documented pattern type; multi-destination moves; any attempt to make `create_folder` accept absolute paths outside the user's home directory (keep the MVP scoped to the user's own filesystem area).

---

## Phase 6 — Verification, Hardening & Testing Pass
**Target: Day 5**

**Objective:** This is the schedule's only slack day. Its job is to make sure everything built in Phases 1–5 is actually reliable, not to build new features.

**Features/components implemented:**
- Full risk-table and injection test suite finalized and passing
- One full run-through of every registered action on a freshly snapshotted Ubuntu VM, restored to clean state before running
- Error-message pass: confirm every failure mode (declined, execution failure, verification failure) produces the correct plain-language message per [Design.md](./Design.md)
- **Only if this finishes early:** the first nice-to-have from [PRD.md](./PRD.md) §16 (JSONL history log) may be added — nothing else.

**Dependencies:** Phases 1–5 complete.

**Expected output:** A clean VM snapshot on which all 10 actions can be run, in sequence, from a written test script, with no manual workarounds.

**Testing requirements:** This entire phase *is* the testing requirement. Every action from the registry gets exercised at least once against real system state in this phase, not just against mocks.

**Definition of done:**
- [ ] Full `pytest` suite passes.
- [ ] Every registered action has been run, at least once, against a real clean Ubuntu VM/snapshot in this phase (not earlier ad hoc testing).
- [ ] At least one deliberate failure case per privileged action has been observed to produce a correct, non-crashing, plain-language error.
- [ ] No known open bug affects any of the 6 demo scenarios in [Design.md](./Design.md)/demo script.

**Do NOT attempt in this phase:** New actions, new risk tiers, refactors "while we're in here," or any nice-to-have beyond the single one named above. If Phase 6 starts late because an earlier phase overran, everything in the "only if this finishes early" line is the first thing dropped — see the reduction ladder below.

---

## Phase 7 — Demo Readiness
**Target: Day 6**

**Objective:** Turn a working system into a working, rehearsed, resilient-to-Murphy's-law demo.

**Features/components implemented:**
- Demo script finalized (safe action → moderate action → install → service restart → blocked refusal, per [PRD.md](./PRD.md)/[Design.md](./Design.md))
- Demo VM/environment pre-warmed: `apt` cache populated for the demo packages, passwordless `sudo` configured for the demo user for the specific demo actions, network dependency minimized where possible
- README written (what it is, how to run it, the safety model, in that order)
- Backup recording of a full successful demo run, in case live execution fails at the event

**Dependencies:** Phase 6 complete — no new functional work happens in Phase 7.

**Expected output:** Two consecutive successful full run-throughs of the demo script on the actual demo machine/VM.

**Testing requirements:** The demo script itself, run twice, is the test. Any failure sends the relevant fix back through a normal (small, tested) change — not a live patch during rehearsal.

**Definition of done:**
- [ ] Demo script runs successfully twice in a row, unattended between runs (fresh VM state each time, matching how the actual demo will run).
- [ ] README exists and accurately describes current, real functionality only.
- [ ] Backup recording exists.
- [ ] No pending `TODO`/`FIXME` in any of the 10 registered actions' core paths.

**Do NOT attempt in this phase:** Any code change that isn't fixing a defect found in rehearsal. This is not the time to add an 11th action.

---

## Scope Reduction Ladder

If the schedule slips, cut **in this order** — later items are cut only after all earlier items have already been cut:

1. Nice-to-have JSONL history log (never build if any earlier phase is behind).
2. Second demo service beyond nginx in `service_control`.
3. `nodejs` as a fourth `install_package` target (keep git, chrome, python).
4. `move_files` action (drop to 9 actions; RAM/CPU/disk/find/top/create_folder/create_venv/install_package/service_control still cover the demo's core arc).
5. `show_top_processes` (drop to 8 actions if truly necessary).

**Never cut, at any point, regardless of schedule pressure:** the risk gate (Phase 3), the block-pattern list, the argv-only execution rule, or verification for whichever actions remain. A 6-action demo with a real, tested safety gate and real verification is a materially better hackathon submission than a 10-action demo with a shortcut taken anywhere in [Rules.md](./Rules.md) §1.
