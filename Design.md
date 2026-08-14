# Design.md — LinuXpert Terminal Experience Design

**Status:** MVP planning — pre-implementation
**Companion documents:** [PRD.md](./PRD.md), [Architecture.md](./Architecture.md), [Rules.md](./Rules.md), [Phases.md](./Phases.md)

LinuXpert is CLI-first for the MVP; this document specifies the terminal experience as rigorously as a web product spec would treat a UI. No web/GUI design is included — it is out of scope (see [PRD.md](./PRD.md) §17).

---

## 1. Product Personality

LinuXpert should feel like **a careful senior engineer looking over your shoulder** — not a chatbot, not a hacker-movie terminal, not a corporate dashboard squeezed into a console. It talks like a tool, not a persona: no name, no chit-chat, no exclamation marks for routine success. The one place personality is allowed to show is in how clearly and calmly it explains a refusal — confidence without alarm.

**Is:** modern, technical, professional, trustworthy, developer-focused, legible at a glance.
**Is not:** playful, verbose, gamified, "AI assistant with a face," decorated with unnecessary ASCII art or emoji.

---

## 2. CLI Visual Identity

### Palette

Color is the primary carrier of risk/status meaning, so the palette is built around **four semantic states** plus one neutral/brand tone — kept deliberately distinct from each other so risk tier is legible even to someone glancing at the screen, not reading closely.

| Role | Use | ANSI / `rich` name | Notes |
|---|---|---|---|
| Brand / prompt | The `LinuXpert >` prompt itself, headers | `bold cyan` | Cool, technical, not tied to any risk state — so it never gets confused with a status color |
| Safe | Safe-tier results, success confirmations | `green` | Standard "good" signal, used sparingly (only on the checkmark/summary line, not whole paragraphs) |
| Moderate | Moderate-tier plan previews, warnings | `yellow` / `bright_yellow` | Caution, not alarm |
| Dangerous / privileged | Dangerous-tier plan previews, sudo notices | `bold red` on plan text, not background | Reserved — never used for anything below dangerous tier, so its appearance alone is meaningful |
| Blocked | Blocked-request refusals | `bold white on red` (inverse block) | The one state allowed a filled background — it should look structurally different from every other screen, not just differently colored |
| Neutral text | Body text, explanations | default terminal foreground | Don't fight the user's terminal theme unnecessarily |
| Muted | Secondary detail (paths, timestamps, argv preview) | `dim` / `grey62` | De-emphasized without being unreadable |

Rule: **color always pairs with a symbol or word**, never color alone (accessibility — some terminals/users have limited color, and monochrome demo projectors are a real hackathon risk). `✓` / `!` / `✗` / `⛔` carry the meaning; color reinforces it.

### Typography / terminal formatting

- Monospace only (it's a terminal — no choice to make, but worth stating: don't fight it with box-drawing characters that misalign on narrower terminals).
- **Bold** for: the resolved action name, the risk-tier word, and the final result headline. Nothing else gets bold — overuse defeats the purpose.
- Indentation (2 spaces) marks "detail belonging to the previous line" — plan fields, sub-results — so structure is visible without heavy rules/boxes.
- No box-drawing borders (`┌─┐`) for routine output — they add visual weight without adding information at this content density. The one place a full-width rule is earned is the BLOCKED screen, where visual weight is the point.
- Line width: don't hardcode 80-column wrapping; let the terminal wrap naturally, but keep individual label/value lines short enough that they don't wrap on a standard 100-column terminal.

### Prompt style

```
LinuXpert >
```

- Prompt text is always `LinuXpert > ` (brand color, bold), followed by the user's typed text in default terminal color.
- No trailing decoration (no `$`, no emoji, no version number in the prompt itself — that belongs in a one-time startup banner, not every line).

### Headers

- No headers within a single request/response cycle — each interaction is short enough not to need internal sectioning.
- The one-time startup banner (shown once when `linuxpert` launches) is minimal:
```
LinuXpert — natural-language Linux assistant
Detected: Ubuntu 22.04 (apt)   |   type 'help' for supported actions
```

### Status indicators (symbol vocabulary)

| Symbol | Meaning | Used with |
|---|---|---|
| `✓` | Success / verified | green |
| `!` | Warning / verification mismatch | yellow |
| `✗` | Failure (execution error, or user declined) | default/dim, not red (red is reserved for dangerous/blocked *previews*, not neutral declines — see §"Failed operation" below) |
| `⛔` | Blocked (unconditional refusal) | bold white on red |
| `…` | In progress | dim, paired with a `rich` spinner |

---

## 3. Message Types

### Success messages
- Format: `✓ <what happened>` then, if verified, a second line `✓ verified: <how we know>`.
- Plain past tense, factual: "installed", "created", "restarted" — not "Successfully installed!" or similar filler.

