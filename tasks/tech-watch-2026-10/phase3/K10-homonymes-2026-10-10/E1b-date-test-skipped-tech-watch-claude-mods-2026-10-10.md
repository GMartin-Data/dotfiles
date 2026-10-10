# Tech Watch — Claude Mods
**Date**: 2026-10-10 | **Window**: 30 days | **Sources**: 20

**Topic normalized to**: Claude Code mods (owner: Anthropic)
**Pipeline counts**: 63 raw results (arXiv 0, GitHub 20, YouTube 15, web Tier 2 28) → 53 on-topic, 1 adjacent, 5 homonyms, 4 dropped unlabeled (2 videos under 3 min, 2 results without a usable title) → 48 unique on-topic after deduplication. Tier 3 not run (48 ≥ 12).
**Enrichment**: 10 / 10 pages opened (3 primary, 7 web candidates), 0 failures. Two pages were read truncated (changelog, StationX guide).
**Coverage note**: 38 sources reach the 60 threshold; the cap of 20 applies. The 18 not listed are 2 dev.to posts (77), 15 community repositories (62–77) and one anonymous blog post (73). Ten web results that were not opened stay at 59 at most (date, length `unverified`) and are excluded.
**Date test**: skipped. The official overview mentions an early-access period (`CLAUDE_CODE_ENABLE_FUNCTION_HOOKS`) without dating it, so homonyms were judged on the meaning test alone.

---

## Executive Summary
Anthropic launched mods for Claude Code on 2026-10-01: JavaScript or TypeScript event handlers, shipped inside plugins, that run inside the Claude Code process and can draw panes and bands, redraw built-in interface parts, intercept tool calls and add commands. Within ten days the ecosystem response is large and almost entirely community-driven: dozens of "N mods you need" videos, mod collections and at least three competing catalogues, while the changelog shows near-daily additions to the mods API. The unexpected finding is how central security is on both sides: the official docs state plainly that mods are not sandboxed and run with the user's full permissions, and several community projects exist only to audit what a mod can read, write, run or send.

---

## Primary sources

