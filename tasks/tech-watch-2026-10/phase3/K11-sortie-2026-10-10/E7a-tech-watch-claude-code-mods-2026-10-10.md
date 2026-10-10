# Tech Watch — mods de Claude Code
**Date**: 2026-10-10 | **Window**: 30 days | **Topic**: Claude Code mods (owner: Anthropic) | **Sources**: 20 ranked + 3 primary

| Source | Status | Raw | On-topic | In report |
|---|---|---|---|---|
| arXiv | empty | 0 | 0 | 0 |
| GitHub | ok | 20 | 19 | 6 |
| YouTube | ok | 15 | 14 | 11 |
| Web (Tier 2) | ok | 28 | 28 | 3 |
| Web (Tier 3) | not run (unique on-topic ≥ 12) | – | – | 0 |
| Owner domains | ok | 10 | – | 3 |

**Pipeline**: 63 raw → 61 on-topic, 0 adjacent, 1 homonyms, 1 dropped → 56 unique → 39 ≥ 60 → 20 ranked (cap 20).
**Enrichment**: 10/10 pages opened (3 primary), 0 failures, 2 truncated.
**Date test**: skipped (the docs overview mentions an early-access period, flag `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS`, without dating it; the changelog read was truncated before the 2.1.287 entry).
**Notes**:
- Cap cut: 39 sources reached 60, 19 were cut. The last slot was a tie at 77 points and 9 stars between `AgriciDaniel/claude-mods-brain` and `ersinkoc/claude-mods`; the grid has no further tie-break, the GitHub best-match order was used. Web pages have no engagement number and lose every tie against a repository or a video.
- Two opened pages scored 77 and were cut by the cap, both with a contradiction flag: the dev.to post by Bobby Hall Jr. dates the launch "October 3, 2026" (announcement: October 1), and the Substack post by Hari Krishna says a mod's code "runs in a sealed little room" (docs: "Mods aren't sandboxed").
- Unopened pages: 16 unique Tier 2 pages were not opened (budget spent). With date and length `unverified` they reach at most 59 and are excluded; this is a budget effect, not a quality judgment.
- Truncated reads: the changelog (about 1 M characters, read to the 2.1.288 entry) and the StationX guide (last 3,790 characters unread). StationX shows only "Updated October 2026": freshness scored 15, the lowest value any October 2026 date can give.
- Scoring interpretations: "last modified" / "updated on" dates shown on a page were accepted as its date; company content hubs (Kanaries, StationX) and company YouTube channels (Better Stack) were rated C; video summaries rely on the title and description returned by the tool, videos are never opened. The five other mods documentation pages returned by the owner search are folded into the overview entry.

---

## Executive Summary
Anthropic launched mods for Claude Code on October 1, 2026: JavaScript or TypeScript event handlers, shipped inside plugins, that run inside Claude Code and can draw panes and bands, add instant commands, and observe, rewrite or answer tool calls and prompts. Within nine days the feature produced a wave of YouTube "N mods you need" videos and dozens of community repositories and catalogues, while Anthropic kept shipping mod API additions and fixes almost daily (2.1.288 to 2.1.296). The unexpected part is the security posture: mods are on by default and not sandboxed, and the community answered with catalogues that audit what each mod can read, write, run or send, more than with research (no arXiv paper).

---

## Primary sources

**Customize Claude Code with mods in TypeScript** — 🔗 https://claude.com/blog/claude-code-mods — 📅 2026-10-01
Launch announcement: "Today we're introducing mods"; available in the Claude Code CLI and desktop app; mods ship inside plugins; not sandboxed; a built-in `sec-default` mod loads first on Team and Enterprise plans and on machines with managed settings. No minimum version and no preview period stated.

**Mods overview - Claude Code Docs** — 🔗 https://code.claude.com/docs/en/plugins/mods/overview — 📅 unverified
Reference definition and requirements: mods are on by default; terminal needs Claude Code v2.1.287 or later, the Desktop app works from v2.1.286; hooks run in the VS Code extension, `claude -p`, the Agent SDK and cloud sessions but draw only in the terminal and the Desktop Code tab; `claude plugin validate` lists a mod's hooks and calls before install; sample mods in `anthropics/claude-code-playground`, built-in mods (`diff`, `agents-md`, `sec-default`, `telemetry`) public in `anthropics/claude-code/mods`; an undated early-access flag `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS` is now ignored. Sibling pages: create, interface, events, api, admin (same `/docs/en/plugins/mods/` path).

