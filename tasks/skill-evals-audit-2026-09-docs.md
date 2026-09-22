# Pièce jointe — Documentation officielle : evals de skills & frontmatter (fetch du 2026-09-22)

Rapport produit par un agent de recherche (general-purpose) lancé depuis la session
d'apprentissage du 2026-09-22, pour le brief `skill-evals-audit-2026-09-brief.md`.
Contenu reproduit tel quel (entités HTML décodées). Toute affirmation ci-dessous est
citée avec son URL ; re-vérifier avant de s'appuyer dessus dans le livrable.

---

**Method note.** `curl` and the `raw.githubusercontent.com` URLs were permission-denied in the research session, so every source was fetched through WebFetch, instructed to reproduce sections verbatim. skill-creator's `SKILL.md`, `references/schemas.md` and `agents/grader.md` were obtained from the `github.com/.../blob/...?plain=1` view (GitHub rendering inserted blank lines, which were collapsed; words unchanged).

---

## 1. `claude plugin eval` — https://code.claude.com/docs/en/plugin-evals.md

### 1a. Requirements
> "To run plugin evals you need:
> * Claude Code v2.1.269 or later. Run `claude --version` to check and `claude update` to upgrade.
> * A plugin directory with a `plugin.json` or `.claude-plugin/plugin.json` manifest, or a [skills-directory plugin].
> * The same authentication and model provider your normal Claude Code sessions use. Eval runs, judge-scored graders, and `claude plugin eval init` call the model with your credentials, so they count against your plan's usage limits or your API bill. When the command reports a cost, the figure is a list-price estimate of those calls."

No account tier or feature flag is listed as a requirement. The only flag-like items appear in Troubleshooting (`"plugin eval is currently in early access"` → build predates GA; `"plugin eval is currently unavailable"` → switched off server-side). Scope statement: "Its case format is separate from the `evals/evals.json` file the skill-creator plugin uses."

### 1b. "Choose what to evaluate" table (all rows)
> "Most of the time you run `claude plugin eval .` from the plugin root, which runs every case in the suite with the plugin you're standing in loaded."