**Mods overview - Claude Code Docs** — 🔗 https://code.claude.com/docs/en/plugins/mods/overview — 📅 unverified
Establishes the definition (a plugin made of JS/TS event handlers called hooks), the requirements (on by default; terminal v2.1.287 or later, Desktop app from v2.1.286), where mods run (hooks run in every session type that loads the plugin; drawing only in the terminal and the Desktop app Code tab, not in the VS Code chat panel, `claude -p` or cloud sessions), the trust model (not sandboxed, run with the user's permissions, `claude plugin validate` lists hooks and calls before install), the built-in mods (`cc-plugin-diff`, `cc-plugin-agents-md`, `cc-plugin-sec-default`, ...) and the existence of an undated early-access period.

**Customize Claude Code with mods in TypeScript** — 🔗 https://claude.com/resources/articles/claude-code-mods — 📅 2026-10-01
Anthropic's launch post ("Today we're introducing mods"): available in the Claude Code CLI and the desktop app, distributed inside plugins, no plan required to use mods; Team and Enterprise plans are tied only to admin controls and the built-in `sec-default` guard.

**Claude Code changelog** — 🔗 https://code.claude.com/docs/en/changelog — 📅 rolling page, latest entry read: 2.1.296 (2026-10-09)
Shows the mods API changing almost every day since launch: 2.1.288 (Oct 2, `$.ui.selection()`), 2.1.290 (Oct 5, `serverToolUses` on `turn.step`), 2.1.292 (Oct 6, prompt caching in `$.model.complete`, workflow agents in `agent.spawn`), 2.1.293 (Oct 7, `isDeferred` in `$.tool.register`), 2.1.295 (Oct 8, `$.ui.notify`, `Button` children), 2.1.296 (Oct 9, fixes). The page was truncated before the 2.1.287 entry, so the launch entry itself and any earlier mention were not read.

Related official pages found but not opened: [Create a mod](https://code.claude.com/docs/en/plugins/mods/create), [Use the mods API](https://code.claude.com/docs/en/plugins/mods/api), [Draw in the interface with a mod](https://code.claude.com/docs/en/plugins/mods/interface), [Manage mods for your organization](https://code.claude.com/docs/en/plugins/mods/admin).

---

## Sources ranked by score

---

### 🔴 Essential (score 85–100)

**[1] Mods in Claude Code: change how Claude Code works**
🔗 https://www.youtube.com/watch?v=yUuFvL1lK4k
📅 2026-10-05 | ⭐ Authority: A Primary | 📊 Score: 94/100
**Summary**: Official video from the Claude channel (3:21) presenting mods as functions you write that change what Claude Code renders, what goes into a prompt and more. The shortest authoritative introduction to the feature, and the reference against which the creator videos can be compared.
**Score reason**: Exact match + A Primary (official channel), published 5 days ago, 371,756 views
**Tags**: `official`, `announcement`, `overview`

**[2] 9 NEW Claude Mods that can truly change how you work**
🔗 https://www.youtube.com/watch?v=lDrAZ1wAyVs
📅 2026-10-08 | ⭐ Authority: C Community | 📊 Score: 85/100
**Summary**: Walkthrough of nine mods by Jay E (RoboNuggets), 12:47, with a companion PDF guide. The most viewed video of the watch, useful as a picture of which mods the mainstream audience is being pointed to.
**Score reason**: Exact match + C Community (YouTube creator), published 2 days ago, 430,694 views
**Tags**: `mod-selection`, `walkthrough`, `video`

**[3] Claude Code Just Dropped MODS. (Master it in 10 Minutes).**
🔗 https://www.youtube.com/watch?v=LDn7rQKIFro
📅 2026-10-05 | ⭐ Authority: C Community | 📊 Score: 85/100
**Summary**: Ten-minute introduction by Tristen O'Brien, with the prompts used offered as a download. The description carries affiliate links unrelated to mods.
**Score reason**: Exact match + C Community (YouTube creator), published 5 days ago, 202,541 views
**Tags**: `introduction`, `prompts`, `video`

**[4] These Mods Take Claude Code to Another Level**
🔗 https://www.youtube.com/watch?v=UcvD53jqHRU
📅 2026-10-05 | ⭐ Authority: C Community | 📊 Score: 85/100
**Summary**: Mark Kashef's 15:41 video, the longest creator video of the watch, distributed with free mods, code and prompts. One of the few that ships source rather than only a demo.
**Score reason**: Exact match + C Community (YouTube creator), published 5 days ago, 38,292 views
**Tags**: `mod-building`, `source-code`, `video`

**[5] Claude Code Just Dropped Mods: Here Are 5 You Need**
🔗 https://www.youtube.com/watch?v=W5JSvXig3Ig
📅 2026-10-06 | ⭐ Authority: C Community | 📊 Score: 85/100
**Summary**: Sharbel A. presents five mods (11:33) with their install commands and a custom mod-building prompt. Representative of the "build mods by prompting Claude" pattern the official docs encourage.
**Score reason**: Exact match + C Community (YouTube creator), published 4 days ago, 24,901 views
**Tags**: `mod-selection`, `install`, `video`

**[6] Claude Mods Are Insane... You Need To Try These Right Now**
🔗 https://www.youtube.com/watch?v=ERNqRK6sMJY
📅 2026-10-09 | ⭐ Authority: C Community | 📊 Score: 85/100
**Summary**: AI LABS shows seven Claude Code mods in 13:28. The most recent of the high-audience selections; sponsored segment in the description.
**Score reason**: Exact match + C Community (YouTube creator), published 1 day ago, 18,873 views
**Tags**: `mod-selection`, `demo`, `video`

---

### 🟠 High value (score 70–84)

**[7] Claude Code Mods Can Do Basically Anything...**
🔗 https://www.youtube.com/watch?v=EiThSVZ8pME
📅 2026-10-04 | ⭐ Authority: C Community | 📊 Score: 82/100
**Summary**: Better Stack describes mods as small TypeScript plugins running inside Claude Code that change its behaviour and draw custom interface (7:37). A developer-oriented take rather than a list of picks. A 1:29 Short from the same channel was dropped.
**Score reason**: Exact match + C Community (YouTube channel), published 6 days ago, 38,882 views
**Tags**: `typescript`, `developer`, `video`

**[8] Claude Code Mods: The Ultimate Customization Guide**
🔗 https://www.youtube.com/watch?v=8wZVnc99x_k
📅 2026-10-08 | ⭐ Authority: C Community | 📊 Score: 82/100
**Summary**: Eric Tech explains what mods are and how they change the way Claude Code looks and works, not only what it knows (9:53). Positions mods against skills and other customization layers.
**Score reason**: Exact match + C Community (YouTube creator), published 2 days ago, 11,628 views
**Tags**: `customization`, `guide`, `video`

**[9] Claude Code Mods: The Complete Guide + 34 Videos (2026)**
🔗 https://app.stationx.net/articles/claude-code-mods
📅 October 2026 (day unverified) | ⭐ Authority: B Expert | 📊 Score: 82/100
**Summary**: Very long guide (about 9,500 words) by Nathan House, founder of the security training company StationX, with a security angle: it stresses that Anthropic's guard only loads on Team/Enterprise plans or managed machines. Its version and date claims (on by default since v2.1.287, 1 Oct 2026; terminal and desktop Code tab) match the primary sources.
**Score reason**: Exact match + B Expert (identified security organization), over 1,500 words, updated October 2026
**Tags**: `security`, `guide`, `long-form`

**[10] Claude Code Mods: What They Are and How to Write One**
🔗 https://www.developersdigest.tech/blog/claude-code-mods-guide-2026
📅 2026-10-06 | ⭐ Authority: C Community | 📊 Score: 81/100
**Summary**: Condensed walkthrough (about 1,800 words, no byline) of the three-file mod structure and the tool-call counter example, including loading a mod for one session with `claude --plugin-dir`. Version requirements match the official overview (v2.1.287 terminal, v2.1.286 Desktop).
**Score reason**: Exact match + C Community (developer blog), published 4 days ago, over 1,500 words
**Tags**: `tutorial`, `first-mod`, `plugin-dir`

**[11] Claude Code Mods Tutorial: Build and Test Your First Mod, Plus 15 Community Examples**
🔗 https://docs.kanaries.net/topics/AICoding/claude-code-mods
📅 2026-10-07 (update date; original publication date not shown) | ⭐ Authority: C Community | 📊 Score: 81/100
**Summary**: About 4,000 words by Soren Atelier on the Kanaries site: build, test and install a first mod, then 15 community examples. States that mods shipped in Claude Code 2.1.287 on October 1, 2026 and are on by default, consistent with the primary sources. A German translation of the same page was deduplicated.
**Score reason**: Exact match + C Community (vendor topic page), updated 3 days ago, over 1,500 words
**Tags**: `tutorial`, `testing`, `community-examples`

**[12] Claude Code Mods Just Turned Agents Into a Platform**
🔗 https://dev.to/max_quimby/claude-code-mods-just-turned-agents-into-a-platform-5gc0
📅 2026-10-04 (year not shown on the page header; comments dated October 2026) | ⭐ Authority: C Community | 📊 Score: 81/100
**Summary**: Opinion and analysis piece (about 2,300 words) by Max Quimby, originally published at AgentConn, arguing that mods plus plugin marketplaces turn Claude Code into a platform. Its launch claim (v2.1.287 on October 1, 2026) matches the primary sources.
**Score reason**: Exact match + C Community (dev.to post), published 6 days ago, over 1,500 words
**Tags**: `analysis`, `platform`, `marketplaces`

**[13] Claude Code Mods Are Game Changers. Set Up These 5 NOW.**
🔗 https://www.youtube.com/watch?v=9hetShMMp2s
📅 2026-10-02 | ⭐ Authority: C Community | 📊 Score: 80/100
**Summary**: Nate Herk's five-mod setup (11:19), one of the first high-audience videos after launch. Companion repository: https://github.com/nateherkai/claude-code-mods (four mods: Cache Keeper, Recording Mode, Goal Meter, Collision Guard; 17 stars, score 72, beyond the cap). A 1:22 Short from the same channel was dropped.
**Score reason**: Exact match + C Community (YouTube creator), published 8 days ago, 222,024 views
**Tags**: `mod-selection`, `setup`, `video`

**[14] Claude Code vient de lancer les mods : voici mes 5 indispensables**
🔗 https://www.youtube.com/watch?v=1Dlh_Mqze1s
📅 2026-10-09 | ⭐ Authority: C Community | 📊 Score: 80/100
**Summary**: French-language video by Tony Lotis (13:20) presenting five mods and a skill for creating your own. The only French-language source of the watch.
**Score reason**: Exact match + C Community (YouTube creator), published 1 day ago, 7,844 views
**Tags**: `french`, `mod-selection`, `video`

**[15] Claude Mods Is The Biggest Claude Code Upgrade Since Skills**
🔗 https://www.youtube.com/watch?v=Rn4nmFRPe0s
📅 2026-10-02 | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Chase AI frames mods as the largest Claude Code change since skills (9:11). Published the day after launch; useful for the positioning of mods against skills.
**Score reason**: Exact match + C Community (YouTube creator), published 8 days ago, 212,429 views
**Tags**: `positioning`, `skills`, `video`

**[16] Claude Mods Just Dropped... Use these 3 NOW**
🔗 https://www.youtube.com/watch?v=moOBIaIb4a8
📅 2026-10-02 | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Jack Roberts presents three mods (9:00) and a free prompt to find mods suited to one's workflow. Early launch-week reaction.
**Score reason**: Exact match + C Community (YouTube creator), published 8 days ago, 41,372 views
**Tags**: `mod-selection`, `prompts`, `video`

**[17] Tickloop/claude-mods**
🔗 https://github.com/Tickloop/claude-mods
📅 2026-10-08 (created) | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: A TypeScript collection of Claude Code mods, created two days before this watch and already at 77 stars. The description gives no detail on the individual mods.
**Score reason**: Exact match + C Community repository created 2 days ago, 77 stars
**Tags**: `repository`, `collection`, `typescript`

**[18] whyashthakker/awesome-claude-code-mods**
🔗 https://github.com/whyashthakker/awesome-claude-code-mods
📅 2026-10-03 (created) | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Collection announced as 100+ mods usable with Claude Code. One of three competing "awesome" lists found in the window.
**Score reason**: Exact match + C Community repository created 7 days ago, 43 stars
**Tags**: `repository`, `awesome-list`, `catalogue`

**[19] wh000wh000/awesome-claude-mods**
🔗 https://github.com/wh000wh000/awesome-claude-mods
📅 2026-10-04 (created) | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Self-described evidence-graded index of Claude Code mods, plugins and hooks, in 20 languages and rebuilt every 2 hours. An automated catalogue, in contrast with hand-curated lists.
**Score reason**: Exact match + C Community repository created 6 days ago, 39 stars
**Tags**: `repository`, `index`, `automation`

**[20] aieo-product/claude_qamods**
🔗 https://github.com/aieo-product/claude_qamods
📅 2026-10-04 (created) | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Mods that make Claude's questions easier to read and answer (topic `askuserquestion`): an example of redrawing a built-in interface part rather than adding a band. Tied at 77 points and 11 stars with promptadvisers/claude-mods-computer-use-threads for the last slot.
**Score reason**: Exact match + C Community repository created 6 days ago, 11 stars
**Tags**: `repository`, `ui-redraw`, `askuserquestion`

---

### 🟡 Worth including (score 60–69)

None within the cap of 20. Sources that reach 60 but fall beyond the cap:

- 77 — [Anthropic Launched Mods for Claude Code. Let's Build a Tiny One in TypeScript.](https://dev.to/bobbyhalljr/anthropic-launched-mods-for-claude-code-lets-build-a-tiny-one-in-typescript-152h) (dev.to, Bobby Hall Jr, Oct 5). ⚠️ Contradicts the launch post (claude.com, 2026-10-01): the article says "On October 3, 2026, Anthropic introduced Mods for Claude Code". The date is not its title or main point, so it is kept and flagged.
- 77 — [What are Claude Code mods? What they can draw and where they run in the desktop app](https://dev.to/nakadadev/what-are-claude-code-mods-what-they-can-draw-and-where-they-run-in-the-desktop-app-58pc) (dev.to, Haruki Nakada, Oct 6; tested on 2.1.286 to 2.1.288, Windows 11; consistent with the official overview).
- 77 — repositories: promptadvisers/claude-mods-computer-use-threads, AgriciDaniel/claude-mods-brain, ersinkoc/claude-mods.
- 75 — video: "Claude Code Mods Are INSANE (Master it in 9 minutes)" (Shab Noor, 359 views).
- 74 — hamzafer/claude-code-mods (177 stars).
- 73 — [claude code mods hook extensions 2026](https://braindetox.kr/en/posts/claude_code_mods_hook_extensions_2026.html) (Oct 5, no named author, authority `unverified`). It presents itself as based on a tutorial by Addy Osmani on claude.dev; that attribution could not be checked against any opened primary source.
- 72 — repositories: zycck/claude-mods, promptadvisers/claude-mods-starter-kit, nateherkai/claude-code-mods, augiefra/claude-mods, OneWave-AI/claude-code-mods.
- 64 — karanb192/awesome-claude-code-mods (456 stars, created 2026-09-15, catalogue listing what each mod can read, write, run or send over the network), JohnnyVizz/claude-kit (partial: skills and mods).
- 62 — karanb192/claude-code-mods, darrell-tw/darrelltw-mods, galElmalah/claude-mods (all created 2026-09-14 to 09-16).

---

## Adjacent, not ranked

- escapeboy/claude-code-kit — https://github.com/escapeboy/claude-code-kit — general Claude Code kit created 2026-01-04 (skills, subagents, hooks, slash commands, guides) in which mods are one component among six.

---

## Trends identified

- **Launch-week saturation by creators, thin on primary detail.** 13 of the 15 videos returned are creator selections of the form "N mods you need", published between Oct 2 and Oct 9; only the 3-minute official video and a handful of written tutorials explain the mechanism (hooks module, `tool.call` and `ui.render` events).
- **Most community mods draw a band above the prompt.** Repository descriptions converge on the same use cases: context and usage meters, rate-limit and cache countdowns, plan progress bars, now-playing or stock tickers. Tool-call guards and interface redraws are a clear minority.
- **Security is the main structural concern.** The official docs state that mods are not sandboxed, run with the user's permissions and can approve tool calls; the built-in `sec-default` guard is tied to Team/Enterprise plans or managed settings. Community answers are catalogues that scan what each mod can read, write, run or send, and a knowledge base on how to check a mod before installing it.
- **Catalogues are already competing.** At least three "awesome" lists or indexes appeared within three weeks (one hand-curated with capability scans, one claiming 100+ mods, one rebuilt automatically every 2 hours), a sign that discovery, not creation, is the bottleneck since mods can be built by prompting Claude.
- **The API is still moving, and repositories predate the public launch.** The changelog shows mods API additions in almost every release from 2.1.288 to 2.1.296, and several repositories were created on Sept 14–16, two weeks before the Oct 1 launch post, consistent with the undated early-access period the docs mention. Tutorials pinned to launch-week behaviour may age quickly.

---

*Generated by tech-watch skill | Sources: arXiv · GitHub · YouTube · Web search*
*Scoring: Relevance 40% · Freshness 20% · Authority 20% · Depth 10% · Engagement 10%*