**Claude Code changelog - Claude Code Docs** — 🔗 https://code.claude.com/docs/en/changelog — 📅 unverified
Release notes (latest entry read: 2.1.296, October 9, 2026): every release from 2.1.288 (October 2) to 2.1.296 carries mod changes, including `$.ui.selection()`, `prompt.autocomplete`, prompt caching in `$.model.complete`, `$.ui.notify`, and several fixes where a user-installed mod could bypass or unload an organization's guard. Entries for 2.1.287 and earlier were not read (truncated).

---

## Sources ranked by score

---

### 🔴 Essential (score 85–100)

**[1] Mods in Claude Code: change how Claude Code works**
🔗 https://www.youtube.com/watch?v=yUuFvL1lK4k
📅 2026-10-05 | ⭐ Authority: A Primary | 📊 Score: 94/100
**Summary**: Official video from the Claude channel (3:21) presenting mods as functions you write that change what Claude Code renders and what goes into a prompt. The only ranked source from the topic owner, and the shortest way into the feature.
**Score reason**: Exact match + A Primary (official channel), published 5 days ago, 372k views
**Tags**: `official`, `overview`, `video`

**[2] 9 NEW Claude Mods that can truly change how you work**
🔗 https://www.youtube.com/watch?v=lDrAZ1wAyVs
📅 2026-10-08 | ⭐ Authority: C Community | 📊 Score: 85/100
**Summary**: Walkthrough of nine mods by Jay E (RoboNuggets), 12:47, with a companion PDF guide announced in the description. The most viewed community video of the window.
**Score reason**: Exact match + C Community (YouTube creator), published 2 days ago, 433k views
**Tags**: `mod-roundup`, `video`, `workflow`

**[3] These Mods Take Claude Code to Another Level**
🔗 https://www.youtube.com/watch?v=UcvD53jqHRU
📅 2026-10-05 | ⭐ Authority: C Community | 📊 Score: 85/100
**Summary**: 15:41 video by Mark Kashef presenting a set of mods; the description announces free mods, code and prompts. Longest of the creator roundups under 20 minutes.
**Score reason**: Exact match + C Community (YouTube creator), published 5 days ago, 38k views
**Tags**: `mod-roundup`, `video`, `prompts`

**[4] Claude Code Just Dropped Mods: Here Are 5 You Need**
🔗 https://www.youtube.com/watch?v=W5JSvXig3Ig
📅 2026-10-06 | ⭐ Authority: C Community | 📊 Score: 85/100
**Summary**: Sharbel A. presents five mods (11:33); the description points to their install commands and a custom mod-building prompt. Illustrates the "describe it and Claude writes the mod" path the docs describe.
**Score reason**: Exact match + C Community (YouTube creator), published 4 days ago, 25k views
**Tags**: `mod-roundup`, `video`, `install`

**[5] Claude Mods Are Insane... You Need To Try These Right Now**
🔗 https://www.youtube.com/watch?v=ERNqRK6sMJY
📅 2026-10-09 | ⭐ Authority: C Community | 📊 Score: 85/100
**Summary**: AI LABS covers seven Claude Code mods in 13:28. The most recent video of the ranking, published eight days after launch.
**Score reason**: Exact match + C Community (YouTube creator), published 1 day ago, 19k views
**Tags**: `mod-roundup`, `video`

**[6] 3 Claude Code mods you need to build**
🔗 https://www.youtube.com/watch?v=WCwNECxFJ_Q
📅 2026-10-05 | ⭐ Authority: C Community | 📊 Score: 85/100
**Summary**: Build Great Products (13:43) frames mods as things to build rather than install, with three examples and a playbook announced in the description.
**Score reason**: Exact match + C Community (YouTube creator), published 5 days ago, 13k views
**Tags**: `build`, `video`, `tutorial`

---

### 🟠 High value (score 70–84)

