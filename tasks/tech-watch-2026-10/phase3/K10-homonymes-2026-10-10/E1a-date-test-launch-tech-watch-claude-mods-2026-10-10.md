# Tech Watch — Claude Mods
**Date**: 2026-10-10 | **Window**: 30 days | **Sources**: 20 ranked + 4 primary

**Pipeline counts**: 63 raw results (arXiv 0, GitHub 20, YouTube 15, web 28) → 50 on-topic, 1 adjacent, 10 homonyms, 2 dropped unlabeled (1 video under 3 min, 1 result without a usable title) → 46 unique on-topic after deduplication (1 moved to the primary block, 45 scored) → 34 reach 60/100 → 20 kept (cap).
**Enrichment**: 10 of 10 pages opened, 0 failures. Tier 3 not run (unique on-topic ≥ 12).

**Coverage notes**
- Queries: arXiv `"Claude Code" mods`, GitHub `claude code mods`, YouTube `Claude Code mods`. 0 arXiv papers, as expected for a product feature.
- Date test: the announcement fixes the launch on 2026-10-01, so 4 repositories created between 2026-09-14 and 2026-09-16 were labelled homonyms and left the pipeline, including `karanb192/awesome-claude-code-mods` (456 stars, the most starred result). The official overview mentions an early-access period (`CLAUDE_CODE_ENABLE_FUNCTION_HOOKS`), so these repositories may well be about mods built during early access. The rule was applied as written; review this exclusion if early-access material matters to you.
- 14 sources scored 60 or more but fell under the cap of 20 (ties at 77 broken on stars or views): 2 videos, 7 repositories, 5 web pages.
- 11 web pages were not opened (budget of 10 spent) and score 59 with date and length `unverified`: they are excluded, not judged poor.
- Summaries below rely on titles, tool descriptions and the three values extracted per page (date, length, author). Article bodies were not read for content, so the contradiction check covers titles and descriptions only: none contradicts a primary source.
- The changelog page was read only down to v2.1.288 (first 100,000 characters of about 1,050,000). The v2.1.287 entry itself was not read.

---

## Executive Summary
Mods are a ten-day-old Claude Code feature (announced 2026-10-01): JavaScript or TypeScript event handlers shipped inside plugins that can draw UI, intercept tool calls and add commands, running in-process and without a sandbox. The ecosystem response is immediate and mostly shallow: creator "N mods you need" videos and personal mod collections dominate, while catalogue and audit projects appear within days, signalling that trust in third-party mods is already a concern. The official changelog shows near-daily mod fixes since launch, several of them about user-installed mods bypassing organization guards, so the API and its security boundary are still moving.

---

## Primary sources

**Customize Claude Code with mods in TypeScript** — 🔗 https://claude.com/resources/articles/claude-code-mods — 📅 2026-10-01
Launch announcement by Anthropic ("Today we're introducing mods"): available in the Claude Code CLI and desktop app, shipped inside plugins, not sandboxed; on Team and Enterprise plans and managed machines the built-in `sec-default` mod loads first. No minimum version stated on this page.

**Mods overview - Claude Code Docs** — 🔗 https://code.claude.com/docs/en/plugins/mods/overview — 📅 unverified
Reference definition: a mod is a plugin made of JavaScript or TypeScript event handlers. On by default; terminal requires Claude Code v2.1.287 or later, Desktop app from v2.1.286. Hooks run in the CLI, Desktop Code tab, VS Code extension, `claude -p` and Agent SDK; drawing appears only in the terminal and Desktop app. Mods run with the user's permissions and are not sandboxed; `claude plugin validate` lists a mod's hooks and calls before install. Sample mods: `token-weather`, `blast-radius`, `replay-theater` in `anthropics/claude-code-playground`.

**Claude Code changelog** — 🔗 https://code.claude.com/docs/en/changelog — 📅 latest entry 2026-10-09 (v2.1.296)
Mod-related entries in every release read from v2.1.288 (2026-10-02) to v2.1.296 (2026-10-09): new API surface (`$.ui.notify`, `prompt.autocomplete`, prompt caching in `$.model.complete`) and fixes, several on user-installed mods bypassing organization guards. Partially read (see coverage notes).

**Create a mod - Claude Code Docs** — 🔗 https://code.claude.com/docs/en/plugins/mods/create — 📅 unverified
Official tutorial (not opened; found in search under its English, German and `.md` variants). Per the overview page, it builds a mod that counts tool calls, shows the count beside the spinner and adds a command.

---

## Sources ranked by score

---

### 🔴 Essential (score 85–100)