| Target | What runs |
|---|---|
| A plugin's root directory, such as `.` | Every case under its eval directory, with that plugin loaded |
| A single `prompt.md` or `case.yaml` file | That case, with its enclosing plugin loaded |
| An installed plugin by name, `name` or `name@marketplace` | The cases in the installed copy's eval directory, with the installed copy loaded. Results are written under `./evals/results/` in your current directory, or `./<dir>/results/` with `--eval-dir` |
| `name@skills-dir` | The same, for a [skills-directory plugin](/docs/en/plugins-reference#skills-directory-plugins) |
| Omitted | The current directory as a path |

> "Add `--case <glob>` to filter by case name and `--tag <tag>` to keep cases with any of the given tags. Put the target before `--tag`, `--allow-tools`, and `--json`."

Also: "A target you name rather than give as a path, meaning an installed plugin or a skills-directory plugin, skips the [trust] prompt."

### 1c. Case formats

**Layout**: "A case is a directory under the plugin's eval directory that contains a `prompt.md`, a `case.yaml`, or both. To group cases, nest them under a directory that isn't itself a case; anything inside a case directory, such as `graders/` and fixture files, belongs to that case."

**`prompt.md` frontmatter** ("An unknown key is an error"):

| Field | Default | Purpose |
|---|---|---|
| `schema_version` | `"1.1"`, set for you | Case format version. Cases written as `prompt.md` get it automatically, so you rarely set it |
| `name` | The directory name | Case name. `--case` globs match it and the report keys on it |
| `description` | | For humans. Not used at run time |
| `tags` | `[]` | Labels for `--tag` filtering. A case runs if any of its tags matches |
| `plugins` | The nearest enclosing plugin | Plugin directories under test, relative to the case directory. Set `plugins: ["../.."]` when auto-detection doesn't find your plugin |
| `runs` | `3` | Runs per arm, 1 to 50. `--runs` overrides it |
| `expected_outcome` | | For humans. Not used at run time |
| `model` | The child session's default | Model for the agent under test. `--model` overrides it |
| `max_turns` | `10` | Turn cap, up to 200. Hitting it is recorded as a run error and usually lowers the score, so set it generously |
| `timeout_seconds` | `300` | Wall-clock cap per run, up to 3600 |
| `allowed_tools` | `[]` | Tools the case wants, such as `[Read, Glob, Grep, Skill]`. Read-only tools are granted when listed here; for anything else, see Grant tools |
| `append_system_prompt` | | Text appended to the child session's system prompt |
| `env` | `{}` | Extra environment variables for the child session. Keys must match `EVAL_[A-Z0-9_]*`; any other key fails the run. The run inherits only an allowlist from your shell: basics such as `PATH` and locale, proxy and certificate settings, the variables that select and authenticate your model provider, most `ANTHROPIC_*` and `CLAUDE_CODE_*` configuration, and `EVAL_*` |

"Claude receives the body exactly as you wrote it. `@path` mentions in it aren't expanded into file attachments."

**`case.yaml`**: "It requires `schema_version: "1.1"` and `name`. The `prompt.md` fields `description`, `tags`, `plugins`, `runs`, and `expected_outcome` go at the top level; `model`, `max_turns`, `timeout_seconds`, `allowed_tools`, `append_system_prompt`, and `env` go under `execution:`."

Fields that "exist only in `case.yaml`":

| Field | Purpose |
|---|---|
| `context.scaffold_script` | A Bash script in the case directory that runs in the empty workspace before Claude starts, to create fixture files or a git repository. It runs only when you pass `--scaffold` |
| `context.history_file` | A `.jsonl` transcript in the case directory to resume. The case's prompt becomes the next user turn |
| `context.add_dirs` | Directories inside the case directory that Claude may read during the run, granted read-only |
| `execution.prompt` | The prompt, when you keep the whole case in `case.yaml` and omit `prompt.md` |
| `graders` | A list of graders, each with a `name` plus the same keys a `graders/*.md` file takes in frontmatter. For `llm` graders, put the rubric in `criteria` |

**Precedence**: "When both files exist, `prompt.md` frontmatter overrides the matching `case.yaml` fields, the `prompt.md` body is the prompt, and `graders/*.md` are added after any graders listed in `case.yaml`."

**Grader file frontmatter** ("The grader's name is the filename without `.md`"):

| Key | Default | Purpose |
|---|---|---|
| `type` | required | One of the grader types |
| `weight` | `1` | Relative weight in the run's score. Any positive number |
| `arm` | unset | `with-only` excludes the grader from scoring in a two-arm run; `both` forces a `tool_used: Skill` grader to be scored in both arms |

### 1d. Grader types

| Type | Options | Passes when |
|---|---|---|
| `regex` | `pattern`, `flags`, `match`, `target` | The JavaScript regex `pattern` is found in the target. Set `match: not_contains` to require absence or `match: "count:N"` to require exactly N matches. Put case-insensitivity in `flags: i`; inline `(?i)` isn't supported |
| `tool_used` | `tool`, `input_match`, `min`, `max` | The number of calls to `tool` whose JSON-encoded input matches the optional `input_match` regex is between `min`, default 1, and `max`, default unlimited. To assert a tool was never called, set both `min: 0` and `max: 0` |
| `tool_order` | `before`, `after` | Both tools were called and the first matching `before` call precedes the first matching `after` call. Each is a tool name or `{ tool, input_match }` |
| `file_exists` | `path`, `exists` | A file Claude created matches the `path` glob, or none does with `exists: false`. Only files created during the run count |
| `llm` | `criteria`, `focus` | A judge model votes PASS on the rubric in at least two of three votes. In the `.md` layout the file body is the criteria |
| `baseline` | `baseline_file`, `criteria` | A judge finds the run satisfies the criteria at least as well as the reference transcript at `baseline_file`, a `.jsonl` in the case directory |

"There are no custom-code graders." Cost: "`regex`, `tool_used`, `tool_order`, and `file_exists` are computed from the transcript and files and cost nothing, while `llm` and `baseline` call a judge model and add to the run's cost." Judge: "a small fast model by default. Pass `--judge-model sonnet` or a full model ID."

`target` (regex) / `focus` (llm) values: `last_message` (default), `trace` ("A `regex` grader sees every message; an `llm` judge sees the first 12 and the last 12. Quotes and newlines inside it are JSON-escaped"), `files` ("The list of paths Claude created during the run, one per line. Not their contents"), `{ source: file, path: <path> }` ("The contents of one file in the workspace after the run… A PNG, JPEG, GIF, or WebP file is shown to an `llm` judge as an image. An `llm` judge refuses other binary files such as `.pptx` or PDF"), `mock_calls`.

Canonical skill-fired grader from the doc:
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?your-skill-name"'
---
```
"This passes when Claude invoked that skill at least once during the run, including by its namespaced `plugin-name:skill-name` form."

**With-only semantics in scoring**: "In a two-arm run, some graders are reported with `scored: false`. A check like 'the skill was invoked' can never pass without the plugin, so counting it would push the without-arm toward zero and inflate `Δ`. To keep the two arms comparable, Claude Code excludes such graders from the score in both arms and reports them in the with-arm as pass/fail indicators only. That includes: * Every `tool_used` grader whose `tool` is `Skill` * Any grader you mark `arm: with-only`. If every grader in a case is one of these, they're scored normally instead, since there would be nothing left to score. Set `arm: both` on a grader to score it in both arms regardless, which is what you want for a 'must not invoke the skill' check with `min: 0` and `max: 0`. Under `--ablation none` nothing is excluded, so the same suite can produce a different absolute score in the two modes." In the report such graders "carry a `plugin-fired indicator` badge."

### 1e. Scoring
> "each case runs three times by default. A run's score is the fraction of its graders that passed, weighted if you set weights, and the case's score is the mean across its runs. A case passes when its score meets the `--threshold`, `1.0` by default. In model calls, a suite makes roughly cases × runs agent runs with the plugin and as many again for the no-plugin baseline, plus three short judge calls per `llm` or `baseline` grader per run."

- `runs`: default 3, "1 to 50"; `--runs <n>` = "Each case's `runs`, else 3".
- `--threshold <0..1>`: default `1.0`; "A case passes when its with-arm score is at least this. Any case below it makes the command exit 1".
- `--ablation <mode>`: default "`with-without` when a plugin resolves, else `none`"; "`none` runs one arm; `with-without` adds the no-plugin baseline".
- Δ: "The summary and report show both scores and `Δ`, the with-arm score minus the without-arm score." One-arm mode: "the table shows `SCORE` and `PASS%` columns instead of `WITH`, `W/OUT`, and `Δ`".
- **"Arms aren't comparable"**: the JSON table says `cases[].aggregates.delta` is "With-arm score minus without-arm score. Omitted when the arms aren't comparable". The page does NOT define that phrase explicitly. The two related passages: (i) the with-only exclusion above ("To keep the two arms comparable, Claude Code excludes such graders…"), and (ii) `cases[].arms.with[].skippedPaidGraders`: "`true` when the cost ceiling skipped this run's judge graders, so its score isn't comparable".

### 1f. Results
> "Every run with at least one case writes a `results/<timestamp>/` directory inside the eval directory, containing `aggregate-result.json` and `report.html`. For a path target that's under the plugin; for a plugin you named, it's under your current directory."

Tree (from the suite reference): `results/<timestamp>/ ├── aggregate-result.json ├── report.html └── mock-recordings/`. "add results/ to .gitignore".

`aggregate-result.json` / `--json`: "a versioned document with `schemaVersion: 1`… Field names are camelCase and new fields are added without renaming existing ones". Documented fields: `partial`, `partialReason` (`cost_ceiling`, `interrupted`, `auth_failed`); `aggregates.overallScore`; `aggregates.casesPassed`, `aggregates.casesTotal`; `aggregates.meanDelta`; `cases[].name`; `cases[].aggregates.score`; `cases[].aggregates.delta`; `cases[].arms.with[].error`; `cases[].arms.with[].aborted` (`server`, `tool`, `reason`); `cases[].arms.with[].skippedPaidGraders`; `costUsd`, `durationSeconds`, `claudeVersion`. "The document also carries the suite configuration, every grader definition, and per-run grader results with explanations and evidence".

`report.html`: "a single self-contained file that makes no external requests". Tiles: "Suite score is the mean of the per-case with-plugin scores, Ablation Δ is how far that sits above or below the baseline score, and Cases counts how many met the threshold. Perfect runs is the share of with-plugin runs where every grader passed."

Options: `--json [path]` — "Print the result document to stdout, or write it to a path ending in `.json`. The run is quiet"; `--output-dir <dir>` — default `<eval dir>/results/<timestamp>/`, "Where `aggregate-result.json` and `report.html` go"; `--no-publish`; `--publish-report`.

Publishing: "If you're signed in with a claude.ai subscription and artifacts are available for your account, Claude Code also publishes the report as a private artifact and prints `Published: <url>`. Pass `--no-publish` to keep it local. If no `Published:` line appears, such as with API-key authentication, the local file is the report." "A run that a Claude Code session started… also stays local, and its `Report:` line says `kept local`."

### 1g. init, mocks, options
- **`claude plugin eval init`**: "An interactive Claude Code session then opens. Claude reads your plugin and asks you what a good result looks like, proposes prompts that should and shouldn't trigger the plugin, designs graders for each, pilots them once to check they behave, and writes one case directory per prompt under `evals/`, each named after its prompt."
- **`--bare`**: "`claude plugin eval init --bare first-case`" — "writes a case named `first-case` with a placeholder `prompt.md` and one placeholder grader, and runs nothing". "`claude plugin eval init` needs a terminal to ask you its questions; in CI, run `claude plugin eval init --bare <name>`".
- **Mocks**: "Put one Markdown file per tool under `evals/mocks/<server>/<tool>.md` for the whole suite, or under a case's own `mocks/` directory". Keys: `type` (default `fixed`; "`agent` treats the body as instructions for a small model that plays the server for the run and sees earlier calls as history"), `expect`, `error`, `abort_when`; plus `_server.md`, `_tools.json`, `fixtures/`, `.replay/<server>/`. `--mocks <mode>` default `record` ("`off` ignores mocks and starts the plugin's real MCP servers"); `--allow-real-servers`. "A `type: agent` mock answers with a call to the `--judge-model`".
- **`--allow-tools <tools...>`**: default None. "Runs never stop to ask for permission. Built-in tools that need a grant you didn't give, such as `Bash`, `Write`, `Edit`, `WebFetch`, and `WebSearch`, are removed from the session". Read-only set: "`Read`, `Glob`, `Grep`, `NotebookRead`, `Skill`, `Agent`, `TodoWrite`, and the task tools `TaskCreate`, `TaskGet`, `TaskList`, `TaskUpdate`, and `TaskStop`". Bash runs under the OS sandbox; "on Linux, install `bubblewrap` and `socat` first."
- **`--max-cost-usd <usd>`**: "A ceiling on the run's list-price cost estimate, not on plan usage. Checked before each run starts… If any run is left unstarted, the command exits 2 with partial results".
- **`--scaffold`**: default Off, "Run each case's `scaffold_script`"; "The script runs as you, outside the agent's sandbox".
- **`--model <model>`**: "Each case's `model`, else `ANTHROPIC_MODEL` if set, else Claude Code's default… Pin it in CI".
- **`--judge-model <model>`**: "A small fast model" — "Model for `llm` and `baseline` graders".
- Others: `-j/--concurrency` (1–8), `--trust-plugin`, `--keep-temp`, `--eval-dir`; `plugin.json` `"experimental": { "evals": "quality/evals" }`.

### 1h. CI and troubleshooting
CI example: `claude plugin eval . --trust-plugin --json results.json --threshold 0.8 --model claude-sonnet-5 --judge-model claude-haiku-4-5 --no-publish --max-cost-usd 20`.

Exit codes: 0 "Every case scored at or above `--threshold` and every case file loaded"; 1 "A case scored below the threshold, a case file failed to load, no cases were found, a run couldn't be started, the plugin directory isn't trusted and `--trust-plugin` wasn't passed, or an option was invalid"; 2 "Partial run: the `--max-cost-usd` ceiling was hit, or your credential was rejected… `results.json` is still written with `partial: true`"; 130 "Interrupted. Partial results are written"; 143 "Terminated, such as by a CI timeout". "Problems writing or publishing the HTML report never change the exit code."

Troubleshooting (heading → fix):
- **"plugin eval is currently in early access"** → "Your build predates general availability of the command. Run `claude update`, then run the command again in a fresh session."
- **"plugin eval is currently unavailable"** → "Anthropic has switched the command off server-side. Nothing on your machine turns it back on; run `claude update` and try again in a fresh session later."
- **"is not a trusted plugin directory, and this run cannot stop to ask you about it"** → "Run `claude plugin eval <dir>` once in a terminal and answer the prompt, or pass `--trust-plugin`".
- **"No eval cases found"** → "No `<case>/prompt.md` or `<case>/case.yaml` exists beneath the eval directory in effect, or your `--case` and `--tag` filters matched no case. Run from the plugin root, or run `claude plugin eval init`".
- **The baseline arm shows no plugin, or delta is zero** → "Add `plugins: ["../.."]` to the case… If the plugin did load and `Δ` is still near zero with your `tool_used: Skill` grader failing, that's usually a real finding, meaning the skill's `description` doesn't trigger on the prompt's phrasing. Adjust the description and re-run the same suite."
- **Everything scores zero although the right files were produced** → "Use `{ source: file, path: <path> }` as the `target` or `focus`. Separately, `file_exists` counts only files created during the run".
- **A regex over the trace doesn't match text I can see** → "The default `target` is `last_message`, not the trace… quotes appear as `\"`. Regexes use JavaScript syntax, so put `i` in `flags`".
- **Tools are denied, MCP tools are missing, or Bash won't run** → "Anything beyond the read-only set needs your grant… a mocked tool needs neither."
- **The run exits 1 but the results look fine** → "The default `--threshold` is 1.0… Set a threshold that matches your bar."
- **"--json output path must end in .json"** → "You put the target after `--json`… Put the target first".
- **A grader shows passed: false under a run that scored 1.0** → "That grader is excluded from the score by design in a two-arm run, and its `scored` field is `false`."
- **Runs fail with a usage-limit or rate-limit error partway through** → "The suite still finishes and isn't marked `partial`… Check the `NOTES` column or `cases[].arms.with[].error`… re-run after the limit resets, with `--runs 1` or a `--case` filter".
- **Runs time out or hit the turn cap** → "The defaults are 10 turns and 300 seconds. Raise `max_turns` and `timeout_seconds`… use `--max-cost-usd` as the cost ceiling rather than tight per-run limits."

### 1i. Triggering vs output quality
- "The most common first finding is a `Δ` near zero with the case's `tool_used: Skill` grader failing, which means Claude isn't choosing your skill on natural phrasing. Adjust the skill's `description`, run `claude plugin eval .` again, and compare."
- "Give each case one grader on the result, such as the final message or a produced file, and one on how Claude got there, such as `tool_used` or `tool_order`. Together they tell you both whether the answer was right and whether your plugin produced it."
- Prompts must be "phrased the way a user would type it rather than naming the skill."
- See also: "[Skills]: how a skill's description decides when Claude invokes it, which is what a case that checks whether the skill triggers is measuring".
- Negative case: `arm: both` + `tool_used` with `min: 0`/`max: 0` for "must not invoke the skill".

---

## 2. Plugins reference — https://code.claude.com/docs/en/plugins-reference.md

### Skills-directory plugins (verbatim)
> "Any folder under a skills directory that contains a `.claude-plugin/plugin.json` manifest is loaded as a plugin named `<name>@skills-dir` on the next session, with no marketplace and no install step. Scaffold one with `plugin init`. Unlike a copied marketplace install, the plugin is discovered in place rather than copied into the plugin cache."

| What you have | What it is |
|---|---|
| `<skills-dir>/foo/SKILL.md` with no manifest | A plain skill named `foo` |
| `<skills-dir>/foo/.claude-plugin/plugin.json` | A plugin `foo@skills-dir`, which can bundle its own skills, agents, hooks, and more |
| `<plugin>/skills/bar/SKILL.md` | A skill `bar` packaged inside a plugin |

| Skills directory | Scope | Loads |
|---|---|---|
| `~/.claude/skills/` | personal | In every project, since the location is yours alone |
| `<cwd>/.claude/skills/` | project | Only after you accept the workspace trust dialog for that folder |

**Does `~/.claude/skills/` itself qualify?** Not as a plugin. It is the *skills directory*; the plugin is a *subfolder* of it carrying `.claude-plugin/plugin.json`. Nothing in the section describes the whole directory becoming a plugin.

Registration: "with no marketplace and no install step"; "There is no `uninstall` step because nothing was installed from a marketplace." Disable: `claude plugin disable my-tool@skills-dir`. Reload: "Changes you make to a skill's `SKILL.md` take effect immediately in the current session. Changes to the plugin's other components, such as `hooks/`, `.mcp.json`, `agents/`, and `output-styles/`, do not. Run `/reload-plugins` or restart". `claude plugin install`, `--plugin-dir`, and settings are NOT mentioned in this section (the eval page only says "Pointing it at a plugin is the same trust decision as `claude --plugin-dir`"). Warning: "Project-scope `@skills-dir` plugins load only from the `.claude/skills/` of the session's primary working directory. They don't walk up to the repository root".

### Manifest
"The manifest is optional. If omitted, Claude Code auto-discovers components in default locations and derives the plugin name from the directory name." "If you include a manifest, `name` is the only required field." (`name`: "Unique identifier in kebab-case, with no spaces, control characters, or bidirectional-formatting characters"). Metadata fields: `$schema`, `displayName`, `version`, `description`, `author`, `homepage`, `repository`, `license`, `keywords`, `metadata`, `defaultEnabled`. Component paths: `skills`, `commands`, `agents`, `workflows`, `hooks`, `mcpServers`, `outputStyles`, `lspServers`, `experimental.themes`, `experimental.monitors`, `experimental.evals`, `userConfig`, `channels`, `dependencies`. "Claude Code ignores top-level fields it does not recognize… `claude plugin validate` reports unrecognized fields as warnings"; `--strict` "to treat warnings as errors". Minimal manifest therefore: `{"name": "plugin-name"}`.

### Directory layout (verbatim, trimmed to requested dirs)
```
enterprise-plugin/
├── .claude-plugin/           # Metadata directory (optional)
│   └── plugin.json             # plugin manifest
├── skills/                   # Skills
│   ├── code-reviewer/
│   │   └── SKILL.md
│   └── pdf-processor/
│       ├── SKILL.md
│       └── scripts/
├── commands/                 # Skills as flat .md files
│   ├── status.md
│   └── logs.md
├── agents/                   # Subagent definitions
│   ├── security-reviewer.md
│   └── review/               # Agents here load as enterprise-plugin:review:<name>
│       └── accessibility.md
├── hooks/                    # Hook configurations
│   ├── hooks.json           # Main hook config
│   └── security-hooks.json  # Additional hooks
```
(also `workflows/`, `output-styles/`, `themes/`, `monitors/`, `bin/`, `settings.json`, `.mcp.json`, `.lsp.json`, `scripts/`, `LICENSE`, `CHANGELOG.md`). Warning: "All other directories (commands/, agents/, skills/, …) must be at the plugin root, not inside `.claude-plugin/`." "A `CLAUDE.md` file at the plugin root is not loaded as project context." File-locations table: Commands = "Skills as flat Markdown files. Use `skills/` for new plugins". No dedicated "plugin validate" section exists on the page (referenced inline only).

---

## 3. Skills — https://code.claude.com/docs/en/skills.md

### 3a. Frontmatter reference (verbatim, condensed column widths)

| Field | Required | Description |
|---|---|---|
| `name` | No | Display name shown in skill listings. Defaults to the directory name. See How a skill gets its command name |
| `description` | Recommended | What the skill does and when to use it. Claude uses this to decide when to apply the skill. If omitted, uses the first non-empty line of the markdown content. Put the key use case first: the combined `description` and `when_to_use` text is truncated at 1,536 characters in the skill listing to reduce context usage. |
| `when_to_use` | No | Additional context for when Claude should invoke the skill, such as trigger phrases or example requests. Appended to `description` in the skill listing and counts toward the 1,536-character cap. |
| `argument-hint` | No | Hint shown during autocomplete to indicate expected arguments. Example: `[issue-number]` or `[filename] [format]`. |
| `arguments` | No | Named positional arguments for `$name` substitution in the skill content. Accepts a space-separated string or a YAML list. Names map to argument positions in order. |
| `disable-model-invocation` | No | Set to `true` to prevent Claude from automatically loading this skill. Use for workflows you want to trigger manually with `/name`. Also prevents the skill from being preloaded into subagents. As of v2.1.196, also prevents the skill from running when a scheduled task fires with the skill as its prompt. Default: `false`. |
| `user-invocable` | No | Set to `false` when only Claude should invoke the skill: Claude Code hides it from the `/` menu and doesn't run it when you type `/name`. Use for background knowledge users shouldn't invoke directly. Default: `true`. |
| `allowed-tools` | No | Tools Claude can use without asking permission during the turn that invokes this skill. The grant clears when you send your next message. Accepts a space- or comma-separated string, or a YAML list. |
| `disallowed-tools` | No | Tools removed from Claude's available pool while this skill is active… Accepts a space- or comma-separated string, or a YAML list. The restriction clears when you send your next message. Like deny rules, the field can't remove `EndConversation` while any other tool remains. |
| `model` | No | Model to use when this skill is active. The override applies for the rest of the current turn and isn't saved to settings… Accepts the same values as `/model`, or `inherit`… With `context: fork`, the value sets the forked subagent's model instead… |
| `effort` | No | Effort level when this skill is active. Overrides the session effort level. Default: inherits from session. Options: `low`, `medium`, `high`, `xhigh`, `max`; available levels depend on the model. |
| `context` | No | Set to `fork` to run in a forked subagent context. |
| `agent` | No | Which subagent type to use when `context: fork` is set. |
| `background` | No | Only applies with `context: fork`. Set to `false` to wait for the forked subagent's result in the turn that invoked the skill, instead of running it in the background. Default: `true`. Requires Claude Code v2.1.218 or later. |
| `hooks` | No | Hooks that Claude Code registers when the skill is invoked and keeps running for the rest of the session. |
| `paths` | No | Glob patterns that limit when this skill is activated. Accepts a comma-separated string or a YAML list. When set, Claude loads the skill automatically only when working with files matching the patterns. |
| `shell` | No | Shell to use for `` !`command` `` and ```` ```! ```` blocks in this skill. Accepts `bash` (default) or `powershell`. |
| `metadata` | No | Free-form YAML map for your own key-value data… Claude Code doesn't act on its contents, and drops a value that isn't a map. Don't reuse frontmatter field names such as `paths` as keys. |
| `license` | No | License covering the skill. Part of the Agent Skills spec… Claude Code accepts the field but doesn't act on it. |
| `compatibility` | No | Environment requirements for the skill… as defined by the Agent Skills spec… Accepts a string of up to 500 characters. Claude Code accepts the field but doesn't act on it. |

Notes after the table: "Claude Code reads the frontmatter only when the opening `---` is the file's first line. Otherwise it treats the whole file, `---` markers included, as skill content." "Boolean fields accept `yes`, `no`, `on`, `off`, `1`, and `0` in any letter case, in addition to `true` and `false`. Before v2.1.218, Claude Code recognized only `true` and `false`."

### 3b. "Evaluate and iterate on a skill" (verbatim)
> "Seeing a skill trigger tells you Claude found it, not that it did what you intended. To know a skill is working, measure separately whether Claude invokes it on the prompts it should, and whether the output matches what you expect when it does.
> The check for both is a baseline comparison. Collect a few realistic prompts, run each one in a fresh session with the skill available and again with it disabled, and compare the results. A fresh session matters because leftover context from authoring the skill will mask gaps in the written instructions.
> Two tools automate that comparison. For a skill that ships in a plugin, `claude plugin eval` runs each prompt in an isolated session with and without the plugin, scores it with graders you define or that it writes for you, and exits non-zero below a threshold so you can gate CI on it. For iterating on a single skill inside a Claude Code conversation, the skill-creator plugin below runs a similar loop with its own `evals/evals.json` format. The two formats aren't interchangeable."

"Run evals with skill-creator": "The `skill-creator` plugin [linked to `anthropics/claude-plugins-official/tree/main/plugins/skill-creator`] automates the comparison loop inside Claude Code. Install it from the official marketplace: `/plugin install skill-creator@claude-plugins-official`… The plugin adds an `/evals` skill that runs tests you define inside `.claude/skills/evals/`. Copy the plugin's template to get started: `/evals --init`… The template sets up an `evals.json` test file that scores whether Claude invokes your skill on realistic prompts and whether the skill's output matches expected results… With the template's default setup, Claude scores whether: 1. Your skill was invoked on prompts where it should have been 2. The skill's output met expectations for those prompts".

"Run evals with plugin evals": "`claude plugin eval <plugin-path> --test-config <path-to-test-config.json>`… Plugin evals run in isolated sessions where Claude Code downloads the plugin fresh… The test config format differs from the skill-creator plugin's `evals.json`."

**Inconsistency to flag**: this `--test-config` flag and JSON test config do not appear anywhere on the plugin-evals page (which documents `evals/<case>/prompt.md` + `graders/*.md` and lists `--help` options without `--test-config`). Likewise `/evals --init` and `.claude/skills/evals/` are absent from the `anthropics/skills` SKILL.md (item 5). The skills page appears to lag the eval page.

### 3c. `/skill-doctor` (verbatim, section titled "Find unused skills")
> "Every skill in the skill listing adds to your context on every turn, whether or not Claude ever uses it. Run `/skill-doctor` to see what each of your skills costs and how often it gets used, so you can decide which ones to turn off. In an interactive session, the report opens in the `/plugin` manager's **Stats** tab. In non-interactive mode with `-p`, Claude Code prints it as text.
> The report covers the skills in your session other than bundled skills and enterprise skills. It flags skills in the listing that have never been invoked and says where to turn them off. Of the skills it tells you where to turn off, start with the ones that have the highest context cost. The report also lists plugins you haven't used recently.
> `/skill-doctor` requires Claude Code v2.1.252 or later and isn't available in sessions that skip feature-flag fetching. If you run `/skill-doctor` over Remote Control… Claude Code replies `Skill usage reports are not available on this connection.`"

### 3d. Commands → skills merge
- Note box: "**Custom commands have been merged into skills.** A file at `.claude/commands/deploy.md` and a skill at `.claude/skills/deploy/SKILL.md` both create `/deploy` and work the same way. Your existing `.claude/commands/` files keep working. Skills add optional features: a directory for supporting files, frontmatter to control whether you or Claude invokes them, and the ability for Claude to load them automatically when relevant."
- "**Command files**: a Markdown file in `.claude/commands/` is the older format and still works. It supports the same frontmatter except `name` and `paths`… Prefer a skill for new work, since skills also support supporting files."
- "**Skill folder as a plugin**: add a `.claude-plugin/plugin.json` to a skill folder and it loads as a plugin named `<name>@skills-dir`, so it can bundle agents, hooks, and MCP servers."
- Arguments: `$ARGUMENTS`, `$ARGUMENTS[N]`, `$N` ("`$0` for the first argument or `$1` for the second"), `$name` via `arguments` frontmatter. "If you invoke a skill with arguments but no placeholder in the skill's content receives one, Claude Code appends `ARGUMENTS: <your input>` to the end of the skill content." "Indexed arguments use shell-style quoting". Escape with `\$1.00`.
- Dynamic context: "The `` !`<command>` `` syntax runs shell commands before the skill content is sent to Claude… The inline form is only recognized when `!` appears at the start of a line or immediately after whitespace… For multi-line commands, use a fenced code block opened with ```` ```! ````." "A failed command aborts the entire skill invocation… `Shell command failed for pattern "..."`." "Injected commands never prompt for permission… A command a deny rule matches aborts the invocation". Disable via `"disableSkillShellExecution": true`. Never run for skills synced from claude.ai (v2.1.228+).
- Namespacing ("How a skill gets its command name"): `.claude/commands/deploy.md` → `/deploy`; `.claude/commands/frontend/component.md` → `/frontend:component`; `.claude/skills/deploy-staging/SKILL.md` → `/deploy-staging`; nested clash `apps/web/.claude/skills/deploy/SKILL.md` → `/apps/web:deploy`; plugin `my-plugin/skills/review/SKILL.md` → `/my-plugin:review`, "or `/my-plugin:fancy` with `name: fancy`"; "The bare `/fancy` also invokes the skill unless another command already uses that name." "In a personal or project skill, `name` sets only the display label shown in skill listings, and the command still comes from the directory name."
- Control table: default → You Yes / Claude Yes / "Description always in context, full skill loads when invoked"; `disable-model-invocation: true` → Yes / No / "Description not in context, full skill loads when you invoke"; `user-invocable: false` → No / Yes / "Description always in context". `skillOverrides` setting states: `"on"`, `"name-only"`, `"user-invocable-only"`, `"off"`; "Plugin skills are not affected by `skillOverrides`."

### 3e. Claude-Code-specific vs Agent Skills spec (verbatim)
> "Claude Code accepts every field in the table above. Outside Claude Code, you can use only the fields in the Agent Skills spec:"

| Distribution path | Frontmatter fields you can use |
|---|---|
| Claude Code skills at any level, including plugin skills | Every field in the table above |
| claude.ai skill uploads, the Skills API, and packaging with `package_skill.py` from anthropics/skills | `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools` |

> "If you include any field the spec doesn't allow, packaging or upload fails with a hard error instead of ignoring the field: `Unexpected key(s) in SKILL.md frontmatter: argument-hint. Allowed properties are: allowed-tools, compatibility, description, license, metadata, name`… Claude Code-only body features, such as dynamic context injection, don't function in claude.ai chat or through the API."

### 3f. Skill content lifecycle (verbatim)
> "When you or Claude invoke a skill, the rendered `SKILL.md` content enters the conversation as a single message and stays there across later turns. This persistence applies to the skill's instructions, not its permissions: an `allowed-tools` grant clears when you send your next message. Claude Code does not re-read the skill file on later turns…
> When Claude re-invokes a skill whose rendered content is identical to the copy already in context, Claude Code adds a short note that the skill is already loaded rather than a second copy…
> Auto-compaction carries invoked skills forward within a token budget… Claude Code re-attaches the most recent invocation of each skill after the summary, keeping the first 5,000 tokens of each. Re-attached skills share a combined budget of 25,000 tokens…
> If a skill seems to stop influencing behavior after the first response, the content is usually still present and the model is choosing other tools or approaches. Strengthen the skill's `description` and instructions so the model keeps preferring it, or use hooks to enforce behavior deterministically. If the skill is large or you invoked several others after it, re-invoke it after compaction to restore the full content."

---

## 4. Agent Skills spec — https://agentskills.io/specification

| Field | Required | Constraints |
|---|---|---|
| `name` | Yes | Max 64 characters. Lowercase letters, numbers, and hyphens only. Must not start or end with a hyphen. |
| `description` | Yes | Max 1024 characters. Non-empty. Describes what the skill does and when to use it. |
| `license` | No | License name or reference to a bundled license file. |
| `compatibility` | No | Max 500 characters. Indicates environment requirements (intended product, system packages, network access, etc.). |
| `metadata` | No | Arbitrary key-value mapping for additional metadata (a map from string keys to string values). |
| `allowed-tools` | No | Space-separated string of pre-approved tools the skill may use. (Experimental) |

`name` details: "Must be 1-64 characters… Must not contain consecutive hyphens (`--`)… Must match the parent directory name". `description`: "Should include specific keywords that help agents identify relevant tasks". `allowed-tools`: "A space-separated string… Experimental. Support for this field may vary" (example `allowed-tools: Bash(git:*) Bash(jq:*) Read`). Note the spec says `allowed-tools` is space-separated only; Claude Code additionally accepts comma-separated or YAML list.

Validation: "Use the skills-ref reference library to validate your skills: `skills-ref validate ./my-skill` This checks that your `SKILL.md` frontmatter is valid and follows all naming conventions." Progressive disclosure: "Metadata (~100 tokens)… Instructions (< 5000 tokens recommended)… Keep your main `SKILL.md` under 500 lines."

---

## 5. skill-creator (anthropics/skills) — https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md

Directory listing (https://github.com/anthropics/skills/tree/main/skills/skill-creator): `agents/`, `assets/`, `eval-viewer/`, `references/`, `scripts/`, `LICENSE.txt`, `SKILL.md`. **No README.md exists** at that path. `scripts/` contains: `__init__.py`, `aggregate_benchmark.py`, `generate_report.py`, `improve_description.py`, `package_skill.py`, `quick_validate.py`, `run_eval.py`, `run_loop.py`, `utils.py`. Also referenced: `eval-viewer/generate_review.py`, `agents/grader.md`, `agents/comparator.md`, `agents/analyzer.md`, `references/schemas.md`, `assets/eval_review.html`.

Frontmatter description: "Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy."

**Files it creates**:
- `evals/evals.json` in the skill dir: "Save test cases to `evals/evals.json`. Don't write assertions yet — just the prompts." Example: `{"skill_name": "example-skill", "evals": [{"id": 1, "prompt": "User's task prompt", "expected_output": "Description of expected result", "files": []}]}`. "See `references/schemas.md` for the full schema (including the `assertions` field, which you'll add later)."
- Workspace: "Put results in `<skill-name>-workspace/` as a sibling to the skill directory. Within the workspace, organize results by iteration (`iteration-1/`, `iteration-2/`, etc.) and within that, each test case gets a directory (`eval-0/`, `eval-1/`, etc.)". Per test case: `eval_metadata.json` (`eval_id`, `eval_name`, `prompt`, `assertions`), `with_skill/outputs/`, `without_skill/outputs/` (or `old_skill/outputs/` when improving), `timing.json` (`total_tokens`, `duration_ms`, `total_duration_seconds`), `grading.json`, `benchmark.json` + `benchmark.md`, `feedback.json`, `skill-snapshot/`.

**How it runs evals** — subagents, not `claude -p`: "For each test case, spawn two subagents in the same turn — one with the skill, one without… Launch everything at once". Subagent prompt: "Execute this task: - Skill path: <path-to-skill> - Task: <eval prompt> - Input files: … - Save outputs to: <workspace>/iteration-<N>/eval-<ID>/with_skill/outputs/ - Outputs to save: …". Baseline: "**Creating a new skill**: no skill at all… **Improving an existing skill**: the old version. Before editing, snapshot the skill (`cp -r <skill-path> <workspace>/skill-snapshot/`)". Claude.ai: "No subagents means no parallel execution… Skip the baseline runs". `claude -p` is used only by description optimization: "This section requires the `claude` CLI tool (specifically `claude -p`) which is only available in Claude Code."

**How it grades**: "spawn a grader subagent (or grade inline) that reads `agents/grader.md` and evaluates each assertion against the outputs. Save results to `grading.json` in each run directory. The grading.json expectations array must use the fields `text`, `passed`, and `evidence`… For assertions that can be checked programmatically, write and run a script rather than eyeballing it". Aggregate: `python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>` → "`benchmark.json` and `benchmark.md` with pass_rate, time, and tokens for each configuration, with mean ± stddev and the delta." Viewer: `eval-viewer/generate_review.py … --benchmark … [--previous-workspace …] [--static <output_path>]`; "Submit All Reviews" writes `feedback.json` (`{"reviews": [{"run_id": "eval-0-with_skill", "feedback": "...", "timestamp": "..."}], "status": "complete"}`). `agents/grader.md` verdict rule: "**PASS**: Clear evidence the expectation is true AND the evidence reflects genuine task completion… **When uncertain**: The burden of proof to pass is on the expectation… **No partial credit**". Blind comparison via `agents/comparator.md` ("optional, requires subagents").

**Trigger testing — yes ("Description Optimization")**: "The description field in SKILL.md frontmatter is the primary mechanism that determines whether Claude invokes a skill. After creating or improving a skill, offer to optimize the description for better triggering accuracy." Step 1: "Create 20 eval queries — a mix of should-trigger and should-not-trigger. Save as JSON: `[{"query": "the user prompt", "should_trigger": true}, {"query": "another prompt", "should_trigger": false}]`… should-trigger queries (8-10)… should-not-trigger queries (8-10), the most valuable ones are the near-misses". Step 2: review in `assets/eval_review.html`. Step 3: `python -m scripts.run_loop --eval-set <path-to-trigger-eval.json> --skill-path <path-to-skill> --model <model-id-powering-this-session> --max-iterations 5 --verbose` — "It splits the eval set into 60% train and 40% held-out test, evaluates the current description (running each query 3 times to get a reliable trigger rate), then calls Claude to propose improvements based on what failed… returns JSON with `best_description` — selected by test score rather than train score". Mechanism note: "Claude only consults skills for tasks it can't easily handle on its own — simple, one-step queries like 'read this PDF' may not trigger a skill even if the description matches perfectly". Description advice: "make the skill descriptions a little bit 'pushy'".

**Schema inconsistency to flag** (`references/schemas.md`): `evals.json` there uses `"expectations": ["The output includes X", …]` with field doc "`evals[].expectations`: List of verifiable statements", while SKILL.md calls it "the `assertions` field", `eval_metadata.json` uses `"assertions": []`, and agentskills.io uses `"assertions"`. `grading.json` in schemas.md/grader.md uses top-level `expectations[]` (+ `summary`, `execution_metrics`, `timing`, `claims`, `user_notes_summary`, `eval_feedback`), while agentskills.io shows `assertion_results[]`. `benchmark.json`: `metadata.runs_per_configuration`, `runs[].configuration` ("Must be `"with_skill"` or `"without_skill"`"), `runs[].result.{pass_rate,passed,failed,total,time_seconds,tokens,tool_calls,errors}`, `run_summary.{with_skill,without_skill}.{pass_rate,time_seconds,tokens}.{mean,stddev,min,max}`, `delta` as strings (`"+0.50"`).

---

## 6. agentskills.io evaluating-skills — https://agentskills.io/skill-creation/evaluating-skills.md

Title: "Evaluating skill output quality". `evals/evals.json` fields: `skill_name`, `evals[].id`, `evals[].prompt`, `evals[].expected_output`, `evals[].files`, and later `evals[].assertions` (array of strings): "Add assertions to each test case in `evals/evals.json`". Workspace verbatim:
```
csv-analyzer-workspace/
└── iteration-1/
    ├── eval-top-months-chart/
    │   ├── with_skill/
    │   │   ├── outputs/       # Files produced by the run
    │   │   ├── timing.json    # Tokens and duration
    │   │   └── grading.json   # Assertion results
    │   └── without_skill/
    │       ├── outputs/
    │       ├── timing.json
    │       └── grading.json
    └── benchmark.json         # Aggregated statistics
```
"The core pattern is to run each test case twice: once **with the skill** and once **without it** (or with a previous version)." Runs: "In environments that support subagents (Claude Code, for example), this isolation comes naturally… Without subagents, use a separate session for each run." Grading: "The simplest approach is to give the outputs and assertions to an LLM… For assertions that can be checked by code… use a verification script". Repeats: "Standard deviation (`stddev`) is only meaningful with multiple runs per eval… focus on the raw pass counts and the delta". Human review → `feedback.json` (`{"eval-top-months-chart": "…", "eval-clean-missing-emails": ""}`). **Trigger testing: NOT covered** — the page is entirely about output quality; the words "trigger", "invoke", "description" do not appear in an eval context. It ends: "The `skill-creator` Skill automates much of this workflow".

---

## Comparison table

| Capability | `claude plugin eval` | skill-creator / agentskills evals |
|---|---|---|
| Trigger test (description quality) | Yes — `tool_used` grader with `tool: Skill` + `input_match`; init "proposes prompts that should and shouldn't trigger"; negative case via `arm: both`, `min: 0`, `max: 0`; troubleshooting "delta is zero" ([plugin-evals] Write a case manually; Score against baseline) | skill-creator: Yes — "Description Optimization", `scripts/run_loop.py`, 20 `should_trigger` queries, 3 runs/query, 60/40 split, uses `claude -p` ([SKILL.md]). agentskills evaluating-skills: No |
| Output assertions (deterministic) | Yes — `regex` (`target`, `match`, `flags`), `file_exists`, `tool_used`, `tool_order`; "no custom-code graders" ([plugin-evals] Grader types) | Partial — natural-language `assertions`/`expectations` strings; "For assertions that can be checked programmatically, write and run a script" ([SKILL.md] Step 4; [agentskills] Grading outputs) |
| LLM judge | Yes — `llm` (2-of-3 votes, `focus`, image input), `baseline` (vs reference `.jsonl`), `--judge-model` ([plugin-evals] Grader types) | Yes — grader subagent per `agents/grader.md` (PASS/FAIL + evidence, burden of proof on the expectation); blind `agents/comparator.md` ([SKILL.md]) |
| Baseline / ablation | Yes — `--ablation with-without` default, `WITH`/`W/OUT`/`Δ`, `aggregates.meanDelta`, with-only exclusion ([plugin-evals] Score against baseline) | Yes — `without_skill/` or `old_skill/` runs, `benchmark.json` `run_summary.delta` ([SKILL.md] Step 1; [agentskills] Workspace structure) |
| Repeated runs | Yes — `runs` default 3, range 1–50, `--runs` ([plugin-evals] prompt.md frontmatter) | Partial — one subagent per arm per test case in the loop; `benchmark.json` has `runs_per_configuration` and stddev; no documented default >1 for output evals (trigger loop: 3 runs/query) ([schemas.md]; [agentskills] Note on stddev) |
| Cost control | Yes — `--max-cost-usd` (exit 2, `partial: true`), `COST` column, `costUsd` ([plugin-evals] Command options) | No ceiling — records `total_tokens`/`duration_ms` in `timing.json` only ([SKILL.md] Step 3) |
| Results report | Yes — `report.html` (self-contained), `aggregate-result.json` (`schemaVersion: 1`), optional publish as private artifact ([plugin-evals] Read the results) | Yes — `eval-viewer/generate_review.py` (server or `--static` HTML), `benchmark.md` ([SKILL.md] Step 4) |
| CI exit code | Yes — 0/1/2/130/143, `--threshold`, `--trust-plugin`, `--json results.json` ([plugin-evals] Run evals in CI) | Not documented |
| Mocks | Yes — MCP mocks `evals/mocks/<server>/<tool>.md`, `type: fixed|agent`, `expect`, `.replay/`, `--mocks record|off` ([plugin-evals] Mock MCP servers) | Not documented |
| Scaffold / setup script | Yes — `context.scaffold_script` + `--scaffold`; `context.add_dirs` ([plugin-evals] case.yaml fields) | Partial — `evals[].files` input file list only; no setup script ([schemas.md]; [agentskills] Designing test cases) |
| History / conversation context | Yes — `context.history_file` (`.jsonl`, "the case's prompt becomes the next user turn") ([plugin-evals] case.yaml fields) | Not documented — runs "start with a clean context" ([agentskills] Spawning runs) |
| Target unit | Requires a plugin (`plugin.json` or `<skills-dir>/<name>/.claude-plugin/plugin.json` → `name@skills-dir`) ([plugin-evals] Requirements; [plugins-reference] Skills-directory plugins) | Bare skill directory, no plugin needed ([SKILL.md]) |

**Doc discrepancies worth recording in the audit**: (1) skills.md documents `claude plugin eval … --test-config <json>` and `/evals --init`, neither of which exists on plugin-evals.md or in the anthropics/skills SKILL.md; (2) skills.md links skill-creator to `anthropics/claude-plugins-official`, not `anthropics/skills`; (3) `assertions` vs `expectations` naming differs between agentskills.io, SKILL.md and `references/schemas.md`.