**[7] Claude Code Mods Can Do Basically Anything...**
🔗 https://www.youtube.com/watch?v=EiThSVZ8pME
📅 2026-10-04 | ⭐ Authority: C Community | 📊 Score: 82/100
**Summary**: Better Stack (7:37) describes mods as small TypeScript plugins that run inside Claude Code and let you change its behavior and draw your own interface. Developer-oriented rather than productivity-oriented.
**Score reason**: Exact match + C Community (company YouTube channel), published 6 days ago, 39k views
**Tags**: `typescript`, `video`, `overview`

**[8] Claude Code Mods: The Ultimate Customization Guide**
🔗 https://www.youtube.com/watch?v=8wZVnc99x_k
📅 2026-10-08 | ⭐ Authority: C Community | 📊 Score: 82/100
**Summary**: Eric Tech (9:53) explains what mods are, on the angle that they change how Claude Code looks and works, not only what it knows.
**Score reason**: Exact match + C Community (YouTube creator), published 2 days ago, 12k views
**Tags**: `customization`, `video`, `guide`

**[9] Claude Code Mods (course lesson, AI development setup)**
🔗 https://stevekinney.com/courses/ai-development-setup/claude-code-mods
📅 2026-10-06 (last modified) | ⭐ Authority: C Community | 📊 Score: 81/100
**Summary**: Course lesson by Steve Kinney (about 1,800 words) that adds its own framing to the official docs: a comparison with Express middleware and fail-closed advice for guards. States mods are on by default as of v2.1.287 and are "unsandboxed code running as you", consistent with the docs.
**Score reason**: Exact match + C Community (personal course site), modified 4 days ago, > 1500 words
**Tags**: `course`, `guards`, `mental-model`

**[10] Claude Code Mods Tutorial: Build and Test Your First Mod, Plus 15 Community Examples**
🔗 https://docs.kanaries.net/topics/AICoding/claude-code-mods
📅 2026-10-07 (updated) | ⭐ Authority: C Community | 📊 Score: 81/100
**Summary**: About 4,000 words by Soren Atelier (Kanaries) with a "What I tested" section: mods built and tested by the author, plus a scan of a community catalogue. Restates the version floors of the docs (2.1.287 terminal, 2.1.286 Desktop) and notes the module has no Node and no DOM.
**Score reason**: Exact match + C Community (company content hub), updated 3 days ago, > 1500 words
**Tags**: `tutorial`, `testing`, `community-examples`

**[11] Claude Code Mods Just Turned Agents Into a Platform**
🔗 https://dev.to/max_quimby/claude-code-mods-just-turned-agents-into-a-platform-5gc0
📅 2026-10-04 | ⭐ Authority: C Community | 📊 Score: 81/100
**Summary**: Analysis piece by Max Quimby (about 2,300 words, first published on AgentConn) arguing mods turn the agent into a platform, and stressing there is "no review process, no signing, and no sandbox". Leans on X posts and third-party coverage rather than the official docs, so its figures should be checked against the primary sources.
**Score reason**: Exact match + C Community (dev.to post), published 6 days ago, > 1500 words
**Tags**: `analysis`, `platform`, `security`

**[12] Claude Code Mods Are Game Changers. Set Up These 5 NOW.**
🔗 https://www.youtube.com/watch?v=9hetShMMp2s
📅 2026-10-02 | ⭐ Authority: C Community | 📊 Score: 80/100
**Summary**: Nate Herk (11:19) sets up five mods the day after launch. Companion repository: https://github.com/nateherkai/claude-code-mods (Cache Keeper, Recording Mode, Goal Meter, Collision Guard; 17 stars, score 72, not ranked separately).
**Score reason**: Exact match + C Community (YouTube creator), published 8 days ago, 222k views
**Tags**: `mod-roundup`, `video`, `setup`

**[13] Claude Mods Is The Biggest Claude Code Upgrade Since Skills**
🔗 https://www.youtube.com/watch?v=Rn4nmFRPe0s
📅 2026-10-02 | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Chase AI (9:11), published the day after launch, positions mods against skills as the next major extension mechanism of Claude Code.
**Score reason**: Exact match + C Community (YouTube creator), published 8 days ago, 212k views
**Tags**: `video`, `skills-comparison`, `launch`

