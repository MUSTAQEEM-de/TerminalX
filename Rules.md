# Rules.md — Development & AI Agent Rules

**Status:** Binding for all development on LinuXpert, human or AI.
**Companion documents:** [PRD.md](./PRD.md), [Architecture.md](./Architecture.md), [Phases.md](./Phases.md), [Design.md](./Design.md)

These rules exist to keep a 6-day hackathon build from quietly becoming the unsafe system this project was explicitly designed not to be. When a rule here and a shortcut conflict, **the rule wins.** If a rule seems to block a needed feature, the fix is to raise it and document a change — not to route around it silently (see §4).

---

## 1. Security Rules (non-negotiable)

1. **Never allow unrestricted arbitrary shell execution.** There is no code path, flag, or mode in which raw user text or raw LLM text is passed to a shell for execution.
2. **The LLM never executes commands.** Its only output is a structured tool call selected from the fixed action registry. There is no "fallback" that runs an LLM-authored shell string, ever — not even for unmapped requests.
3. **Never use `shell=True`** for action execution. All `subprocess` calls use argument lists (`subprocess.run([...], shell=False)`).
4. **Never interpolate untrusted input into a command string.** User-supplied values (folder names, file patterns, package names) are passed as discrete argv elements, never through f-strings/`.format()`/concatenation into a command line.
5. **Validate action names against the registry.** If the LLM (or anything else) references an action name not present in the registry, treat it as "no matching action" — never execute, never guess.
6. **Validate action parameters** against each action's own schema (type, format, allowed characters) in application code, independent of whatever validation the LLM claims to have done. LLM output is untrusted input.
7. **Risk classification is deterministic and code-owned.** Risk tier comes from a static lookup table keyed by action name (and, where defined, parameter shape) — never from the LLM's stated opinion of its own request's risk.
8. **The LLM must not determine its own permission/risk level.** Don't add a field like `"risk": "safe"` to the LLM's tool response and trust it. If such a field exists for prompting purposes, it is discarded on receipt.
9. **Privileged operations must be explicit.** Any action that needs `sudo` declares `requires_sudo=True` in its registry entry, and the confirmation screen states this before any password prompt appears.
10. **Dangerous operations require appropriate confirmation, or are blocked.** No dangerous-tier action executes without an explicit, typed confirmation (not a bare Enter/default-yes).
11. **Catastrophic operations must be blocked, unconditionally.** The block-pattern list (root/home recursive delete, disk-wipe utilities, fork bombs, remote-script-piped-to-shell patterns) cannot be overridden by any confirmation flow. If a request matches, no confirmation UI is even shown.
12. **Never silently grant root privileges.** `sudo` is invoked in exactly one place in the codebase (the executor, per [Architecture.md](./Architecture.md) §10), only when the action's `requires_sudo` flag is set, and only after confirmation. No action implementation embeds its own `sudo` call.

If you (the coding agent) find yourself about to violate one of these to make a feature work, **stop and say so explicitly** rather than finding a workaround. This applies even under time pressure — especially under time pressure.

---

## 2. Coding Rules

### Language & tooling
- **Python 3.11+**, no other language in the core app.
- **Type hints on all function signatures** (params and return types). Use `dataclasses` or `TypedDict` for structured data (`ActionRequest`, `ActionResult`, etc.) rather than bare dicts passed around loosely.
- Use `pyproject.toml` for dependency and project metadata. Pin dependency versions loosely (`>=`) but keep the dependency list itself minimal — see [Architecture.md](./Architecture.md) §19 for the approved stack.

### Code organization
- Follow the folder structure in [Architecture.md](./Architecture.md) §20. New files go where that structure implies; don't invent a parallel structure.
- One action = one function/class in the relevant `actions/*.py` module. Don't split a single action's `plan`/`run`/`verify` across files.
- `nlu/` code must never import `subprocess` or anything from `core/executor.py`. `actions/` code must never call `subprocess` directly — only through `core/executor.py` or the manager abstractions. This import boundary is how the security boundary stays enforceable by inspection.

### Naming conventions
- Action names are `snake_case` verbs matching the registry table in [Architecture.md](./Architecture.md) §7 exactly (`install_package`, not `installPackage` or `do_install`).
- Risk tiers are the `RiskTier` enum values `SAFE`, `MODERATE`, `DANGEROUS` — spelled exactly this way everywhere (docs, code, CLI output) so grepping/cross-referencing works.
- Modules, functions, variables: standard PEP 8 (`snake_case` for functions/variables, `PascalCase` for classes).

### Error handling
- Every `subprocess` call site handles both non-zero exit and exceptions (timeout, `FileNotFoundError` for a missing binary) — no bare `except:`; catch specific exceptions.
- User-facing errors are plain language (see [Design.md](./Design.md) for exact formatting). Raw tracebacks are never shown in normal operation; a `--debug` flag may enable them.
- Distinguish, in both code and messaging, between "declined/blocked" (not an error), "execution failed" (an error), and "executed but verification failed" (a warning) — see [Architecture.md](./Architecture.md) §15.

