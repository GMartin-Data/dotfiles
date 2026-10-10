# Tech Watch — Claude Code mods
**Date**: 2026-10-10 | **Window**: 30 days | **Sources**: 20 ranked + 3 primary

**Request**: "Claude Mods" | **Queries**: arXiv `"Claude Code" mods` · GitHub `claude code mods` · YouTube `Claude Code mods`
**Results**: 63 raw (arXiv 0, GitHub 20, YouTube 15, Tier 2 web 28) → 57 on-topic, 0 adjacent, 1 off-topic, 5 dropped unlabeled (1 video under 3 min, 4 results without a usable title) → 53 unique on-topic after deduplication
**Tiers run**: 1 and 2. Tier 3 not run (53 unique on-topic ≥ 12).
**Enrichment**: 10 / 10 pages opened (3 primary, 7 web candidates), 0 failures.
**Coverage note**: 36 on-topic results reach 60; the cap of 20 applies. The 16 results left out by the cap score 62–77 (mostly community repositories, plus two verified guides at 77: stevekinney.com and mindstudio.ai, tied with the last ranked entries and placed behind them on the engagement tie-break). 15 web pages that were not opened keep an `unverified` date and length and score 59, below the threshold. 0 arXiv papers: expected for a product feature.

---

## Executive Summary
Anthropic announced mods on 2026-10-01: JavaScript/TypeScript event handlers shipped inside plugins that run in Claude Code's own process and can draw panes and bands, rewrite prompts, and hold, answer or approve tool calls. Ten days later the dominant pattern is a very fast community build-out (dozens of mod collections and several competing "awesome" catalogues created within a week, "N mods to install now" videos with six-figure view counts) running ahead of a security model in which mods are explicitly not sandboxed and the built-in guard only loads on Team, Enterprise or managed machines. The unexpected finding is how unsettled the API still is: the changelog shows mod-related additions and guard-bypass fixes in almost every release between 2.1.288 and 2.1.296, so any guide older than a few days may already be outdated.

---

## Primary sources

**Mods overview — Claude Code Docs** — 🔗 https://code.claude.com/docs/en/plugins/mods/overview — 📅 unverified
Establishes the reference facts: mods are on by default; terminal requires Claude Code v2.1.287 or later, the Desktop app's bundled copy from v2.1.286; the early-access variable `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS` is ignored from v2.1.287. Hooks run in the terminal, Desktop Code tab, VS Code chat panel, `claude -p`/Agent SDK and cloud sessions, but drawing only appears in the terminal and the Desktop app (no plugins in Desktop WSL sessions). Mods are not sandboxed and run with the user's permissions; `claude plugin validate` lists a mod's hooks and calls before install. Sample mods (`token-weather`, `blast-radius`, `replay-theater`) are in `anthropics/claude-code-playground`; source of four built-in mods (`diff`, `agents-md`, `sec-default`, `telemetry`) is in `anthropics/claude-code/mods`.

**Customize Claude Code with mods** (Anthropic announcement) — 🔗 https://claude.com/blog/claude-code-mods — 📅 2026-10-01
Establishes the announcement date and availability ("available today in the Claude Code CLI and desktop app"), distribution through plugins and `/plugin`, the trust warning (not sandboxed, same machine access as Claude Code), and that `sec-default` loads first on Team, Enterprise or managed-settings machines. No minimum version and no beta/GA label is stated on this page.

**Claude Code changelog** — 🔗 https://code.claude.com/docs/en/changelog — 📅 entries read from 2026-10-02 (2.1.288) to 2026-10-09 (2.1.296)
Establishes the release cadence after launch: mod-related entries in 2.1.288, 2.1.289, 2.1.290, 2.1.292, 2.1.293, 2.1.295 and 2.1.296, including new API surface (`$.ui.selection()`, `prompt.autocomplete`, prompt caching in `$.model.complete`, `$.ui.notify`, `isDeferred` in `$.tool.register`) and several fixes where a user-installed mod could bypass or unload an organization's guard. The page was read only up to the start of 2.1.288; the 2.1.287 entry itself was not read.