**[14] Claude Mods Just Dropped... Use these 3 NOW**
🔗 https://www.youtube.com/watch?v=moOBIaIb4a8
📅 2026-10-02 | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Jack Roberts (9:00) presents three mods the day after launch; the description offers a prompt to find mods suited to your own use.
**Score reason**: Exact match + C Community (YouTube creator), published 8 days ago, 42k views
**Tags**: `mod-roundup`, `video`, `launch`

**[15] Tickloop/claude-mods**
🔗 https://github.com/Tickloop/claude-mods
📅 2026-10-08 | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: "A collection of claude code mods" in TypeScript, created two days ago and already at 77 stars. A source of working mod code to read.
**Score reason**: Exact match + C Community repository created 2 days ago, 77 stars
**Tags**: `repository`, `typescript`, `collection`

**[16] whyashthakker/awesome-claude-code-mods**
🔗 https://github.com/whyashthakker/awesome-claude-code-mods
📅 2026-10-03 | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Collection announced as 100+ mods usable with Claude Code. One of three competing "awesome" lists that appeared in the window.
**Score reason**: Exact match + C Community repository created 7 days ago, 43 stars
**Tags**: `awesome-list`, `repository`, `collection`

**[17] wh000wh000/awesome-claude-mods**
🔗 https://github.com/wh000wh000/awesome-claude-mods
📅 2026-10-04 | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Index of Claude Code mods, plugins and hooks described as evidence-graded, in 20 languages and rebuilt every 2 hours. An automated catalogue, by contrast with hand-curated lists.
**Score reason**: Exact match + C Community repository created 6 days ago, 39 stars
**Tags**: `awesome-list`, `index`, `automation`

**[18] promptadvisers/claude-mods-computer-use-threads**
🔗 https://github.com/promptadvisers/claude-mods-computer-use-threads
📅 2026-10-05 | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Two mods with source, build prompts, setup and tests: a Codex computer-use bridge and coordinated Claude sessions. Companion repository from the same author: https://github.com/promptadvisers/claude-mods-starter-kit (ten mods, beginner guides and a build-your-own template; score 72).
**Score reason**: Exact match + C Community repository created 5 days ago, 11 stars
**Tags**: `repository`, `multi-session`, `codex`

**[19] aieo-product/claude_qamods**
🔗 https://github.com/aieo-product/claude_qamods
📅 2026-10-04 | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Mods that make Claude's questions easier to read and answer (topic `askuserquestion`), an example of redrawing Claude Code's own interface rather than adding a pane.
**Score reason**: Exact match + C Community repository created 6 days ago, 11 stars
**Tags**: `repository`, `interface`, `askuserquestion`

**[20] AgriciDaniel/claude-mods-brain**
🔗 https://github.com/AgriciDaniel/claude-mods-brain
📅 2026-10-03 | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Source-cited Obsidian knowledge base about mods: how they work, how to build them, and how to check one before installing it. Closest repository to a documentation companion.
**Score reason**: Exact match + C Community repository created 7 days ago, 9 stars
**Tags**: `knowledge-base`, `obsidian`, `review-before-install`

---

### 🟡 Worth including (score 60–69)

No ranked source in this band: the 20-source cap was reached at score 77.

---

## Trends identified

- Adoption was led by video: 11 of the 20 ranked sources are YouTube videos published between October 2 and 9, almost all in the same "N mods to install now" format, and nine of them exceed 10k views.
- The recurring mod types across repositories are the same few: a band above the prompt showing context, usage limits, cache countdown or cost; guards on tool calls; panes; and games or novelty displays.
- Security is the shared caveat. The primary sources state that mods are not sandboxed and run with the user's permissions, the changelog fixed several ways a user-installed mod could get past an organization's guard between 2.1.289 and 2.1.292, and community catalogues describe what each mod can read, write, run or send.
- Secondary sources drift on facts: among seven opened pages, one misdates the launch (October 3 instead of October 1) and one describes mods as running in a sealed environment, against the docs.
- Community repositories predate the announcement: catalogues and mods were created on September 14 to 16 and a video on September 18 calls mods "a hidden feature", consistent with the undated early-access period the docs mention.

---

*Generated by tech-watch skill | Sources used: GitHub · YouTube · Web (Tier 2) · Owner domains*
*Scoring: Relevance 40% · Freshness 20% · Authority 20% · Depth 10% · Engagement 10%*