### Logging
- Use the standard library `logging` module, not `print`, for internal diagnostics. User-facing CLI output goes through the dedicated rendering layer in `cli.py`, not through logging calls.
- Log at minimum: every resolved `ActionRequest`, its risk tier, the confirmation outcome, and the final `ActionResult`. This is useful for debugging even before/instead of the optional history feature.

### Configuration
- Constants (timeouts, the service allowlist, supported distro families) live in `linuxpert/config.py`. No hardcoded magic values scattered across action modules.
- No environment-variable-driven behavior changes to the security model (e.g. no `LINUXPERT_UNSAFE_MODE` env var, ever, under any justification).

### Dependency management
- New dependencies require a one-line justification in the PR/commit message (why existing stack can't do it). Default answer to "should we add a new dependency" is no.
- No dependency that itself shells out unpredictably or wraps command execution in ways that reintroduce string-based execution.

### Testing
- Every action gets at minimum: a `plan()` test asserting the exact argv produced for representative parameters, and a `verify()` test with both a passing and failing fixture.
- The risk classifier and block-pattern matcher get table-driven tests covering the full action list plus adversarial phrasings (see [Phases.md](./Phases.md) testing sections).
- Injection tests assert that a crafted parameter value (e.g., a folder name containing `; rm -rf ~`) appears as a single literal argv element and is never split/interpreted.
- Tests run via `pytest`; a failing test blocks a commit that touches the code it covers (see §4).

### Documentation
- Every action's docstring states: what it does, its parameter schema, its risk tier, and its verification approach — this docstring is also the source for the LLM tool-spec description, so keep it user-facing, not implementation-facing.
- Non-obvious decisions get a one-line comment explaining *why*, not *what* (the code already says what).

### Simplicity / avoiding unnecessary abstraction
- No abstract base classes, plugin loaders, or dependency-injection frameworks for a 10-action registry. A `Protocol` and a flat list is enough (see [Architecture.md](./Architecture.md) §6–7).
- Don't build configurability for scenarios outside the MVP (multi-distro, multi-user, remote execution) — write the code for what's actually being shipped, not for a hypothetical v2. When v2 needs it, it gets designed then, informed by what v1 actually needed.
- Three similar lines of code across actions is fine. Don't extract a shared abstraction until a third, real use case demands it.

---

## 3. AI Coding Agent Behavior Rules

- **Do not invent APIs or libraries.** If unsure whether a function/parameter exists (in `psutil`, the Anthropic SDK, etc.), check the actual installed version's docs/signature rather than guessing from training data.
- **Do not modify the architecture without documenting the reason.** Any deviation from [Architecture.md](./Architecture.md) (different risk tier for an action, a new component, a changed folder structure) gets a note in the commit message and, if material, a corresponding edit to the architecture doc itself — the docs and the code must not drift apart.
- **Do not introduce unnecessary dependencies.** See §2 Dependency management.
- **Do not expand MVP scope without approval.** The action registry in [Architecture.md](./Architecture.md) §7 and the feature list in [PRD.md](./PRD.md) §16 are the scope. Adding an 11th action, a new risk tier, or a new distro mid-build is a scope change — flag it, don't just build it.
- **Do not remove or weaken a security control to make a feature easier to ship.** If a feature seems to require weakening §1, the feature is wrong for this MVP, not the rule.
- **Do not claim a feature works without testing it.** "Implemented" and "verified working" are different claims — only make the second after actually running the code path (unit test and, where practical, a real command against a test VM/environment).
- **Do not silently change requirements.** If something in the PRD/Architecture turns out to be impractical within the 6-day window, say so explicitly and propose the smallest change, rather than quietly building something different from what's documented.
- **Prefer existing project conventions** (naming, structure, patterns already established in earlier files) over introducing a new style partway through the build.
- When multiple approaches are reasonable, **prefer the one that's easier to verify and test** over the one that's more "elegant" or general.

---

## 4. Git / Development Workflow Rules

Kept intentionally light for a solo/small-team hackathon — process should never be the bottleneck, but a few habits pay for themselves even at this size.

- **Commit early and often**, in small units that each represent one coherent change (one action added, one bug fixed) — not one giant end-of-day commit.
- **Write commit messages that state what changed and why** in one line; a body paragraph only when the "why" isn't obvious from the message + diff.
- **Run relevant tests before committing** anything that touches `actions/`, `core/risk.py`, or `core/executor.py` — these are the security-load-bearing modules; nothing here ships untested, even under deadline pressure.
- **A single `main` branch is fine** for a solo build; use a short-lived branch only if trying something that might not work out (e.g. experimenting with the LLM tool-use prompt) and you want `main` to stay demo-safe in the meantime.
- **Document significant architectural changes** (see §3) in the relevant `.md` file in the same work session as the code change, not "later."
- **Never commit secrets** (API keys) — use environment variables / a local `.env` excluded via `.gitignore`, from the very first commit.
- Before the demo day, **tag or note the exact commit used for the demo** so a last-minute change can't accidentally destabilize what was rehearsed.
