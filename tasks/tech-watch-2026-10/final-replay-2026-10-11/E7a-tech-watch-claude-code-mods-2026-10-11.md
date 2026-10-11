# Tech Watch — Claude Code mods
**Date**: 2026-10-11 | **Window**: 30 days | **Request**: "mods de Claude Code" | **Owner**: Anthropic | **Sources**: 20 ranked + 3 primary

| Source | Status | Raw | On-topic | In report |
|---|---|---|---|---|
| arXiv | empty | 0 | 0 | 0 |
| GitHub | ok | 20 | 19 | 3 |
| YouTube | ok | 15 | 15 | 12 |
| Web (Tier 2) | ok | 28 | 28 | 5 |
| Web (Tier 3) | not run (unique on-topic ≥ 12) | – | – | 0 |
| Owner domains | ok | 10 | – | 3 |

**Pipeline**: 63 raw → 62 on-topic, 0 adjacent, 1 homonyms, 0 dropped → 58 unique → 39 ≥ 60 → 20 ranked (cap 20).
**Enrichment**: 10/10 pages opened (3 primary), 0 failures, 2 truncated.
**Date test**: skipped (the Mods overview mentions an early-access period without dating it; the changelog was truncated before any entry that could date it).
**Notes**:
- Cap cut: 19 sources scored ≥ 60 but fall below the 20th rank (score 77). Best of them: Gundeep Ai video (75), `hamzafer/claude-code-mods` (74, 183 stars), eight repositories at 72 (among them `whyashthakker/awesome-claude-code-mods`, `zycck/claude-mods`, `nateherkai/claude-code-mods`, `AgriciDaniel/claude-mods-brain`, `OneWave-AI/claude-code-mods`), the dev.to post by Yong Yu on blast-radius and sandboxing (72), Firecrawl video (68), Station X guide (66), `karanb192/awesome-claude-code-mods` (64, 477 stars).
- Unopened pages: 17 unique Tier 2 web results were not opened (budget of 10 exhausted). They stay `unverified`, cap at 59 and are excluded, not judged poor. Among them: smartscope.blog, mindstudio.ai, pasqualepillitteri.it, it-connect.fr, claudekit.io, onewave-ai.com, blog.laozhang.ai, wmedia.es, four Medium posts, the dev.to post by nakadadev.
- Truncated reads: the Claude Code changelog (about 1.05 M characters) was read down to 2.1.288 (October 2, 2026) only; the 2.1.287 entry that turns mods on by default and any early-access entry were not reached, so the start date of early access is not established. The Station X guide was read except its last 3,500 characters.
- Scoring interpretations: "Updated on" (Kanaries) and "Last modified on" (Steve Kinney) dates shown on the page are used as the verified date; dev.to bylines show the day without a year ("Oct 4", "Oct 5") and are read as 2026; Station X shows only "Updated October 2026", so its date is `unverified` (freshness 5). Better Stack and Firecrawl are rated B (organization channels); company content hubs and personal course sites are rated C.
- Contradiction check: enrichment extracts date, length and author only, so secondary sources were compared with the primary sources on their titles and descriptions; no contradiction found. Two ranked videos are not in English (German, French); they are original content, not translations.

---

## Executive Summary
Anthropic announced mods for Claude Code on October 1, 2026: JavaScript or TypeScript event handlers, shipped inside plugins, that run in Claude Code's own process and can rewrite prompts, guard or answer tool calls, add commands and draw panes and bands in the interface. Within ten days the feature produced a wave of community content dominated by "N mods you need" videos and personal mod collections on GitHub, while the changelog shows the API still moving almost daily (new methods and many guard and reload fixes between 2.1.288 and 2.1.296). The recurring point of caution, stated by the official documentation itself, is that mods are not sandboxed and run with the user's full permissions, which makes the many third-party catalogues and "install these now" lists something to approach with `claude plugin validate` and a code read first.

---

## Primary sources

**Customize Claude Code with mods in TypeScript** — 🔗 https://claude.com/blog/claude-code-mods — 📅 2026-10-01
Anthropic's announcement (about 650 words): mods are introduced and "available today in the Claude Code CLI and desktop app"; a mod can target the terminal, the desktop app or both; a built-in `sec-default` mod loads first on Team and Enterprise plans and on machines with managed settings; no minimum version or plan is stated for mods themselves.