### Warning messages
- Format: `! <what's uncertain>` in yellow — used specifically for the "executed but verification failed" case from [Architecture.md](./Architecture.md) §15. Never reuse the green `✓` for this case, even partially.

### Error messages
- Format: `✗ <what went wrong>` followed by, when available, a one-line plain-language likely cause ("package name not recognized — did you mean 'chromium-browser'?").
- Never a raw stack trace or raw subprocess stderr dump in normal operation. A `--debug` flag exposes the raw detail for developers.

### Risk indicators
Shown as a labeled field in every plan preview (moderate/dangerous), not as freestanding text:
```
  risk      moderate
```
or
```
  risk      dangerous · privileged (sudo required)
```
The word itself (`moderate`/`dangerous`) is colored per §2; the field label (`risk`) stays neutral/dim so the colored value is what draws the eye.

### Confirmation screens
See §4 for full examples. Structural rule: **every confirmation screen shows the actual resolved action, its parameters, and the real command(s) from `plan()`** — never a paraphrase. The user is confirming reality, not marketing copy.

### Blocked-operation screens
Structurally distinct (inverse-color band, `⛔` symbol, no `Proceed?` prompt at all — the absence of a yes/no prompt is itself part of the design, communicating "this isn't a decision you get to make here").

### Progress indicators
- A `rich` spinner with a short present-participle label (`Installing…`, `Restarting nginx…`) for any action expected to take more than ~1 second (package installs, service restarts).
- No spinner for actions that resolve near-instantly (RAM/CPU/disk reads) — a spinner there would read as latency, not progress.

### Help output
`help` (or unrecognized input) lists the registered actions grouped by category, each with one example phrase — not a full man-page. This doubles as the honest list of "what LinuXpert can actually do," which matters for a system that deliberately refuses unmapped requests.

### Result formatting
- One blank line separates each full request/response cycle, none within one.
- Multi-field results (e.g. disk usage across mounts) use aligned two-column layout via `rich.table` with no visible borders — alignment carries the structure, not ruled lines.

---

## 4. Example CLI Screens

Colors are noted in `[brackets]`; assume `rich` markup renders them in an actual terminal.

### 1. Safe operation

```
LinuXpert > show my ram usage
[green]✓[/green] RAM: 6.2 GB used / 16.0 GB total (39%)
```

### 2. Moderate-risk operation

```
LinuXpert > create a folder called projects
  action     create_folder
  target     ~/projects
  risk       [yellow]moderate[/yellow]

  Proceed? [y/N] y

[green]✓[/green] created ~/projects
[green]✓[/green] verified: directory exists
```

### 3. Privileged (dangerous) operation

```
LinuXpert > install git
  action     install_package
  target     git
  method     apt
  command    sudo apt-get install -y git
  risk       [bold red]dangerous[/bold red] · privileged (sudo required)

  Type 'yes' to proceed: yes

  … Installing[dim] (this may take a moment)[/dim]

[green]✓[/green] installed
[green]✓[/green] verified: git version 2.43.0
```

### 4. Blocked dangerous operation

```
LinuXpert > delete everything from my computer

[bold white on red] ⛔  BLOCKED [/bold white on red]
  This request matches a destructive-operation pattern and will not run,
  regardless of confirmation.

  If you meant something narrower, try rephrasing — e.g.
  "remove old kernel packages" or "empty the trash".
```

### 5. Failed operation

```
LinuXpert > install chorme
  action     install_package
  target     chorme
  method     apt
  command    sudo apt-get install -y chorme
  risk       [bold red]dangerous[/bold red] · privileged (sudo required)

  Type 'yes' to proceed: yes

  … Installing

[dim]✗[/dim] failed — package 'chorme' not found
  Did you mean: google-chrome?
```

### 6. Successful verification (explicit "verified" moment)

```
LinuXpert > restart nginx
  action     service_control
  target     nginx (restart)
  command    sudo systemctl restart nginx
  risk       [bold red]dangerous[/bold red] · privileged (sudo required)

  Type 'yes' to proceed: yes

  … Restarting nginx

[green]✓[/green] restart command completed
[green]✓[/green] verified: nginx is active (systemctl is-active → active)
```

---

## 5. Cross-cutting rules

- Every screen that leads to system-changing execution shows **action, target, and the literal command** before anything runs — no exceptions, matching [Rules.md](./Rules.md) §1's "no hidden execution" principle at the UI layer, not just the code layer.
- The visual weight of a screen should scale with its risk tier: safe is one line, moderate is a short block, dangerous is a fuller block with an explicit typed confirmation, blocked is visually unmissable even out of the corner of your eye. This is a deliberate redundancy with the color-coding, not decoration.
- Never let a spinner or "in progress" state be the last thing shown if something fails — always resolve to a final `✓` / `!` / `✗` line.
