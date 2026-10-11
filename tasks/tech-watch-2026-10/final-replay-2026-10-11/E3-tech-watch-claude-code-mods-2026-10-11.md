# Tech Watch — Claude Code mods
**Date**: 2026-10-11 | **Window**: 30 days | **Request**: "Claude Mods" | **Owner**: Anthropic | **Sources**: 20 ranked + 3 primary

| Source | Status | Raw | On-topic | In report |
|---|---|---|---|---|
| arXiv | empty | 0 | 0 | 0 |
| GitHub | degraded: ⚠️ GitHub token rejected (401); results fetched without authentication (10 searches/min instead of 30). Rotate GITHUB_TOKEN on the service. Fallback `WebSearch` on github.com: 10 of the 30 raw results, 6 new, none ranked | 30 | 29 | 12 |
| YouTube | failed: YouTube API key not configured. Fallback `WebSearch` on youtube.com: 10 links, all 10 raw results, no date, duration, views or channel, none ranked | 10 | 10 | 0 |
| Web (Tier 2) | ok | 28 | 25 | 8 |
| Web (Tier 3) | not run (unique on-topic ≥ 12) | – | – | 0 |
| Owner domains | ok | 10 | – | 3 |

**Pipeline**: 68 raw → 64 on-topic, 0 adjacent, 1 homonyms, 3 dropped → 56 unique → 25 ≥ 60 → 20 ranked (cap 20).
**Enrichment**: 10/10 pages opened (2 primary), 0 failures, 1 truncated.
**Date test**: skipped (the docs overview mentions an early-access period without dating it; launch is 2026-10-01 per the Anthropic blog post).
**Notes** (at most 5 bullets; omit the line if none):
- Cap cut: 5 sources scored ≥ 60 but fell below rank 20: karanb192/awesome-claude-code-mods (64, 477 stars, the most-starred catalogue, created 2026-09-15 so freshness 5), JohnnyVizz/claude-kit (64), karanb192/claude-code-mods (62), darrell-tw/darrelltw-mods (62), galElmalah/claude-mods (62).
- Unopened, therefore `unverified` and excluded, not judged poor: 13 Tier 2 web pages past the 10-page budget (the Medium and Substack posts, 1 dev.to post, it-connect.fr, pasqualepillitteri.it, claudekit.io, braindetox.kr, onewave-ai.com, blog.laozhang.ai), 2 GitHub fallback links without metadata (ruvnet field-guide gist, hoobnn/awesome-claude-code-mods) and the 10 YouTube links. No YouTube video could be ranked; one title, "Mods in Claude Code: change how Claude Code works" (https://www.youtube.com/watch?v=yUuFvL1lK4k), reads like an official video but its channel is `unverified`. Essential band is empty.
- Scoring interpretations: an "Updated" or "Last modified" date is not a publication date, so [15], [19] and [20] have date `unverified` (freshness 5). dev.to shows "Oct N" without a year on [4], [5] and [17]; read as 2026 because the posts cover the 2026-10-01 launch and today is 2026-10-11. The third primary source (Create a mod) and the reference repositories were not opened: their dates are `unverified`.
- Truncated read: StationX guide [20] read to 100,000 of 103,463 characters (length taken from what was read). The Claude Code changelog was not opened (known to truncate before the launch entry), so the 2.1.287 entry and the early-access start date were not checked there.
- Contradictions: [4] is kept and flagged (announcement date). The unranked YouTube title "Claude Code 3.0 (New Mods Feature) … SILENTLY dropped" contradicts the primary sources (v2.1.287, public announcement) and would have been excluded. Summaries of ranked web pages rely on title and search description only (step 8 extracts date, length and author, no content).

---

## Executive Summary
Anthropic launched mods for Claude Code on 2026-10-01: plugins made of JavaScript or TypeScript event handlers that run inside Claude Code, can observe, rewrite or answer events (tool calls, prompts, interface rendering) and draw their own panes and bands. Within ten days the ecosystem response is overwhelmingly community repositories, most created on 2026-10-02, split between status-band utilities (context, usage limits, cost) and catalogues that scan what each mod can reach. The unexpected finding is how quickly security auditing became a theme of its own: mods are not sandboxed and run with the user's permissions, and several of the earliest community projects exist to answer "what can this mod read, write, run or send".

---

## Primary sources

**Customize Claude Code with mods in TypeScript** — 🔗 https://claude.com/blog/claude-code-mods — 📅 2026-10-01
Launch announcement (Anthropic, about 780 words): mods are "available today in the Claude Code CLI and desktop app", ship inside plugins, are not sandboxed, and on Team and Enterprise plans a built-in `sec-default` mod loads first; `/diff` is now a mod. No version number is given; links to the `mods` directory of anthropics/claude-code and to design issue #91870.

**Mods overview - Claude Code Docs** — 🔗 https://code.claude.com/docs/en/plugins/mods/overview — 📅 unverified
Reference definition and requirements: mods are on by default, need Claude Code v2.1.287 or later in the terminal and v2.1.286 in the Desktop app; the early-access variable `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS` is now ignored. Hooks run in every session that loads the plugin, drawing appears only in the terminal and the Desktop Code tab (not in the VS Code chat panel, `claude -p` or cloud sessions; no plugins in WSL Desktop sessions). Names the sample mods (`token-weather`, `blast-radius`, `replay-theater` in anthropics/claude-code-playground, unsupported), the built-in mods (`diff`, `agents-md`, `sec-default`, `telemetry` with public source in https://github.com/anthropics/claude-code/tree/main/mods) and `claude plugin validate` to list a mod's hooks and calls before installing.

**Create a mod - Claude Code Docs** — 🔗 https://code.claude.com/docs/en/plugins/mods/create — 📅 unverified
Official tutorial (not opened; also surfaced through its `/docs/it/` and `/docs/de/` versions): ask Claude for a mod or write one yourself, building a mod that counts tool calls, shows the count beside the spinner and adds a command.

---

## Sources ranked by score

---

### 🔴 Essential (score 85–100)

No source reached this band: the YouTube tool failed, so no official or high-engagement video could be verified, and every community source is C-level authority.

---

### 🟠 High value (score 70–84)

**[1] Tickloop/claude-mods**
🔗 https://github.com/Tickloop/claude-mods
📅 2026-10-08 | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: A collection of Claude Code mods in TypeScript, created one week after launch and already at 77 stars. The description gives no detail on the individual mods.
**Score reason**: Exact match + C Community repository created 3 days ago, 77 stars
**Tags**: `mods-collection`, `typescript`, `community`

**[2] wh000wh000/awesome-claude-mods**
🔗 https://github.com/wh000wh000/awesome-claude-mods
📅 2026-10-04 | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Evidence-graded index of Claude Code mods, plugins and hooks, published in 20 languages and rebuilt every 2 hours. One of several catalogues that grade entries rather than simply list them.
**Score reason**: Exact match + C Community repository created 7 days ago, 47 stars
**Tags**: `catalogue`, `awesome-list`, `automated-index`

**[3] promptadvisers/claude-mods-computer-use-threads**
🔗 https://github.com/promptadvisers/claude-mods-computer-use-threads
📅 2026-10-05 | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Two mods that push past status displays: a Codex computer-use bridge and coordinated Claude sessions, shipped with source, build prompts, setup and tests. Shows mods used for cross-tool and cross-session orchestration.
**Score reason**: Exact match + C Community repository created 6 days ago, 11 stars
**Tags**: `multi-session`, `computer-use`, `orchestration`

**[4] Anthropic Launched Mods for Claude Code. Let's Build a Tiny One in TypeScript.**
🔗 https://dev.to/bobbyhalljr/anthropic-launched-mods-for-claude-code-lets-build-a-tiny-one-in-typescript-152h
📅 2026-10-05 | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Hands-on walkthrough by Bobby Hall Jr building a small mod in TypeScript (about 1,200 words including code).
⚠️ Contradicts Customize Claude Code with mods in TypeScript (claude.com/blog): the post dates Anthropic's announcement to October 3, 2026; the announcement is dated October 1, 2026.
**Score reason**: Exact match + C Community dev.to post published 6 days ago, about 1,200 words
**Tags**: `tutorial`, `typescript`, `first-mod`

**[5] What are Claude Code mods? What they can draw and where they run in the desktop app**
🔗 https://dev.to/nakadadev/what-are-claude-code-mods-what-they-can-draw-and-where-they-run-in-the-desktop-app-58pc
📅 2026-10-06 | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Explainer by Haruki Nakada focused on the interface side: what a mod can draw and on which surfaces it appears, with compatibility tables (about 1,100 words). Complements the "Where mods run" table of the official overview.
**Score reason**: Exact match + C Community dev.to post published 5 days ago, about 1,100 words
**Tags**: `interface`, `desktop-app`, `compatibility`

**[6] hamzafer/claude-code-mods**
🔗 https://github.com/hamzafer/claude-code-mods
📅 2026-10-02 | ⭐ Authority: C Community | 📊 Score: 74/100
**Summary**: The most-starred mod collection created after launch: live lines above the prompt, guards, panes and games, including a context bar, usage meter, Codex review watch, Markdown preview and Spotify now playing. A good sample of the range of what the drawing API allows.
**Score reason**: Exact match + C Community repository created 9 days ago, 183 stars
**Tags**: `mods-collection`, `status-band`, `typescript`

**[7] whyashthakker/awesome-claude-code-mods**
🔗 https://github.com/whyashthakker/awesome-claude-code-mods
📅 2026-10-03 | ⭐ Authority: C Community | 📊 Score: 72/100
**Summary**: Collection of 100+ mods usable with Claude Code, from utilities to games. Useful as a breadth indicator of the first week of community output.
**Score reason**: Exact match + C Community repository created 8 days ago, 46 stars
**Tags**: `catalogue`, `awesome-list`, `community`

**[8] zycck/claude-mods**
🔗 https://github.com/zycck/claude-mods
📅 2026-10-02 | ⭐ Authority: C Community | 📊 Score: 72/100
**Summary**: Single-purpose mods drawing live plan progress bars above the prompt. Representative of the dominant "band above the prompt" pattern.
**Score reason**: Exact match + C Community repository created 9 days ago, 46 stars
**Tags**: `status-band`, `plan-progress`, `typescript`

**[9] promptadvisers/claude-mods-starter-kit**
🔗 https://github.com/promptadvisers/claude-mods-starter-kit
📅 2026-10-02 | ⭐ Authority: C Community | 📊 Score: 72/100
**Summary**: Ten mods with beginner guides, creation prompts, safe demos and a build-your-own template. Oriented to learning by prompting Claude to write the mod, the path the official docs put first.
**Score reason**: Exact match + C Community repository created 9 days ago, 20 stars
**Tags**: `starter-kit`, `beginner`, `template`

**[10] nateherkai/claude-code-mods**
🔗 https://github.com/nateherkai/claude-code-mods
📅 2026-10-02 | ⭐ Authority: C Community | 📊 Score: 72/100
**Summary**: Four workflow mods: Cache Keeper, Recording Mode, Goal Meter and Collision Guard. Examples of mods that guard or track a session rather than decorate it.
**Score reason**: Exact match + C Community repository created 9 days ago, 18 stars
**Tags**: `guards`, `workflow`, `prompt-cache`

**[11] augiefra/claude-mods**
🔗 https://github.com/augiefra/claude-mods
📅 2026-10-02 | ⭐ Authority: C Community | 📊 Score: 72/100
**Summary**: One band above the prompt showing context in tokens, 5-hour and weekly limits against the clock, prompt cache countdown, session cost and running agents. The clearest instance of the usage-and-limits meter theme.
**Score reason**: Exact match + C Community repository created 9 days ago, 11 stars
**Tags**: `usage-meter`, `status-band`, `cost`

**[12] OneWave-AI/claude-code-mods**
🔗 https://github.com/OneWave-AI/claude-code-mods
📅 2026-10-02 | ⭐ Authority: C Community | 📊 Score: 72/100
**Summary**: Ten open-source mods: live panes, bands, status lines and tool-call guards (burn meter, launch codes, session wrapped, boss fight, code pet). Companion blog post, not opened: https://www.onewave-ai.com/blog/claude-code-mods.
**Score reason**: Exact match + C Community repository created 9 days ago, 11 stars
**Tags**: `mods-collection`, `tool-call-guards`, `panes`

**[13] AgriciDaniel/claude-mods-brain**
🔗 https://github.com/AgriciDaniel/claude-mods-brain
📅 2026-10-03 | ⭐ Authority: C Community | 📊 Score: 72/100
**Summary**: Source-cited Obsidian knowledge base about mods: how they work, how to build them and how to check one before installing it. A documentation artifact rather than code, directly reusable as a NotebookLM-style corpus.
**Score reason**: Exact match + C Community repository created 8 days ago, 10 stars
**Tags**: `knowledge-base`, `obsidian`, `security-review`

**[14] arasovic/claude-code-mods**
🔗 https://github.com/arasovic/claude-code-mods
📅 2026-10-02 | ⭐ Authority: C Community | 📊 Score: 72/100
**Summary**: Function-hook plugins that add live panes and behaviour to the terminal UI. Uses the "function hook" vocabulary of the underlying primitive.
**Score reason**: Exact match + C Community repository created 9 days ago, 6 stars
**Tags**: `function-hooks`, `panes`, `terminal-ui`

**[15] Claude Code Mods (course lesson, AI Development Setup)**
🔗 https://stevekinney.com/courses/ai-development-setup/claude-code-mods
📅 unverified | ⭐ Authority: B Expert | 📊 Score: 72/100
**Summary**: Lesson on mods inside Steve Kinney's AI development setup course (about 1,650 words). The page shows only "Last modified on October 6, 2026", no publication date.
**Score reason**: Exact match + B Expert (course author's site), about 1,650 words, publication date unverified
**Tags**: `course`, `setup`, `guide`

**[16] Claude Code mods: how to (MindStudio blog)**
🔗 https://www.mindstudio.ai/blog/claude-code-mods-how-to
📅 2026-10-03 | ⭐ Authority: C Community | 📊 Score: 72/100
**Summary**: How-to guide from MindStudio (about 1,200 words) described in search results as covering installation and five example mods.
**Score reason**: Exact match + C Community (vendor blog outside the topic), published 8 days ago, about 1,200 words
**Tags**: `how-to`, `installation`, `examples`

**[17] Claude Code Mods Just Landed: First Hook, Blast Radius Guard, and Why They're Not Sandboxed**
🔗 https://dev.to/yong_yu_f98e15562e9b120a0/claude-code-mods-just-landed-first-hook-blast-radius-guard-and-why-theyre-not-sandboxed-3225
📅 2026-10-02 | ⭐ Authority: C Community | 📊 Score: 72/100
**Summary**: Day-two post by YongBo Yu (about 1,300 words) covering a first hook, the `blast-radius` sample guard and the absence of sandboxing. Its title matches the official position that mods are not sandboxed.
**Score reason**: Exact match + C Community dev.to post published 9 days ago, about 1,300 words
**Tags**: `first-hook`, `blast-radius`, `security`

**[18] Claude Code mods: how to install and create (SmartScope)**
🔗 https://smartscope.blog/en/blog/claude-code-mods-how-to-install-create-2026/
📅 2026-10-02 | ⭐ Authority: C Community | 📊 Score: 72/100
**Summary**: Short install-and-create guide from the SmartScope blog (881 words, no named author), published the day after launch.
**Score reason**: Exact match + C Community blog published 9 days ago, 881 words
**Tags**: `install`, `create`, `guide`

---

### 🟡 Worth including (score 60–69)

**[19] Claude Code Mods Tutorial: Build and Test Your First Mod, Plus 15 Community Examples**
🔗 https://docs.kanaries.net/topics/AICoding/claude-code-mods
📅 unverified | ⭐ Authority: C Community | 📊 Score: 66/100
**Summary**: Long tutorial by Soren Atelier on Kanaries (about 4,500 words including code and tables) that builds and tests a first mod and lists 15 community examples. The page shows only "Updated on 10/7/2026", no publication date.
**Score reason**: Exact match + C Community, about 4,500 words, publication date unverified
**Tags**: `tutorial`, `testing`, `community-examples`

**[20] Claude Code Mods: The Complete Guide + 34 Videos (2026)**
🔗 https://app.stationx.net/articles/claude-code-mods
📅 unverified | ⭐ Authority: C Community | 📊 Score: 66/100
**Summary**: Very long guide by Nathan House (StationX), announced as a 30-minute read with 34 embedded videos; read truncated at 100,000 characters. The page shows only "Updated October 2026"; a possible pointer to the videos the failed YouTube search could not verify.
**Score reason**: Exact match + C Community, more than 1,500 words (truncated read), publication date unverified
**Tags**: `complete-guide`, `videos`, `security`

---

## Trends identified

- Launch-day burst: 9 of the 12 ranked repositories were created on 2026-10-02 or 2026-10-03, one or two days after the announcement; a few repositories outside the ranking (karanb192, darrell-tw, galElmalah) date from 2026-09-14 to 2026-09-16, consistent with the early-access period the docs mention without dating.
- The band above the prompt is the dominant use: context, usage limits, cache countdown, cost and plan progress meters recur across collections ([6], [8], [11], [12]), ahead of tool-call guards and well ahead of panes.
- Security review became a product category at once: catalogues grade or scan what each mod can read, write, run or send ([2], [13], and the cap-cut karanb192 catalogue), mirroring the official warning that mods are not sandboxed and the `claude plugin validate` listing.
- Catalogues multiply faster than they consolidate: at least four "awesome" lists appeared in the window ([2], [7], karanb192, hoobnn), with no reference index from Anthropic beyond its sample and built-in mods.
- Written guides agree with the docs on the requirements (v2.1.287, CLI and Desktop Code tab) but drift on dates: one ranked post [4] gives October 3 for the announcement, and search descriptions of unopened pages mention October 2 for default-on; the primary sources give October 1 for the launch and no date for early access.

---

*Generated by tech-watch skill | Sources used: GitHub · Web (Tier 2) · Owner domains*
*Scoring: Relevance 40% · Freshness 20% · Authority 20% · Depth 10% · Engagement 10%*