**[1] Mods in Claude Code: change how Claude Code works**
🔗 https://www.youtube.com/watch?v=yUuFvL1lK4k
📅 2026-10-05 | ⭐ Authority: A Primary | 📊 Score: 94/100
**Summary**: Official video from the Claude channel (3:21) presenting mods as functions you write that change what Claude Code renders, what goes into a prompt, and more. The only first-party video in the results.
**Score reason**: Exact match + A Primary (official channel), published 5 days ago, 371,756 views
**Tags**: `official`, `overview`, `video`

**[2] Claude Code Mods Can Do Basically Anything...**
🔗 https://www.youtube.com/watch?v=EiThSVZ8pME
📅 2026-10-04 | ⭐ Authority: B Expert | 📊 Score: 88/100
**Summary**: Better Stack (7:37) describes mods as small TypeScript plugins running inside Claude Code that change behavior and draw custom UI. A 1:29 Short from the same channel on the same subject was dropped at the duration filter.
**Score reason**: Exact match + B Expert (established engineering organization channel), published 6 days ago, 38,881 views
**Tags**: `demo`, `typescript`, `video`

**[3] 9 NEW Claude Mods that can truly change how you work**
🔗 https://www.youtube.com/watch?v=lDrAZ1wAyVs
📅 2026-10-08 | ⭐ Authority: C Community | 📊 Score: 85/100
**Summary**: Jay E | RoboNuggets (12:47) walks through nine mods; the description promotes a free PDF guide. Most viewed result of the watch.
**Score reason**: Exact match + C Community (YouTube creator), published 2 days ago, 430,694 views
**Tags**: `mod-roundup`, `video`, `creator`

**[4] Claude Code Just Dropped Mods: Here Are 5 You Need**
🔗 https://www.youtube.com/watch?v=W5JSvXig3Ig
📅 2026-10-06 | ⭐ Authority: C Community | 📊 Score: 85/100
**Summary**: Sharbel A. (11:33) presents five mods; install commands and a mod-building prompt are offered through an external link.
**Score reason**: Exact match + C Community (YouTube creator), published 4 days ago, 24,901 views
**Tags**: `mod-roundup`, `video`, `creator`

**[5] Claude Mods Are Insane... You Need To Try These Right Now**
🔗 https://www.youtube.com/watch?v=ERNqRK6sMJY
📅 2026-10-09 | ⭐ Authority: C Community | 📊 Score: 85/100
**Summary**: AI LABS (13:28) covers seven Claude Code mods. Sponsored video (Runway).
**Score reason**: Exact match + C Community (YouTube creator), published 1 day ago, 18,837 views
**Tags**: `mod-roundup`, `video`, `sponsored`

**[6] 3 Claude Code mods you need to build**
🔗 https://www.youtube.com/watch?v=WCwNECxFJ_Q
📅 2026-10-05 | ⭐ Authority: C Community | 📊 Score: 85/100
**Summary**: Build Great Products (13:43) focuses on building three mods rather than installing existing ones; the description promotes a playbook in a Skool community.
**Score reason**: Exact match + C Community (YouTube creator), published 5 days ago, 13,058 views
**Tags**: `build-your-own`, `video`, `creator`

---

### 🟠 High value (score 70–84)

**[7] Claude Code Mods: The Ultimate Customization Guide**
🔗 https://www.youtube.com/watch?v=8wZVnc99x_k
📅 2026-10-08 | ⭐ Authority: C Community | 📊 Score: 82/100
**Summary**: Eric Tech (9:53) explains what mods are, framed as changing how Claude Code looks and works, not just what it knows.
**Score reason**: Exact match + C Community (YouTube creator), published 2 days ago, 11,624 views
**Tags**: `explainer`, `customization`, `video`

**[8] Claude Code Mods: What They Are and How to Write One**
🔗 https://www.developersdigest.tech/blog/claude-code-mods-guide-2026
📅 2026-10-06 | ⭐ Authority: C Community | 📊 Score: 81/100
**Summary**: Written guide of about 1,800 words on what mods are and how to write one; no author named on the page. Whether it adds content beyond the official tutorial was not checked.
**Score reason**: Exact match + C Community (blog, no named author), published 4 days ago, > 1500 words
**Tags**: `guide`, `how-to`, `article`

**[9] Claude Code Mods Just Turned Agents Into a Platform**
🔗 https://dev.to/max_quimby/claude-code-mods-just-turned-agents-into-a-platform-5gc0
📅 2026-10-04 | ⭐ Authority: C Community | 📊 Score: 81/100
**Summary**: Opinion and analysis piece by Max Quimby (about 2,200 words) reading mods as a platform move. The page says it was first published on agentconn.com; the original URL was not retrieved, so the dev.to copy is cited.
**Score reason**: Exact match + C Community (dev.to post), published 6 days ago, > 1500 words
**Tags**: `analysis`, `platform`, `article`