Related official pages returned by the primary search, not opened: [Create a mod](https://code.claude.com/docs/en/plugins/mods/create), [Use the mods API](https://code.claude.com/docs/en/plugins/mods/api), [Draw in the interface](https://code.claude.com/docs/en/plugins/mods/interface), [React to events](https://code.claude.com/docs/en/plugins/mods/events), [Manage mods for your organization](https://code.claude.com/docs/en/plugins/mods/admin).

---

## Sources ranked by score

---

### 🔴 Essential (score 85–100)

**[1] Mods in Claude Code: change how Claude Code works**
🔗 https://www.youtube.com/watch?v=yUuFvL1lK4k
📅 2026-10-05 | ⭐ Authority: A Primary | 📊 Score: 94/100
**Summary**: Official video from the Claude channel (3:21) presenting mods as functions that change what Claude Code renders, what goes into a prompt, and how tool calls are handled. It is the vendor's own framing of the feature and the shortest authoritative introduction.
**Score reason**: Exact match + A Primary (official channel), published 5 days ago, 371k views
**Tags**: `official`, `introduction`, `video`

**[2] 9 NEW Claude Mods that can truly change how you work**
🔗 https://www.youtube.com/watch?v=lDrAZ1wAyVs
📅 2026-10-08 | ⭐ Authority: C Community | 📊 Score: 85/100
**Summary**: Walkthrough of nine mods (12:47) from Jay E / RoboNuggets, the most viewed community video of the window. Useful as a snapshot of which mod ideas the non-developer audience is adopting; a PDF guide is offered as a lead magnet.
**Score reason**: Exact match + C Community (YouTube creator), published 2 days ago, 430k views
**Tags**: `mod-roundup`, `video`, `workflow`

**[3] Claude Mods - The Biggest Claude Code Upgrade!**
🔗 https://www.youtube.com/watch?v=XaYubuLtW8M
📅 2026-10-03 | ⭐ Authority: C Community | 📊 Score: 85/100
**Summary**: Prompt Engineering channel (10:37) explains mods as JavaScript or TypeScript functions running inside Claude Code that can watch, change or answer events. More mechanism-oriented than the "top N" videos.
**Score reason**: Exact match + C Community (YouTube creator), published 7 days ago, 65k views
**Tags**: `explainer`, `video`, `hooks`

**[4] These Mods Take Claude Code to Another Level**
🔗 https://www.youtube.com/watch?v=UcvD53jqHRU
📅 2026-10-05 | ⭐ Authority: C Community | 📊 Score: 85/100
**Summary**: Mark Kashef (15:41) demonstrates a set of mods and distributes their code and prompts. One of the longer build-oriented videos of the window.
**Score reason**: Exact match + C Community (YouTube creator), published 5 days ago, 38k views
**Tags**: `mod-roundup`, `video`, `build`

**[5] Claude Mods Are Insane... You Need To Try These Right Now**
🔗 https://www.youtube.com/watch?v=ERNqRK6sMJY
📅 2026-10-09 | ⭐ Authority: C Community | 📊 Score: 85/100
**Summary**: AI LABS (13:28) presents seven Claude Code mods. Most recent of the roundup videos, so it reflects the ecosystem after the first week of releases. Sponsored content in the description.
**Score reason**: Exact match + C Community (YouTube creator), published 1 day ago, 18.7k views
**Tags**: `mod-roundup`, `video`

**[6] 3 Claude Code mods you need to build**
🔗 https://www.youtube.com/watch?v=WCwNECxFJ_Q
📅 2026-10-05 | ⭐ Authority: C Community | 📊 Score: 85/100
**Summary**: Build Great Products (13:43) focuses on building three mods rather than installing existing ones, which matches the official "ask Claude for a mod" path.
**Score reason**: Exact match + C Community (YouTube creator), published 5 days ago, 13k views
**Tags**: `build`, `video`, `tutorial`

---

### 🟠 High value (score 70–84)

**[7] Claude Code mods let you customize the interface, commands and more**
🔗 https://www.it-connect.tech/claude-code-mods-let-you-customize-the-interface-commands-and-more/
📅 2026-10-05 | ⭐ Authority: B Expert | 📊 Score: 83/100
**Summary**: News article by Florian Burnel (IT-Connect, about 1,100 words) covering the announcement, the v2.1.287 default, CLI and Desktop availability, and the fact that Claude Code sandboxing isolates only Claude's Bash commands, not mods. Its facts match the official docs; a French edition exists at it-connect.fr.
**Score reason**: Exact match + B Expert (established IT publication), published 5 days ago
**Tags**: `news`, `security`, `sysadmin`

**[8] Claude Code Mods Can Do Basically Anything...**
🔗 https://www.youtube.com/watch?v=EiThSVZ8pME
📅 2026-10-04 | ⭐ Authority: C Community | 📊 Score: 82/100
**Summary**: Better Stack (7:37) describes mods as small TypeScript plugins running inside Claude Code and shows custom drawing and behavior changes. Developer-oriented and concise.
**Score reason**: Exact match + C Community (YouTube creator), published 6 days ago, 38.9k views
**Tags**: `explainer`, `video`, `typescript`

**[9] Claude Code Mods: The Ultimate Customization Guide**
🔗 https://www.youtube.com/watch?v=8wZVnc99x_k
📅 2026-10-08 | ⭐ Authority: C Community | 📊 Score: 82/100
**Summary**: Eric Tech (9:53) explains what mods are and how they change both the look and the behavior of Claude Code, positioned as a customization guide.
**Score reason**: Exact match + C Community (YouTube creator), published 2 days ago, 11.6k views
**Tags**: `guide`, `video`, `customization`

**[10] Claude Code Mods Tutorial: Build and Test Your First Mod, Plus 15 Community Examples**
🔗 https://docs.kanaries.net/topics/AICoding/claude-code-mods
📅 2026-10-07 (page "Updated on") | ⭐ Authority: C Community | 📊 Score: 81/100
**Summary**: Long hands-on tutorial (about 5,000 words, Soren Atelier for Kanaries) that builds and tests a first mod and lists 15 community examples. It reproduces the official version requirements (2.1.287 terminal, 2.1.286 Desktop) and the where-mods-run matrix, and notes that a mod can approve a call a deny rule refuses on an unmanaged machine.
**Score reason**: Exact match + C Community (vendor blog), updated 3 days ago, over 1,500 words
**Tags**: `tutorial`, `testing`, `examples`

**[11] Claude Code Mods Just Turned Agents Into a Platform**
🔗 https://dev.to/max_quimby/claude-code-mods-just-turned-agents-into-a-platform-5gc0
📅 2026-10-04 | ⭐ Authority: C Community | 📊 Score: 81/100
**Summary**: Analysis piece (about 2,000 words, Max Quimby, originally on AgentConn) arguing that mods turn Claude Code into a platform, with coverage of marketplaces and the absence of code review or signing for mods.
⚠️ Contradicts Mods overview (Claude Code Docs): the article lists Anthropic's four built-in mods as `/diff`, `sec-default`, `telemetry` and a test framework; the docs list six built-in entries and publish source for `diff`, `agents-md`, `sec-default` and `telemetry`, with no test-framework mod.
**Score reason**: Exact match + C Community (dev.to post), published 6 days ago, over 1,500 words
**Tags**: `analysis`, `platform`, `marketplace`

**[12] Claude Code Mods Are Game Changers. Set Up These 5 NOW.**
🔗 https://www.youtube.com/watch?v=9hetShMMp2s
📅 2026-10-02 | ⭐ Authority: C Community | 📊 Score: 80/100
**Summary**: Nate Herk (11:19) sets up five mods the day after the announcement; the matching repository `nateherkai/claude-code-mods` (Cache Keeper, Recording Mode, Goal Meter, Collision Guard) was created the same day. A Medium post with the same title duplicates this content.
**Score reason**: Exact match + C Community (YouTube creator), published 8 days ago, 222k views
**Tags**: `mod-roundup`, `video`, `setup`

**[13] Claude Code vient de lancer les mods : voici mes 5 indispensables**
🔗 https://www.youtube.com/watch?v=1Dlh_Mqze1s
📅 2026-10-09 | ⭐ Authority: C Community | 📊 Score: 80/100
**Summary**: French-language video by Tony Lotis (13:20) presenting five mods and a skill to create new ones. The only French-language source returned by the tools.
**Score reason**: Exact match + C Community (YouTube creator), published 1 day ago, 7.7k views
**Tags**: `french`, `mod-roundup`, `video`

**[14] Claude Mods Is The Biggest Claude Code Upgrade Since Skills**
🔗 https://www.youtube.com/watch?v=Rn4nmFRPe0s
📅 2026-10-02 | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Chase AI (9:11) frames mods as the largest Claude Code extension point since skills. Published the day after the announcement, so it predates the later changelog additions.
**Score reason**: Exact match + C Community (YouTube creator), published 8 days ago, 212k views
**Tags**: `explainer`, `video`, `launch-reaction`

**[15] Claude Mods Just Dropped... Use these 3 NOW**
🔗 https://www.youtube.com/watch?v=moOBIaIb4a8
📅 2026-10-02 | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Jack Roberts (9:00) presents three mods on launch-plus-one day, with a prompt to find mods suited to a given workflow.
**Score reason**: Exact match + C Community (YouTube creator), published 8 days ago, 41k views
**Tags**: `mod-roundup`, `video`, `launch-reaction`

**[16] Tickloop/claude-mods**
🔗 https://github.com/Tickloop/claude-mods
📅 2026-10-08 (created) | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: TypeScript collection of Claude Code mods created two days before this watch and already at 77 stars, the fastest-growing of the recent collections.
**Score reason**: Exact match + C Community repository created 2 days ago, 77 stars
**Tags**: `repository`, `collection`, `typescript`

**[17] whyashthakker/awesome-claude-code-mods**
🔗 https://github.com/whyashthakker/awesome-claude-code-mods
📅 2026-10-03 (created) | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Collection announced as 100+ mods usable with Claude Code. One of three competing "awesome" lists created within three weeks.
**Score reason**: Exact match + C Community repository created 7 days ago, 43 stars
**Tags**: `repository`, `awesome-list`, `catalogue`

**[18] wh000wh000/awesome-claude-mods**
🔗 https://github.com/wh000wh000/awesome-claude-mods
📅 2026-10-04 (created) | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Index of Claude Code mods, plugins and hooks described as evidence-graded, available in 20 languages and rebuilt every 2 hours. Notable for attempting to grade entries rather than only listing them.
**Score reason**: Exact match + C Community repository created 6 days ago, 39 stars
**Tags**: `repository`, `awesome-list`, `automated-index`

**[19] promptadvisers/claude-mods-computer-use-threads**
🔗 https://github.com/promptadvisers/claude-mods-computer-use-threads
📅 2026-10-05 (created) | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Two mods with source, build prompts, setup and tests: a Codex computer-use bridge and coordinated Claude sessions. Illustrates mods used for cross-session and cross-tool orchestration rather than display.
**Score reason**: Exact match + C Community repository created 5 days ago, 11 stars
**Tags**: `repository`, `orchestration`, `multi-session`

**[20] aieo-product/claude_qamods**
🔗 https://github.com/aieo-product/claude_qamods
📅 2026-10-04 (created) | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Mods that restyle the questions Claude asks the user (AskUserQuestion) so they are easier to read and answer. A concrete example of redrawing Claude Code's own interface, one of the capabilities listed in the official overview.
**Score reason**: Exact match + C Community repository created 6 days ago, 11 stars
**Tags**: `repository`, `interface`, `askuserquestion`

---

### 🟡 Worth including (score 60–69)

No source in this band is listed: the cap of 20 is reached by sources scoring 77 or more (see the coverage note).

---

## Trends identified

- **Display mods dominate.** Most community repositories put information in a band above the prompt: context and token usage, 5-hour and weekly limits, cache countdown, plan progress, session cost. Guards and tool-call rewriting, the more powerful half of the API, are much less represented.
- **Catalogues appeared before curation.** At least three "awesome" lists and one knowledge base were created between 2026-09-15 and 2026-10-04, some rebuilt automatically from GitHub scans. Search snippets report catalogue sizes in the thousands within days of launch; those counts were not verified here.
- **Security is the consistent caveat in written sources, not in videos.** Every opened article that addresses the subject repeats the official position (not sandboxed, user permissions, `sec-default` only on Team, Enterprise or managed machines, `claude plugin validate` before install) and several add that on a personal machine a mod can approve what a deny rule refuses. Video titles and descriptions focus on "install these now".
- **The API is moving weekly.** Seven releases in eight days carry mod-related changes, including fixes for mods bypassing or unloading an organization's guard. Sources dated 2026-10-02 describe an older state than the docs.
- **Early-access content is still in circulation.** Repositories created from 2026-09-14 and a 2026-09-18 video calling mods a "hidden feature" predate the announcement; the docs confirm an early-access period gated by `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS`, now ignored. Instructions from that period (setting the variable) no longer apply.

---

*Generated by tech-watch skill | Sources: arXiv · GitHub · YouTube · Web search*
*Scoring: Relevance 40% · Freshness 20% · Authority 20% · Depth 10% · Engagement 10%*
