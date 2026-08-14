# PRD.md — LinuXpert Product Requirements Document

**Status:** MVP planning — pre-implementation
**Timeline:** ~6-day hackathon build
**Companion documents:** [Architecture.md](./Architecture.md), [Rules.md](./Rules.md), [Phases.md](./Phases.md), [Design.md](./Design.md)

---

## 1. Product Name

**LinuXpert** — an AI-powered Linux assistant that lets users control and manage their Linux system using natural language instead of memorizing shell commands.

---

## 2. Product Overview

LinuXpert is a CLI tool. The user runs `linuxpert`, gets a `LinuXpert >` prompt, and types what they want in plain English (e.g. "install git", "show my RAM usage", "restart nginx"). LinuXpert interprets the request, maps it to one of a small, fixed set of supported system actions, checks whether the action is safe enough to run automatically or needs confirmation, executes it safely on the local machine, verifies the outcome actually happened, and reports the result in plain language.

LinuXpert is explicitly **not** a general-purpose "LLM writes and runs a shell command" tool. It supports a closed set of well-tested actions rather than unbounded shell access. This is a scope decision as much as a safety decision: a small, reliable action set is achievable in six days; an open-ended shell-command generator is not — no code the LLM freely writes on a hackathon night, and no test suite in six days, can be trusted to run on a real machine.

---

## 3. Problem Statement

Linux is powerful but command-driven. Many users — especially newer developers, students, and people migrating from GUI-first operating systems — know the outcome they want ("I want Git installed") but not the mechanism (`sudo apt install git`, correct package name, whether a repo needs adding, whether the service needs a restart afterward). This gap causes friction, incorrect commands copy-pasted from random web pages, and in the worst case, destructive mistakes from commands the user didn't fully understand.

## 4. Problem Context

- Command syntax varies by tool and by distribution (package manager, service manager, flags).
- Search-and-copy-paste from forums/StackOverflow/AI chat is the current workaround, and it routinely produces subtly wrong or dangerous commands with no safety check before execution.
- Existing "AI does my terminal for me" tools tend to solve this by having an LLM generate and directly execute shell strings — which reintroduces the danger it was supposed to remove.
- There is a real gap for a tool that keeps the "just tell it what you want" convenience while adding a genuine safety boundary between intent and execution.

---

## 5. Target Users

- **Students / Linux newcomers** who know what outcome they want but not the correct command.
- **Developers on unfamiliar machines** (a fresh VM, a new laptop, a remote box) who want common setup tasks done quickly without looking up syntax.
- **Hackathon judges / technical evaluators** (for this build specifically) assessing both the concept and the safety architecture as the differentiator.

Out of scope for MVP: system administrators managing fleets, non-technical end users with zero command-line comfort, enterprise/regulated environments.

---

## 6. User Pain Points

- Doesn't remember exact package names or install flags across tools.
- Doesn't know which package manager or service manager the current distro uses.
- Unsure whether elevated privileges are required, or what a command will actually do before running it.
- No easy way to confirm an operation actually worked (e.g., "did nginx actually restart?").
- Fear of destructive mistakes when copy-pasting unfamiliar commands.

---

## 7. Product Vision

Make everyday Linux system operations accessible through natural language, without ever giving up the safety guarantees a careful engineer would want before running something on their own machine. Long-term, LinuXpert becomes the default way non-expert (and expert-but-busy) users perform common local system tasks — but the MVP's job is to prove the *safety-first natural-language-to-action* model works convincingly on one distro family with a small, reliable action set.

---

## 8. Product Goals

1. Prove that natural language can be reliably mapped to a small set of structured, safe system actions.
2. Prove that a deterministic risk/confirmation gate — not the LLM's own judgment — can sit between intent and execution.
3. Ship a CLI that is demoable live, end to end, with no smoke and mirrors.
4. Keep the implementation small enough to be fully working and tested within ~6 days.

---

## 9. MVP Objectives

- 6–10 fully working, verified actions covering install, system-info, filesystem, and service-management categories.
- A working 4-tier risk model (SAFE / MODERATE / DANGEROUS-PRIVILEGED / BLOCKED) enforced in application code.
- Ubuntu/Debian (`apt`) support only.
- Every action verified after execution — success is reported only when the real system state confirms it.
- A demo script that includes at least one live, on-screen safety refusal.