**[10] Claude Code Mods Are Game Changers. Set Up These 5 NOW.**
🔗 https://www.youtube.com/watch?v=9hetShMMp2s
📅 2026-10-02 | ⭐ Authority: C Community | 📊 Score: 80/100
**Summary**: Nate Herk (11:19) sets up five mods, one day after launch. Companion repository: https://github.com/nateherkai/claude-code-mods (four mods: Cache Keeper, Recording Mode, Goal Meter, Collision Guard; 17 stars, created 2026-10-02).
**Score reason**: Exact match + C Community (YouTube creator), published 8 days ago, 222,014 views
**Tags**: `mod-roundup`, `video`, `companion-repo`

**[11] Claude Code vient de lancer les mods : voici mes 5 indispensables**
🔗 https://www.youtube.com/watch?v=1Dlh_Mqze1s
📅 2026-10-09 | ⭐ Authority: C Community | 📊 Score: 80/100
**Summary**: French-language video by Tony Lotis (13:20) presenting five mods; the mods and a mod-creation skill are distributed through a paid community. The only French-language source of the watch.
**Score reason**: Exact match + C Community (YouTube creator), published 1 day ago, 7,804 views
**Tags**: `french`, `mod-roundup`, `video`

**[12] Claude Mods Is The Biggest Claude Code Upgrade Since Skills**
🔗 https://www.youtube.com/watch?v=Rn4nmFRPe0s
📅 2026-10-02 | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Chase AI (9:11) positions mods relative to skills, one day after launch. The description contains only community links.
**Score reason**: Exact match + C Community (YouTube creator), published 8 days ago, 212,429 views
**Tags**: `explainer`, `skills-comparison`, `video`

**[13] Claude Mods Just Dropped... Use these 3 NOW**
🔗 https://www.youtube.com/watch?v=moOBIaIb4a8
📅 2026-10-02 | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Jack Roberts (9:00) presents three mods the day after launch and links a prompt for finding suitable mods.
**Score reason**: Exact match + C Community (YouTube creator), published 8 days ago, 41,372 views
**Tags**: `mod-roundup`, `video`, `creator`

**[14] Tickloop/claude-mods**
🔗 https://github.com/Tickloop/claude-mods
📅 2026-10-08 (created) | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: "A collection of claude code mods" in TypeScript. No further detail in the repository description.
**Score reason**: Exact match + C Community repository created 2 days ago, 77 stars
**Tags**: `mod-collection`, `typescript`, `repository`

**[15] whyashthakker/awesome-claude-code-mods**
🔗 https://github.com/whyashthakker/awesome-claude-code-mods
📅 2026-10-03 (created) | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Describes itself as a collection of 100+ mods usable with Claude Code. Count not verified.
**Score reason**: Exact match + C Community repository created 7 days ago, 43 stars
**Tags**: `awesome-list`, `catalogue`, `repository`

**[16] wh000wh000/awesome-claude-mods**
🔗 https://github.com/wh000wh000/awesome-claude-mods
📅 2026-10-04 (created) | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Describes itself as an evidence-graded index of Claude Code mods, plugins and hooks, in 20 languages, rebuilt every 2 hours. An automated index rather than a hand-curated list.
**Score reason**: Exact match + C Community repository created 6 days ago, 39 stars
**Tags**: `index`, `automated`, `repository`

**[17] aieo-product/claude_qamods**
🔗 https://github.com/aieo-product/claude_qamods
📅 2026-10-04 (created) | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Mods that make Claude's questions easier to read and answer (topic tag `askuserquestion`). An example of a mod restyling Claude Code's own dialogs, a capability the official overview lists.
**Score reason**: Exact match + C Community repository created 6 days ago, 11 stars
**Tags**: `ui-restyle`, `single-purpose`, `repository`

**[18] promptadvisers/claude-mods-computer-use-threads**
🔗 https://github.com/promptadvisers/claude-mods-computer-use-threads
📅 2026-10-05 (created) | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Two mods: a Codex computer-use bridge and coordinated Claude sessions, with source, build prompts, setup and tests. Companion repository from the same author: https://github.com/promptadvisers/claude-mods-starter-kit (ten mods, beginner guides and a template; 19 stars, created 2026-10-02).
**Score reason**: Exact match + C Community repository created 5 days ago, 11 stars
**Tags**: `multi-session`, `codex`, `repository`