**Mods overview - Claude Code Docs** — 🔗 https://code.claude.com/docs/en/plugins/mods/overview — 📅 unverified
Reference documentation: mods are on by default, require Claude Code v2.1.287 or later in the terminal (v2.1.286 in the Desktop app's bundled copy), install as plugins from a marketplace (`/plugin install name@marketplace`), and are not sandboxed (they run with the user's permissions; `claude plugin validate` lists a mod's hooks and calls before install). Hooks run in every session type that loads the plugin, but drawing appears only in the terminal and the Desktop app's Code tab. An undated early-access period used `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS`, now ignored. Sample mods (`token-weather`, `blast-radius`, `replay-theater`) are in `anthropics/claude-code-playground`; the source of four built-in mods (`diff`, `agents-md`, `sec-default`, `telemetry`) is in `anthropics/claude-code/mods`. Sibling pages returned by the same search and not opened: Create a mod, Use the mods API, Draw in the interface, Interface gallery, Manage mods for your organization.

**Claude Code changelog - Claude Code Docs** — 🔗 https://code.claude.com/docs/en/changelog — 📅 unverified
Release notes, read from 2.1.296 (October 9, 2026) down to 2.1.288 (October 2, 2026) only: about 40 mod-related entries in eight days, including new API surface (`$.ui.notify`, `$.ui.selection()`, `prompt.autocomplete`, prompt caching in `$.model.complete`, `isDeferred` on `$.tool.register`) and many fixes on guard hooks, hot reload and the precedence of organization mods over user-installed ones. The launch entry (2.1.287) was not reached.

---

## Sources ranked by score

---

### 🔴 Essential (score 85–100)

**[1] Mods in Claude Code: change how Claude Code works**
🔗 https://www.youtube.com/watch?v=yUuFvL1lK4k
📅 2026-10-05 | ⭐ Authority: A Primary | 📊 Score: 94/100
**Summary**: The official video from the Claude channel (3:21). It presents mods as functions you write that change what Claude Code renders, what goes into a prompt and what happens on events. Short, but the vendor's own framing of the feature.
**Score reason**: Exact match + A Primary (official channel), published 6 days ago, 382k views
**Tags**: `official`, `overview`, `video`

**[2] Claude Code Mods Can Do Basically Anything...**
🔗 https://www.youtube.com/watch?v=EiThSVZ8pME
📅 2026-10-04 | ⭐ Authority: B Expert | 📊 Score: 88/100
**Summary**: Better Stack's 7:37 walkthrough, describing mods as small TypeScript plugins that run inside Claude Code to change its behavior and draw custom UI. A developer-oriented introduction from an engineering organization rather than a creator list.
**Score reason**: Exact match + B Expert (organization channel), published 7 days ago, 39k views
**Tags**: `typescript`, `introduction`, `video`

**[3] 9 NEW Claude Mods that can truly change how you work**
🔗 https://www.youtube.com/watch?v=lDrAZ1wAyVs
📅 2026-10-08 | ⭐ Authority: C Community | 📊 Score: 85/100
**Summary**: Jay E (RoboNuggets) presents nine mods in 12:47, with a companion PDF guide offered through his channel. The most viewed community video of the window on the topic.
**Score reason**: Exact match + C Community (YouTube creator), published 3 days ago, 502k views
**Tags**: `mod-selection`, `workflow`, `video`

**[4] These Mods Take Claude Code to Another Level**
🔗 https://www.youtube.com/watch?v=UcvD53jqHRU
📅 2026-10-05 | ⭐ Authority: C Community | 📊 Score: 85/100
**Summary**: Mark Kashef's 15:41 video on mods, with the mods, code and prompts offered through his links. One of the longer creator walkthroughs in the window.
**Score reason**: Exact match + C Community (YouTube creator), published 6 days ago, 39k views
**Tags**: `mod-selection`, `prompts`, `video`

**[5] Claude Mods Are Insane... You Need To Try These Right Now**
🔗 https://www.youtube.com/watch?v=ERNqRK6sMJY
📅 2026-10-09 | ⭐ Authority: C Community | 📊 Score: 85/100
**Summary**: AI LABS covers seven Claude Code mods in 13:28. Sponsored video; useful as a recent sample of which mods creators showcase.
**Score reason**: Exact match + C Community (YouTube creator), published 2 days ago, 26k views
**Tags**: `mod-selection`, `demo`, `video`

**[6] Claude Code Just Dropped Mods: Here Are 5 You Need**
🔗 https://www.youtube.com/watch?v=W5JSvXig3Ig
📅 2026-10-06 | ⭐ Authority: C Community | 📊 Score: 85/100
**Summary**: Sharbel A. presents five mods in 11:33 and links their install commands and his own mod-building prompt. Illustrates the "ask Claude to write the mod" path the documentation describes.
**Score reason**: Exact match + C Community (YouTube creator), published 5 days ago, 25k views
**Tags**: `mod-selection`, `install`, `video`

**[7] Diese 10 Claude Code Mods solltest du unbedingt kennen**
🔗 https://www.youtube.com/watch?v=ji4ANdb_M6Y
📅 2026-10-10 | ⭐ Authority: C Community | 📊 Score: 85/100
**Summary**: German-language video by Julian Ivanov (17:27) presenting ten mods, noting the feature has existed since early October. The most recent video in the ranking.
**Score reason**: Exact match + C Community (YouTube creator), published 1 day ago, 17k views
**Tags**: `mod-selection`, `german`, `video`

**[8] 3 Claude Code mods you need to build**
🔗 https://www.youtube.com/watch?v=WCwNECxFJ_Q
📅 2026-10-05 | ⭐ Authority: C Community | 📊 Score: 85/100
**Summary**: Build Great Products focuses on building three mods rather than installing existing ones (13:43), with a playbook offered through the channel's community.
**Score reason**: Exact match + C Community (YouTube creator), published 6 days ago, 13k views
**Tags**: `build`, `tutorial`, `video`

**[9] Claude Code vient de lancer les mods : voici mes 5 indispensables**
🔗 https://www.youtube.com/watch?v=1Dlh_Mqze1s
📅 2026-10-09 | ⭐ Authority: C Community | 📊 Score: 85/100
**Summary**: French-language video by Tony Lotis (13:20) presenting five mods and a skill for creating your own, distributed through his community.
**Score reason**: Exact match + C Community (YouTube creator), published 2 days ago, 12k views
**Tags**: `mod-selection`, `french`, `video`

---

### 🟠 High value (score 70–84)

**[10] Claude Code Mods: The Ultimate Customization Guide**
🔗 https://www.youtube.com/watch?v=8wZVnc99x_k
📅 2026-10-08 | ⭐ Authority: C Community | 📊 Score: 82/100
**Summary**: Eric Tech explains in 9:53 what mods are and how they change how Claude Code looks and works, "not just what it knows". An explanatory video rather than a list.
**Score reason**: Exact match + C Community (YouTube creator), published 3 days ago, 13k views
**Tags**: `customization`, `explainer`, `video`

**[11] Claude Code Mods Tutorial: Build and Test Your First Mod, Plus 15 Community Examples**
🔗 https://docs.kanaries.net/topics/AICoding/claude-code-mods
📅 2026-10-07 (updated) | ⭐ Authority: C Community | 📊 Score: 81/100
**Summary**: A hands-on tutorial of about 4,400 words by Soren Atelier (Kanaries) covering building and testing a first mod, with 15 community examples; per its search description, the author built and tested three mods on Claude Code 2.1.293. The longest verified written tutorial in the ranking.
**Score reason**: Exact match + C Community (company content hub), updated 4 days ago, about 4,400 words
**Tags**: `tutorial`, `testing`, `community-examples`

**[12] Claude Code Mods Just Turned Agents Into a Platform**
🔗 https://dev.to/max_quimby/claude-code-mods-just-turned-agents-into-a-platform-5gc0
📅 2026-10-04 | ⭐ Authority: C Community | 📊 Score: 81/100
**Summary**: An analysis post of about 2,200 words by Max Quimby arguing that mods turn Claude Code into a platform. The page states it was originally published at agentconn.com; the original URL was not retrieved, so the dev.to URL is cited.
**Score reason**: Exact match + C Community (dev.to post), published 7 days ago, about 2,200 words
**Tags**: `analysis`, `platform`, `ecosystem`

**[13] Claude Code Mods Are Game Changers. Set Up These 5 NOW.**
🔗 https://www.youtube.com/watch?v=9hetShMMp2s
📅 2026-10-02 | ⭐ Authority: C Community | 📊 Score: 80/100
**Summary**: Nate Herk's 11:19 video on five mods, published the day after the announcement. Companion repository: `nateherkai/claude-code-mods` (four mods: Cache Keeper, Recording Mode, Goal Meter, Collision Guard; scored 72, cut by the cap).
**Score reason**: Exact match + C Community (YouTube creator), published 9 days ago, 226k views
**Tags**: `mod-selection`, `setup`, `video`

**[14] Claude Mods Is The Biggest Claude Code Upgrade Since Skills**
🔗 https://www.youtube.com/watch?v=Rn4nmFRPe0s
📅 2026-10-02 | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Chase AI's 9:11 reaction and overview, published the day after the announcement, positioning mods relative to skills.
**Score reason**: Exact match + C Community (YouTube creator), published 9 days ago, 213k views
**Tags**: `overview`, `skills-comparison`, `video`

**[15] Tickloop/claude-mods**
🔗 https://github.com/Tickloop/claude-mods
📅 2026-10-08 (created) | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: A TypeScript collection of Claude Code mods, created three days before this watch and already at 77 stars.
**Score reason**: Exact match + C Community repository created 3 days ago, 77 stars
**Tags**: `repository`, `typescript`, `mod-collection`

**[16] wh000wh000/awesome-claude-mods**
🔗 https://github.com/wh000wh000/awesome-claude-mods
📅 2026-10-04 (created) | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: An index of Claude Code mods, plugins and hooks that describes itself as evidence-graded, available in 20 languages and rebuilt every 2 hours. One of several competing catalogues that appeared after the launch.
**Score reason**: Exact match + C Community repository created 7 days ago, 47 stars
**Tags**: `repository`, `catalogue`, `awesome-list`

**[17] promptadvisers/claude-mods-computer-use-threads**
🔗 https://github.com/promptadvisers/claude-mods-computer-use-threads
📅 2026-10-05 (created) | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Two mods with source, build prompts, setup and tests: a Codex computer-use bridge and coordinated Claude sessions. Same organization as `promptadvisers/claude-mods-starter-kit` (ten mods, beginner guides and a template; scored 72, cut by the cap).
**Score reason**: Exact match + C Community repository created 6 days ago, 11 stars
**Tags**: `repository`, `multi-session`, `computer-use`

**[18] Claude Code mods (AI Development Setup course)**
🔗 https://stevekinney.com/courses/ai-development-setup/claude-code-mods
📅 2026-10-06 (last modified) | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: A course page of about 1,500 words by Steve Kinney; per its search description it explains when to use a mod rather than a settings hook, a skill or a status line, the same comparison the official overview draws.
**Score reason**: Exact match + C Community (personal course site), last modified 5 days ago, about 1,500 words
**Tags**: `course`, `decision-guide`, `hooks-vs-mods`

**[19] Anthropic Launched Mods for Claude Code. Let's Build a Tiny One in TypeScript.**
🔗 https://dev.to/bobbyhalljr/anthropic-launched-mods-for-claude-code-lets-build-a-tiny-one-in-typescript-152h
📅 2026-10-05 | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: A short build-along by Bobby Hall Jr (about 900 words of prose plus code) that writes a minimal mod in TypeScript. A compact written complement to the official "Create a mod" page.
**Score reason**: Exact match + C Community (dev.to post), published 6 days ago, about 900 words
**Tags**: `tutorial`, `typescript`, `first-mod`

**[20] I Built Mods for Claude. Here's What Happened**
🔗 https://nandigamharikrishna.substack.com/p/i-built-mods-for-claude-heres-what
📅 2026-10-06 | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: A first-person account of building mods, about 1,500 words, by Hari Krishna on the "Tech in General" Substack. An experience report rather than a list or a rewrite of the announcement.
**Score reason**: Exact match + C Community (Substack post), published 5 days ago, about 1,500 words
**Tags**: `experience-report`, `build`, `substack`

---

### 🟡 Worth including (score 60–69)

No source in this band made the ranking: the cap of 20 was reached at score 77 (see Notes).

---

## Trends identified

- Creator videos dominate the first ten days: 12 of the 20 ranked sources are YouTube videos and most follow the same "N mods you need" format, often gating the mods, prompts or guides behind a creator community link. Only the official video and Better Stack come from an organization.
- The GitHub ecosystem formed within days of the announcement: 12 of the 20 repositories returned were created between October 2 and October 5, most as personal collections of a few mods (bands above the prompt, usage and context meters, tool-call guards, games). Four repositories created September 14 to 16 and a September 18 video calling mods a "hidden feature" predate the announcement, consistent with the early-access period the documentation mentions without dating it.
- Catalogues are competing rather than converging: at least three "awesome" indexes exist (`karanb192`, `wh000wh000`, `whyashthakker`), and search results show third-party guides disagreeing on the number of public mods (1,740 three days after launch versus 2,685 on October 6); neither figure comes from Anthropic.
- Security is the common caveat and the area of fastest vendor change: the official overview states mods are not sandboxed and run with the user's permissions, community posts repeat it, and most mod-related changelog entries from 2.1.289 to 2.1.296 fix guard, approval or organization-precedence behavior. Anything written in the first week may already describe outdated behavior.
- "Build by asking" is the prevailing authoring model: the documentation's first suggestion is to describe the mod and let Claude write it (built-in `plugin-authoring` skill), and several creators distribute a mod-building prompt or skill rather than code.

---

*Generated by tech-watch skill | Sources used: GitHub · YouTube · Web (Tier 2) · Owner domains*
*Scoring: Relevance 40% · Freshness 20% · Authority 20% · Depth 10% · Engagement 10%*