---

## 10. Core User Experience

```
$ linuxpert
LinuXpert > show my ram usage
✓ RAM: 6.2 GB used / 16.0 GB total (39%)

LinuXpert > install git
  action     install_package
  target     git
  method     apt
  privilege  sudo required
  Proceed? [y/N] y
  ✓ installed   ✓ verified: git version 2.43.0

LinuXpert > delete everything from my computer
  ✗ blocked — this matches a destructive-operation pattern and will not run.
```

The experience is: type intent → see exactly what will happen before anything risky runs → get a plain-language, verified result.

---

## 11. Key Use Cases

1. Install common developer tools (Git, Python, Node.js, Chrome) without knowing package names or `apt` syntax.
2. Check system resource usage (RAM, CPU, disk) without remembering `free`, `top`, `df` flags.
3. Find large files eating disk space without constructing a `find` command.
4. Create a folder or a Python virtual environment with one sentence.
5. Move files by type (e.g., all PDFs) into a target folder.
6. Start, stop, or restart a known service (nginx) without remembering `systemctl` syntax.
7. See which processes are consuming the most CPU.
8. Be stopped, clearly and immediately, from accidentally issuing a catastrophic system command.

---

## 12. Example User Interactions

| User says | Resolved action | Risk tier |
|---|---|---|
| "Install Git" | `install_package(name="git")` | Dangerous (privileged) |
| "Install Chrome" | `install_package(name="google-chrome")` | Dangerous (privileged) |
| "Install Python" | `install_package(name="python3")` | Dangerous (privileged) |
| "Show my RAM usage" | `show_ram_usage()` | Safe |
| "Show my CPU usage" | `show_cpu_usage()` | Safe |
| "How much disk space do I have?" | `show_disk_usage()` | Safe |
| "Find files larger than 1 GB" | `find_large_files(min_size="1GB")` | Safe |
| "Create a folder called projects" | `create_folder(name="projects")` | Moderate |
| "Move all PDF files to Documents" | `move_files(pattern="*.pdf", destination="Documents")` | Moderate |
| "Restart nginx" / "Start nginx" / "Stop nginx" | `service_control(name="nginx", action="restart\|start\|stop")` | Dangerous (privileged) |
| "Create a Python virtual environment" | `create_venv(path=".venv")` | Moderate |
| "Show which processes use the most CPU" | `show_top_processes()` | Safe |
| "Delete everything from my computer" | *(no match — pattern-blocked)* | Blocked |

---

## 13. Functional Requirements

- FR1: Parse a free-text user request into a structured action call selected from a fixed action registry.
- FR2: Reject/decline requests that do not map to a registered action, with a clear explanation — never fall back to executing an LLM-authored raw command.
- FR3: Detect the local Linux distribution and confirm it is a supported family (Ubuntu/Debian) before offering privileged actions.
- FR4: Classify every resolved action's risk tier via static, code-owned lookup — not LLM self-assessment.
- FR5: Execute SAFE actions immediately; require explicit confirmation for MODERATE and DANGEROUS actions; unconditionally refuse BLOCKED requests.
- FR6: Execute all system-modifying commands via argument-list subprocess calls — never shell-string interpolation.
- FR7: Verify the real post-condition of every executed action (not just exit code) and report success only when verification passes.
- FR8: Report results in plain language, including partial failures and verification mismatches.
- FR9: Provide a help/list-of-supported-actions output so users know what LinuXpert can currently do.

## 14. Non-Functional Requirements

- NFR1: Runs on a stock Ubuntu/Debian desktop or VM with Python 3.11+ and no exotic system dependencies.
- NFR2: Each action completes and reports within a few seconds for local operations; installs bounded by network/package-manager time, with clear in-progress feedback.
- NFR3: CLI output is legible, consistent, and clearly encodes risk/status (see [Design.md](./Design.md)).
- NFR4: The codebase stays small enough for one person to hold in their head — no framework or abstraction whose payoff arrives after day 6.
- NFR5: Errors from the OS/package manager are surfaced in plain language, not raw stack traces, in normal operation.

## 15. Security Requirements