**[19] AgriciDaniel/claude-mods-brain**
🔗 https://github.com/AgriciDaniel/claude-mods-brain
📅 2026-10-03 (created) | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Source-cited Obsidian knowledge base about mods: how they work, how to build one, and how to check one before installing it. Documentation rather than mod code.
**Score reason**: Exact match + C Community repository created 7 days ago, 9 stars
**Tags**: `knowledge-base`, `security-review`, `repository`

**[20] ersinkoc/claude-mods**
🔗 https://github.com/ersinkoc/claude-mods
📅 2026-10-09 (created) | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: "KOZMOS": visual mods for the CLI and desktop app (bands above the prompt, sidebars, status ticker, companions, guards, sound). The newest repository in the results.
**Score reason**: Exact match + C Community repository created 1 day ago, 9 stars
**Tags**: `ui`, `desktop`, `repository`

---

### 🟡 Worth including (score 60–69)

None listed: the cap of 20 was reached at score 77. Sources that reached 60 but fell under the cap:

| Score | Source | URL |
|---|---|---|
| 77 | Anthropic Launched Mods for Claude Code. Let's Build a Tiny One in TypeScript (Bobby Hall Jr, dev.to, 2026-10-05) | https://dev.to/bobbyhalljr/anthropic-launched-mods-for-claude-code-lets-build-a-tiny-one-in-typescript-152h |
| 77 | What are Claude Code mods? What they can draw and where they run in the desktop app (Haruki Nakada, dev.to, 2026-10-06) | https://dev.to/nakadadev/what-are-claude-code-mods-what-they-can-draw-and-where-they-run-in-the-desktop-app-58pc |
| 75 | Claude Code Mods Are INSANE (Master it in 9 minutes) (Shab Noor, 2026-10-08) | https://www.youtube.com/watch?v=oL6yb21XhDQ |
| 75 | Claude Mods Are Insane (Real Claude Code Upgrade) (Gundeep Ai, 2026-10-09) | https://www.youtube.com/watch?v=ZJ45whWptH8 |
| 74 | hamzafer/claude-code-mods (177 stars, created 2026-10-02) | https://github.com/hamzafer/claude-code-mods |
| 72 | zycck/claude-mods (42 stars, created 2026-10-02) | https://github.com/zycck/claude-mods |
| 72 | augiefra/claude-mods (11 stars, created 2026-10-02) | https://github.com/augiefra/claude-mods |
| 72 | OneWave-AI/claude-code-mods (10 stars, created 2026-10-02) | https://github.com/OneWave-AI/claude-code-mods |
| 72 | claudekit / updates / claude-code-mods (ClaudeKit, 2026-10-01) | https://claudekit.io/en/updates/claude-code-mods/ |
| 66 | Claude Code Mods: The Complete Guide + 34 Videos (StationX, date unverified) | https://app.stationx.net/articles/claude-code-mods |
| 66 | Claude Code Mods Tutorial: Build and Test Your First Mod, Plus 15 Community Examples (Kanaries, date unverified) | https://docs.kanaries.net/topics/AICoding/claude-code-mods |
| 64 | JohnnyVizz/claude-kit (skills and mods, partial match; 121 stars, created 2026-10-04) | https://github.com/JohnnyVizz/claude-kit |

The two remaining repositories at 72 (`nateherkai/claude-code-mods`, `promptadvisers/claude-mods-starter-kit`) are folded into entries [10] and [18].

---

## Adjacent, not ranked

- He Finally 10x Claude Code With This Method (AI LABS) — https://www.youtube.com/watch?v=qLfSDQ5NGh0 — about loop engineering with Claude Code, not about mods.

---

## Trends identified

- Creator videos set the tone within 24 to 48 hours of the 2026-10-01 launch, almost all in the "N mods you need" format; several gate the actual mods behind paid or lead-capture communities, and only one first-party video exists.
- GitHub activity is a burst of small personal collections: 14 on-topic repositories created between 2026-10-02 and 2026-10-09, most under 100 stars, with no dominant reference besides Anthropic's own sample and built-in mods.
- Catalogues and audit tooling appeared as fast as the mods themselves (awesome lists, an automated graded index, a knowledge base on checking a mod before install), which matches the primary sources' insistence that mods are unsandboxed and run with the user's permissions.
- Dominant use cases in repository descriptions are status displays above the prompt (context, usage limits, cost, plan progress) and tool-call guards; novelty mods (games, pets, music) are a visible second group.
- The API is not stable yet: the official changelog lists mod additions and fixes in every release read between 2026-10-02 and 2026-10-09, including several guard-bypass fixes, so tutorials from launch week may age quickly.

---

*Generated by tech-watch skill | Sources: arXiv · GitHub · YouTube · Web search*
*Scoring: Relevance 40% · Freshness 20% · Authority 20% · Depth 10% · Engagement 10%*
