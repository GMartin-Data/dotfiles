# Tech Watch — Claude Code mods
**Date**: 2026-10-10 | **Window**: 30 days | **Sources**: 20

**Pipeline counts**: 63 raw results (arXiv 0, GitHub 20, YouTube 15, web 28) | 53 on-topic (51 unique after deduplication), 2 adjacent, 1 off-topic, 7 dropped unlabeled (1 video under 3 min, 6 web results without a usable title) | Tier 3 not run (unique on-topic >= 12) | Pages opened: 10/10 of the WebFetch budget, 0 failures

**Selection note**: 40 results reached the 60/100 threshold; the 20 highest scores are kept (ties among repositories broken by stars). Scored but cut by the cap: 10 on-topic repositories (89, 84, 74), three opened articles at 85 (Kanaries tutorial, StationX guide, Max Quimby on dev.to), four opened articles at 68-79, one video at 74, two adjacent repositories at 69. Web results that were not opened have an `unverified` date and length and cannot reach 60.

---

## Executive Summary
Mods are a new Claude Code extension mechanism, announced by Anthropic on 2026-10-01: JavaScript or TypeScript event handlers shipped inside plugins, running in-process, able to rewrite prompts and tool calls and to draw or replace parts of the interface. The watch window captures the launch wave almost exclusively: the community response is massive but shallow (dozens of "N mods you need" videos and mod collections created within nine days), while the official documentation carries the substance, in particular the security model (mods are not sandboxed and run with the user's permissions). The unexpected finding is how fast the surface is still moving: the changelog shows mod-related additions and guard-bypass fixes in almost every release from 2.1.288 to 2.1.296 (October 2 to 9).

---

## Primary sources

**Mods overview - Claude Code Docs** — 🔗 https://code.claude.com/docs/en/plugins/mods/overview — 📅 unverified
Establishes the reference facts: mods are on by default; terminal requires Claude Code v2.1.287 or later, the Desktop app works from v2.1.286; hooks run in most session types but drawing only appears in the terminal and the Desktop Code tab (not in the VS Code chat panel, `claude -p`, cloud sessions; nothing runs in Desktop WSL sessions); mods are not sandboxed; `claude plugin validate` lists a mod's hooks and calls before install; sample mods (`token-weather`, `blast-radius`, `replay-theater`) live in `anthropics/claude-code-playground`; the early-access variable `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS` is ignored from v2.1.287.

**Customize Claude Code with mods in TypeScript (Anthropic announcement)** — 🔗 https://claude.com/blog/claude-code-mods — 📅 2026-10-01
Establishes the launch date and scope: available in the Claude Code CLI and desktop app, distributed through plugins (`/plugin` or the Claude directory); the built-in `sec-default` mod loads first on Team and Enterprise plans and on machines with managed settings; `/diff` is now itself a mod. The post states no minimum version and does not say beta or GA.

**Claude Code changelog** — 🔗 https://code.claude.com/docs/en/changelog — 📅 latest entry read: 2.1.296, 2026-10-09
Establishes the release cadence after launch: mod-related entries in 2.1.288 (Oct 2), 2.1.289 (Oct 3), 2.1.290 (Oct 5), 2.1.292 (Oct 6), 2.1.293 (Oct 7), 2.1.295 (Oct 8) and 2.1.296 (Oct 9), including new API (`$.ui.notify`, `prompt.autocomplete`, `$.ui.selection()`) and fixes where a user-installed mod could bypass an organization's guard or a deny rule. Only the first part of the page was read; the 2.1.287 entry itself was not reached.

Also returned by the owner-domain search, not opened: Create a mod (https://code.claude.com/docs/en/plugins/mods/create), Use the mods API (https://code.claude.com/docs/en/plugins/mods/api), Manage mods for your organization (https://code.claude.com/docs/en/plugins/mods/admin), Draw in the interface with a mod (https://code.claude.com/docs/en/plugins/mods/interface).

---

## Sources ranked by score

Conventions used: GitHub freshness is scored on the last push date; repository depth is scored 4 (length not established, repositories are not opened); authority High = Tier 1 tool source. Video and repository summaries rely on the title and description returned by the tools only.

---

### 🔴 Essential (score 85–100)

**[1] 9 NEW Claude Mods that can truly change how you work**
🔗 https://www.youtube.com/watch?v=lDrAZ1wAyVs
📅 2026-10-08 | ⭐ Authority: High | 📊 Score: 100/100
**Summary**: Walkthrough of nine mods by Jay E (RoboNuggets), 12:47, with a companion PDF guide. The most viewed video of the window (428,120 views), so a good marker of what the general audience retains from the launch.
**Score reason**: Direct match on query + published 2 days ago with 428k views
**Tags**: `youtube`, `mod-roundup`, `workflow`

**[2] Claude Code Mods Can Do Basically Anything...**
🔗 https://www.youtube.com/watch?v=EiThSVZ8pME
📅 2026-10-04 | ⭐ Authority: High | 📊 Score: 100/100
**Summary**: Better Stack presents mods as small TypeScript plugins running inside Claude Code that change its behavior and draw custom UI (7:37). One of the few videos whose description is technical rather than a list of picks.
**Score reason**: Direct match on query + 38.9k views within 6 days
**Tags**: `youtube`, `typescript`, `explainer`

**[3] These Mods Take Claude Code to Another Level**
🔗 https://www.youtube.com/watch?v=UcvD53jqHRU
📅 2026-10-05 | ⭐ Authority: High | 📊 Score: 100/100
**Summary**: Mark Kashef demonstrates a set of mods and distributes the mods, code and prompts used (15:41, the longest video of the set). Useful for reusable material rather than concepts.
**Score reason**: Direct match on query + 38.3k views within 5 days
**Tags**: `youtube`, `demo`, `prompts`

**[4] Claude Code Just Dropped Mods: Here Are 5 You Need**
🔗 https://www.youtube.com/watch?v=W5JSvXig3Ig
📅 2026-10-06 | ⭐ Authority: High | 📊 Score: 100/100
**Summary**: Sharbel A. presents five mods with their install commands and a custom mod-building prompt (11:33). Representative of the "build it by asking Claude" approach.
**Score reason**: Direct match on query + 24.9k views within 4 days
**Tags**: `youtube`, `mod-roundup`, `install`

**[5] Claude Mods Are Insane... You Need To Try These Right Now**
🔗 https://www.youtube.com/watch?v=ERNqRK6sMJY
📅 2026-10-09 | ⭐ Authority: High | 📊 Score: 100/100
**Summary**: AI LABS reviews seven Claude Code mods (13:28). Sponsored video; the most recent English-language roundup of the window.
**Score reason**: Direct match on query + published yesterday with 18.5k views
**Tags**: `youtube`, `mod-roundup`, `sponsored`

**[6] 3 Claude Code mods you need to build**
🔗 https://www.youtube.com/watch?v=WCwNECxFJ_Q
📅 2026-10-05 | ⭐ Authority: High | 📊 Score: 100/100
**Summary**: Build Great Products focuses on building three mods rather than installing existing ones (13:43), with a companion playbook. Complements the install-oriented roundups.
**Score reason**: Direct match on query + 13k views within 5 days
**Tags**: `youtube`, `build-your-own`, `tutorial`

**[7] Claude Code Mods: The Ultimate Customization Guide**
🔗 https://www.youtube.com/watch?v=8wZVnc99x_k
📅 2026-10-08 | ⭐ Authority: High | 📊 Score: 100/100
**Summary**: Eric Tech explains what mods are and how they change the look and behavior of Claude Code, "not just what it knows" (9:53). Positioned as a guide rather than a list.
**Score reason**: Direct match on query + published 2 days ago with 11.6k views
**Tags**: `youtube`, `guide`, `customization`

**[8] Claude Code Mods Are Game Changers. Set Up These 5 NOW.**
🔗 https://www.youtube.com/watch?v=9hetShMMp2s
📅 2026-10-02 | ⭐ Authority: High | 📊 Score: 95/100
**Summary**: Nate Herk sets up five mods the day after the announcement (11:19, 221,897 views). His four published mods (Cache Keeper, Recording Mode, Goal Meter, Collision Guard) are in the repository `nateherkai/claude-code-mods`.
**Score reason**: Direct match on query + 222k views, published 8 days ago
**Tags**: `youtube`, `mod-roundup`, `launch-week`

**[9] Claude Mods Is The Biggest Claude Code Upgrade Since Skills**
🔗 https://www.youtube.com/watch?v=Rn4nmFRPe0s
📅 2026-10-02 | ⭐ Authority: High | 📊 Score: 95/100
**Summary**: Chase AI frames mods as the largest Claude Code change since skills (9:11, 212,411 views). Opinion-led positioning piece from launch week.
**Score reason**: Direct match on query + 212k views, published 8 days ago
**Tags**: `youtube`, `positioning`, `launch-week`

**[10] Claude Mods Just Dropped... Use these 3 NOW**
🔗 https://www.youtube.com/watch?v=moOBIaIb4a8
📅 2026-10-02 | ⭐ Authority: High | 📊 Score: 95/100
**Summary**: Jack Roberts presents three mods and a prompt to find which mods fit a given workflow (9:00). Early launch-week coverage.
**Score reason**: Direct match on query + 41.4k views, published 8 days ago
**Tags**: `youtube`, `mod-roundup`, `launch-week`

**[11] Claude Code vient de lancer les mods : voici mes 5 indispensables**
🔗 https://www.youtube.com/watch?v=1Dlh_Mqze1s
📅 2026-10-09 | ⭐ Authority: High | 📊 Score: 95/100
**Summary**: French-language roundup by Tony Lotis of five mods plus a skill to create one's own (13:20). The only French-language source returned by the tools.
**Score reason**: Direct match on query + published yesterday, 7.6k views
**Tags**: `youtube`, `french`, `mod-roundup`

**[12] Claude Code Mods Are INSANE (Master it in 9 minutes)**
🔗 https://www.youtube.com/watch?v=oL6yb21XhDQ
📅 2026-10-08 | ⭐ Authority: High | 📊 Score: 95/100
**Summary**: Short overview by Shab Noor aimed at operators (8:59). Low audience (359 views); kept on the grid's criteria, with little independent signal behind it.
**Score reason**: Direct match on query + published 2 days ago
**Tags**: `youtube`, `overview`, `low-audience`

**[13] Mods in Claude Code: change how Claude Code works**
🔗 https://www.youtube.com/watch?v=yUuFvL1lK4k
📅 2026-10-05 | ⭐ Authority: High | 📊 Score: 94/100
**Summary**: Video from the channel named "Claude" (official status of the channel not verified by the tool output) describing mods as functions that change what Claude Code renders, what goes into a prompt and what tools do (3:21, 371,436 views). The shortest and closest-to-source video of the set.
**Score reason**: Direct match on query + 371k views within 5 days (short format lowers depth)
**Tags**: `youtube`, `announcement`, `overview`

**[14] karanb192/awesome-claude-code-mods**
🔗 https://github.com/karanb192/awesome-claude-code-mods
📅 created 2026-09-15, last push 2026-10-10 | ⭐ Authority: High | 📊 Score: 89/100
**Summary**: Community catalogue of public mods scanned from GitHub, listing for each mod what it can read, write, run or send over the network (455 stars, the most starred repository of the window). Directly addresses the trust question raised by the official docs.
**Score reason**: Exact catalogue of the topic + pushed today, 455 stars
**Tags**: `github`, `catalogue`, `security-review`

**[15] hamzafer/claude-code-mods**
🔗 https://github.com/hamzafer/claude-code-mods
📅 created 2026-10-02, last push 2026-10-09 | ⭐ Authority: High | 📊 Score: 89/100
**Summary**: Collection of mods adding live lines above the prompt, guards, panes and games: context bar, usage meter, Codex review watch, Markdown preview, Spotify now playing (177 stars, TypeScript). A broad sample of what the drawing API is used for.
**Score reason**: Exact implementation of the topic + pushed yesterday, 177 stars
**Tags**: `github`, `mod-collection`, `typescript`

**[16] Tickloop/claude-mods**
🔗 https://github.com/Tickloop/claude-mods
📅 created 2026-10-08, last push 2026-10-08 | ⭐ Authority: High | 📊 Score: 89/100
**Summary**: A collection of Claude Code mods in TypeScript (77 stars two days after creation). The description gives no detail on the individual mods.
**Score reason**: Exact implementation of the topic + pushed 2 days ago
**Tags**: `github`, `mod-collection`, `typescript`

**[17] darrell-tw/darrelltw-mods**
🔗 https://github.com/darrell-tw/darrelltw-mods
📅 created 2026-09-16, last push 2026-10-05 | ⭐ Authority: High | 📊 Score: 89/100
**Summary**: Mods by Darrell Wang drawing bands above the prompt with zero model tokens, starting with Taiwan and US stock tickers (65 stars). Created two weeks before the public launch, so built during early access.
**Score reason**: Exact implementation of the topic + pushed 5 days ago
**Tags**: `github`, `prompt-band`, `early-access`

**[18] whyashthakker/awesome-claude-code-mods**
🔗 https://github.com/whyashthakker/awesome-claude-code-mods
📅 created 2026-10-03, last push 2026-10-03 | ⭐ Authority: High | 📊 Score: 89/100
**Summary**: Collection announcing 100+ mods usable with Claude Code (43 stars). A second, independent list alongside the karanb192 catalogue; the count is the author's claim.
**Score reason**: Exact collection of the topic + pushed 7 days ago
**Tags**: `github`, `awesome-list`, `mod-collection`

**[19] zycck/claude-mods**
🔗 https://github.com/zycck/claude-mods
📅 created 2026-10-02, last push 2026-10-08 | ⭐ Authority: High | 📊 Score: 89/100
**Summary**: Mods showing live plan progress bars above the prompt (42 stars, TypeScript). A single-purpose example of the "band above the prompt" pattern.
**Score reason**: Exact implementation of the topic + pushed 2 days ago
**Tags**: `github`, `prompt-band`, `progress`

**[20] karanb192/claude-code-mods**
🔗 https://github.com/karanb192/claude-code-mods
📅 created 2026-09-15, last push 2026-10-03 | ⭐ Authority: High | 📊 Score: 89/100
**Summary**: Mods and the tooling to build them, starting with a builder skill (40 stars). Tagged `function-hooks`, the name the feature carried during early access.
**Score reason**: Exact implementation of the topic + pushed 7 days ago
**Tags**: `github`, `builder-skill`, `function-hooks`

---

### 🟠 High value (score 70–84)

None kept: every result in this band was cut by the 20-source cap (see the selection note in the header).

---

### 🟡 Worth including (score 60–69)

None kept: the total already reaches 20.

---

## Trends identified

- **A launch-week wave, not a mature ecosystem**: 13 of the 14 videos kept by the relevance filter were published between October 2 and 9, and 13 of the 17 on-topic repositories were created on or after October 2. No arXiv paper mentions the topic.
- **Early access preceded the announcement**: several repositories date from September 14 to 16 and a September 18 video calls mods a "hidden feature"; the official docs confirm an early-access flag (`CLAUDE_CODE_ENABLE_FUNCTION_HOOKS`) that v2.1.287 now ignores.
- **The band above the prompt is the dominant use case**: context, usage, cache and plan-progress meters recur across independent repositories and match Anthropic's own `token-weather` sample; guards on tool calls come second.
- **Security is the main reservation, and tooling is forming around it**: the docs state that mods are not sandboxed and that the `sec-default` guard only loads on Team and Enterprise plans or managed machines; community catalogues respond by listing what each mod can read, write, run or send, and the changelog fixed several guard-bypass cases within the first nine days.
- **The API is still changing daily**: seven releases between October 2 and 9 carry mod-related additions or fixes, so tutorials and collections from launch week may already be out of date; check any version or behavior claim against the docs.
- **Fact drift in secondary coverage**: among the opened articles cut by the cap, one (Bobby Hall Jr, dev.to) dates the launch to October 3, which contradicts the Anthropic announcement dated October 1; the others agree with the primary sources on version and availability.

---

*Generated by tech-watch skill | Sources: arXiv · GitHub · YouTube · Web search*
*Scoring: Relevance 40% · Freshness 20% · Authority 20% · Depth 10% · Engagement 10%*