- SR1: The LLM never executes anything directly. It only ever returns a structured action name + parameters chosen from the registry (enforced via tool-calling / function-calling with a fixed schema).
- SR2: All parameters returned by the LLM are re-validated against the action's own parameter schema in code before use — the LLM's output is treated as untrusted input, not a trusted plan.
- SR3: Risk tier is a static property of the action (and, where relevant, its parameters), assigned by code — never inferred from the model's own judgment of danger.
- SR4: No command is ever built via string concatenation/interpolation of user input; all execution uses argument lists (`subprocess.run([...], shell=False)`).
- SR5: Actions requiring elevated privileges declare this explicitly in the registry and say so on the confirmation screen before any password prompt appears.
- SR6: A hard-coded block list of catastrophic patterns (recursive delete of `/` or home directory, disk-wipe utilities, fork bombs, remote-script-piped-to-shell patterns) is checked ahead of everything else and cannot be overridden by user confirmation.
- SR7: Any request that does not map to a registered action is refused with an explanation — the system never invents or runs an ad hoc command for an unmapped request.
- SR8: Every action defines a verification check; a result is only reported as successful when verification passes.

---

## 16. MVP Features

**MUST HAVE**
- REPL CLI (`linuxpert` → `LinuXpert >` prompt)
- 6–10 registered actions covering: package install (git, chrome, python3, node), RAM/CPU/disk usage, find large files, top CPU processes, create folder, move files by pattern, create venv, service control (start/stop/restart) for one demo service (nginx)
- Structured intent parsing constrained to the action registry (LLM tool-use)
- Ubuntu/Debian distro detection + `apt` execution
- 4-tier risk model (safe / moderate / dangerous-privileged / blocked) with static, code-owned classification
- Confirmation flow for moderate & dangerous tiers
- Hard-coded block list for catastrophic patterns, unconditionally enforced
- Post-execution verification for every action
- Argument-list-only subprocess execution
- Plain-language result reporting, including failures

**NICE TO HAVE**
- Local JSONL log of executed actions (append-only, no query UI needed)
- `--dry-run` flag that prints the plan without executing
- A second demo service beyond nginx (e.g. a second `systemctl`-managed service)
- Friendlier "closest supported action" suggestion when an unmapped request is refused

**FUTURE (explicitly out of scope for this build)**
- Fedora/`dnf`, Arch/`pacman`, or any cross-distro parity
- Web dashboard, mobile app, or voice interface
- Remote execution / multi-machine control
- Multi-user accounts / authentication
- Undo/rollback engine
- Plugin system for community-contributed actions
- Freeform/unbounded shell command generation in any mode
- Persistent database, cloud sync, or telemetry

---

## 17. Explicitly Out-of-Scope Features (MVP)

Everything under FUTURE above, plus:
- Any action not in the registry at launch (no ad hoc extensibility mid-demo).
- Any multi-step/compound request handling ("install node and create a project folder" as one request) — each request maps to exactly one action in the MVP.
- Any attempt to "learn" or adapt action behavior at runtime.

---

## 18. Success Criteria

- A user can perform all 13 example requests from the project brief (mapped onto the 6–10 registered actions) via natural language, end to end, on a clean Ubuntu VM.
- At least one destructive-sounding request is demonstrably blocked, live, with a clear on-screen explanation.
- No action ever executes via raw shell-string interpolation anywhere in the codebase (verifiable by code review / grep for `shell=True`).
- Every implemented action has a working verification check that can actually fail (i.e., it checks real state, not just exit code).

## 19. MVP Acceptance Criteria

- [ ] All MUST HAVE features above are implemented and manually tested on a clean Ubuntu/Debian VM.
- [ ] Risk classification for every registered action is reviewed and matches [Architecture.md](./Architecture.md) / [Rules.md](./Rules.md).
- [ ] The block list refuses at least the following without exception: recursive delete of `/`, recursive delete of the user's home directory, disk-wipe commands, fork bombs, `curl|bash`-style remote execution.
- [ ] Every action's verifier has been observed to correctly report both a pass and a plausible failure case during testing.
- [ ] The demo script (see [Phases.md](./Phases.md)) runs successfully twice in a row on the demo machine/VM.

## 20. Future Possibilities

Cross-distro support (Fedora/`dnf`, Arch/`pacman`), a companion web dashboard for audit/history (not a replacement for the CLI), voice input, an undo/rollback engine built on the existing verification layer, a plugin system for community-contributed actions using the same schema-and-risk-tier contract, and a policy configuration file for teams to tune confirmation requirements.
