# Tech Watch — Claude Mods
**Date**: 2026-10-10 | **Window**: 30 days | **Topic**: Claude Code mods (owner: Anthropic) | **Sources**: 20 ranked + 3 primary

| Source | Status | Raw | On-topic | In report |
|---|---|---|---|---|
| arXiv | empty | 0 | 0 | 0 |
| GitHub | ok | 20 | 19 | 6 |
| YouTube | ok | 15 | 14 | 11 |
| Web (Tier 2) | ok | 28 | 28 | 3 |
| Web (Tier 3) | not run (unique on-topic ≥ 12) | – | – | 0 |
| Owner domains | ok | 10 | – | 3 |

**Pipeline**: 63 raw → 61 on-topic, 0 adjacent, 1 homonyms, 1 dropped → 57 unique → 39 ≥ 60 → 20 ranked (cap 20).
**Enrichment**: 10/10 pages opened (3 primary), 0 failures, 2 truncated.
**Date test**: skipped (the docs overview mentions an "early access" period without dating it; the changelog read was truncated before the launch entries).
**Notes**:
- Cap cut: 39 sources reached 60, 19 were cut. Two sources scored 77 like the last ranked ones and lost on the engagement tie-break: `ersinkoc/claude-mods` (9 stars, an exact tie with rank 20, which the tie-break rule does not resolve; the tool's best-match order decided) and the dev.to tutorial by Bobby Hall Jr. (no engagement signal; it also dates the launch to 2026-10-03, which contradicts the Anthropic post). Among the cut repositories: `hamzafer/claude-code-mods` (74, 177 stars) and the catalogue `karanb192/awesome-claude-code-mods` (64, 456 stars, created 2026-09-15).
- Unopened pages: 17 unique Tier 2 web pages were not opened (budget exhausted). With date, length and authority `unverified` they cannot reach 60 and are excluded, including several dev.to / Medium / Substack posts and the it-connect, claudekit, braindetox and laozhang guides.
- Truncated reads: the changelog (only 2.1.296 to 2.1.288 read, so the 2.1.287 launch entry and any early-access entry were not seen) and the StationX guide (last 3,790 characters not read).
- Scoring interpretations: StationX, Kanaries and Steve Kinney show only an "updated" / "last modified" date, used as the verified date; StationX shows the month only ("October 2026"), scored at the lower freshness bound (15). Better Stack and StationX are scored B (identified organization with original content); all other creators and repositories are C.
- Homonym (meaning test): `0xDarkMatter/claude-mods` (created 2025-11-27; a skills/agents/commands toolkit, not the mods plugin type). Dropped: one Better Stack Short (1:29). Localized duplicates folded: `code.claude.com/docs/de|it/plugins/mods/create`, it-connect.fr, pasqualepillitteri.it/es, StationX returned twice.

---

## Executive Summary
Anthropic launched mods for Claude Code on 2026-10-01: a plugin type made of JavaScript or TypeScript event handlers that run inside Claude Code and can redraw the interface, rewrite prompts and intercept tool calls. Within ten days the ecosystem is dominated by creator videos and small community mod collections, mostly "bands above the prompt" (usage meters, context bars) and tool-call guards, while independent catalogues try to index and audit thousands of public mods. The unexpected part is how central security is: the official docs state mods are not sandboxed and run with the user's permissions, and the most substantial third-party guides spend much of their length on vetting a mod before installing it. No research paper covers the topic yet.

---

## Primary sources

**Customize Claude Code with mods in TypeScript** — 🔗 https://claude.com/blog/claude-code-mods — 📅 2026-10-01
Anthropic's announcement: mods are available in the Claude Code CLI and desktop app as of the post; they are not sandboxed ("you should only install mods from sources you trust"); built-in features such as `/diff` ship as mods; on Team and Enterprise plans and managed machines the built-in `sec-default` mod loads first. No minimum version is stated in the post.

**Mods overview - Claude Code Docs** — 🔗 https://code.claude.com/docs/en/plugins/mods/overview — 📅 unverified
Reference documentation: mods are on by default, require Claude Code v2.1.287 or later in the terminal (v2.1.286 in the Desktop app); hooks run everywhere a plugin loads, but drawn UI appears only in the terminal and the Desktop Code tab (not in the VS Code chat panel, `claude -p` or cloud sessions); install with `/plugin install <name>@<marketplace>`, inspect with `claude plugin validate`; an undated early-access period used the `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS` variable, now ignored. Sample mods live in `anthropics/claude-code-playground`, built-in mod sources in `anthropics/claude-code/mods`.

**Claude Code changelog** — 🔗 https://code.claude.com/docs/en/changelog — 📅 unverified
Rolling release notes (read from 2.1.296, 2026-10-09, down to 2.1.288, 2026-10-02; truncated below): the mods API changes in almost every release since launch (`$.ui.notify`, `isDeferred` on `$.tool.register`, prompt caching in `$.model.complete`, `serverToolUses`), and 2.1.290 fixes a case where a user-installed mod could make an organization's guard skip its check.

---

## Sources ranked by score

---

### 🔴 Essential (score 85–100)

**[1] Mods in Claude Code: change how Claude Code works**
🔗 https://www.youtube.com/watch?v=yUuFvL1lK4k
📅 2026-10-05 | ⭐ Authority: A Primary | 📊 Score: 94/100
**Summary**: Official video from the Claude channel (3:21) presenting mods as functions you write that change what Claude Code renders, what goes into a prompt and how tool calls behave. The shortest authoritative overview of the feature.
**Score reason**: Exact match + A Primary (official channel), published 5 days ago, 372k views
**Tags**: `official`, `overview`, `video`

**[2] Claude Code Mods Can Do Basically Anything...**
🔗 https://www.youtube.com/watch?v=EiThSVZ8pME
📅 2026-10-04 | ⭐ Authority: B Expert | 📊 Score: 88/100
**Summary**: Better Stack walkthrough (7:37) describing mods as small TypeScript plugins that run inside Claude Code, changing its behavior and drawing custom UI. A developer-oriented demo rather than a list of mods to install.
**Score reason**: Exact match + B Expert (engineering organization channel), published 6 days ago, 38.9k views
**Tags**: `demo`, `typescript`, `video`

**[3] 9 NEW Claude Mods that can truly change how you work**
🔗 https://www.youtube.com/watch?v=lDrAZ1wAyVs
📅 2026-10-08 | ⭐ Authority: C Community | 📊 Score: 85/100
**Summary**: Tour of nine mods by Jay E (RoboNuggets), 12:47, with an accompanying PDF guide. The most-viewed video of the watch, a good indicator of which mod ideas reach a wide audience.
**Score reason**: Exact match + C Community creator, published 2 days ago, 433k views
**Tags**: `roundup`, `workflow`, `video`

**[4] These Mods Take Claude Code to Another Level**
🔗 https://www.youtube.com/watch?v=UcvD53jqHRU
📅 2026-10-05 | ⭐ Authority: C Community | 📊 Score: 85/100
**Summary**: Mark Kashef (15:41) demonstrates a set of mods and distributes the code and prompts used to build them. Longer than most creator videos, with build material attached.
**Score reason**: Exact match + C Community creator, published 5 days ago, 38.3k views
**Tags**: `roundup`, `build-prompts`, `video`

**[5] Claude Code Just Dropped Mods: Here Are 5 You Need**
🔗 https://www.youtube.com/watch?v=W5JSvXig3Ig
📅 2026-10-06 | ⭐ Authority: C Community | 📊 Score: 85/100
**Summary**: Sharbel A. (11:33) presents five mods with their install commands and a custom mod-building prompt. Useful for the install path through the plugin system.
**Score reason**: Exact match + C Community creator, published 4 days ago, 25k views
**Tags**: `roundup`, `install`, `video`

**[6] Claude Mods Are Insane... You Need To Try These Right Now**
🔗 https://www.youtube.com/watch?v=ERNqRK6sMJY
📅 2026-10-09 | ⭐ Authority: C Community | 📊 Score: 85/100
**Summary**: AI LABS (13:28) reviews seven Claude Code mods. The most recent roundup in the window, published eight days after launch.
**Score reason**: Exact match + C Community creator, published 1 day ago, 19.2k views
**Tags**: `roundup`, `video`

**[7] 3 Claude Code mods you need to build**
🔗 https://www.youtube.com/watch?v=WCwNECxFJ_Q
📅 2026-10-05 | ⭐ Authority: C Community | 📊 Score: 85/100
**Summary**: Build Great Products (13:43) focuses on building three mods rather than installing existing ones, with a companion playbook. Fits the "ask Claude to write the mod" path documented by Anthropic.
**Score reason**: Exact match + C Community creator, published 5 days ago, 13.1k views
**Tags**: `build`, `tutorial`, `video`

---

### 🟠 High value (score 70–84)

**[8] Claude Code Mods: The Ultimate Customization Guide**
🔗 https://www.youtube.com/watch?v=8wZVnc99x_k
📅 2026-10-08 | ⭐ Authority: C Community | 📊 Score: 82/100
**Summary**: Eric Tech (9:53) explains what mods are and how they change how Claude Code looks and works, "not just what it knows". Positions mods against skills and other customization mechanisms.
**Score reason**: Exact match + C Community creator, published 2 days ago, 11.7k views
**Tags**: `guide`, `customization`, `video`

**[9] Claude Code Mods: The Complete Guide + 34 Videos (2026)**
🔗 https://app.stationx.net/articles/claude-code-mods
📅 updated October 2026 (day and publication date unverified) | ⭐ Authority: B Expert | 📊 Score: 82/100
**Summary**: Long guide (about 10,000 words) by Nathan House, founder of StationX, combining the official docs, 34 videos, the author's own mod builds, a copy-paste lab with test output and a 5 October re-scan of public catalogues. It gives v2.1.287 and 2026-10-01 as the launch markers, describes a September 2026 preview behind an opt-in flag, and warns that many guides still describe that preview.
**Score reason**: Exact match + B Expert (security training organization, original tests), > 1,500 words, updated this month
**Tags**: `guide`, `security`, `catalogue-scan`

**[10] Claude Code Mods Tutorial: Build and Test Your First Mod, Plus 15 Community Examples**
🔗 https://docs.kanaries.net/topics/AICoding/claude-code-mods
📅 updated 2026-10-07 (publication date unverified) | ⭐ Authority: C Community | 📊 Score: 81/100
**Summary**: Hands-on tutorial (about 4,500 words) by Soren Atelier on Kanaries: three mods built and tested on Claude Code 2.1.293 with `claude plugin validate` and automated test runs, plus install commands for a third-party mod and for a local folder. States that the API "is in early access and changes between releases", which matches the pace of the changelog.
**Score reason**: Exact match + C Community with original tests, updated 3 days ago, > 1,500 words
**Tags**: `tutorial`, `testing`, `examples`

**[11] Claude Code mods (AI development setup course)**
🔗 https://stevekinney.com/courses/ai-development-setup/claude-code-mods
📅 last modified 2026-10-06 (publication date unverified) | ⭐ Authority: C Community | 📊 Score: 81/100
**Summary**: Course chapter by Steve Kinney (about 1,800 words) with its own guidance, anti-patterns, a sample hook and a worked example. Confirms mods are on by default as of v2.1.287.
**Score reason**: Exact match + C Community (personal course site, original examples), modified 4 days ago, > 1,500 words
**Tags**: `course`, `best-practices`, `anti-patterns`

**[12] Claude Code Mods Are Game Changers. Set Up These 5 NOW.**
🔗 https://www.youtube.com/watch?v=9hetShMMp2s
📅 2026-10-02 | ⭐ Authority: C Community | 📊 Score: 80/100
**Summary**: Nate Herk (11:19) sets up five mods the day after launch. Companion repository: `nateherkai/claude-code-mods` (Cache Keeper, Recording Mode, Goal Meter, Collision Guard), which was cut by the cap.
**Score reason**: Exact match + C Community creator, published 8 days ago, 222k views
**Tags**: `roundup`, `setup`, `video`

**[13] Claude Mods Is The Biggest Claude Code Upgrade Since Skills**
🔗 https://www.youtube.com/watch?v=Rn4nmFRPe0s
📅 2026-10-02 | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Chase AI (9:11) frames mods as the largest extension mechanism since skills. One of the earliest high-reach reactions to the launch.
**Score reason**: Exact match + C Community creator, published 8 days ago, 212k views
**Tags**: `overview`, `skills-comparison`, `video`

**[14] Claude Mods Just Dropped... Use these 3 NOW**
🔗 https://www.youtube.com/watch?v=moOBIaIb4a8
📅 2026-10-02 | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Jack Roberts (9:00) presents three mods and a prompt for finding mods suited to one's own workflow. Launch-week content aimed at non-developers.
**Score reason**: Exact match + C Community creator, published 8 days ago, 41.5k views
**Tags**: `roundup`, `video`

**[15] Tickloop/claude-mods**
🔗 https://github.com/Tickloop/claude-mods
📅 2026-10-08 (created) | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: A TypeScript collection of Claude Code mods, 77 stars two days after creation. One of the fastest-growing small collections in the window.
**Score reason**: Exact match + C Community repository created 2 days ago, 77 stars
**Tags**: `collection`, `typescript`, `repository`

**[16] whyashthakker/awesome-claude-code-mods**
🔗 https://github.com/whyashthakker/awesome-claude-code-mods
📅 2026-10-03 (created) | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Collection of more than 100 mods usable with Claude Code, in TypeScript. A curated list rather than a single mod.
**Score reason**: Exact match + C Community repository created 7 days ago, 43 stars
**Tags**: `awesome-list`, `collection`, `repository`

**[17] wh000wh000/awesome-claude-mods**
🔗 https://github.com/wh000wh000/awesome-claude-mods
📅 2026-10-04 (created) | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Evidence-graded index of Claude Code mods, plugins and hooks, available in 20 languages and rebuilt every 2 hours. Represents the automated-catalogue approach to the mod ecosystem.
**Score reason**: Exact match + C Community repository created 6 days ago, 39 stars
**Tags**: `index`, `automation`, `repository`

**[18] promptadvisers/claude-mods-computer-use-threads**
🔗 https://github.com/promptadvisers/claude-mods-computer-use-threads
📅 2026-10-05 (created) | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Two mods with source, build prompts, setup and tests: a Codex computer-use bridge and coordinated Claude sessions. Companion repository from the same organization: `promptadvisers/claude-mods-starter-kit` (ten mods, beginner guides, build-your-own template; score 72, cut by the cap).
**Score reason**: Exact match + C Community repository created 5 days ago, 11 stars
**Tags**: `multi-session`, `codex`, `repository`

**[19] aieo-product/claude_qamods**
🔗 https://github.com/aieo-product/claude_qamods
📅 2026-10-04 (created) | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Mods that restyle the dialog in which Claude asks questions so they are easier to read and answer. An example of the "redraw Claude Code's own interface" capability described in the docs.
**Score reason**: Exact match + C Community repository created 6 days ago, 11 stars
**Tags**: `ui`, `askuserquestion`, `repository`

**[20] AgriciDaniel/claude-mods-brain**
🔗 https://github.com/AgriciDaniel/claude-mods-brain
📅 2026-10-03 (created) | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Source-cited Obsidian knowledge base about Claude Code mods: how they work, how to build them and how to check one before installing it. Documentation-oriented rather than code-oriented.
**Score reason**: Exact match + C Community repository created 7 days ago, 9 stars
**Tags**: `knowledge-base`, `vetting`, `repository`

---

### 🟡 Worth including (score 60–69)

None in the ranking: the 20-source cap was reached at score 77.

---

## Trends identified

- Launch-week content is overwhelmingly "N mods you need" videos: 11 of the 20 ranked sources are YouTube videos, most published within 8 days of the 2026-10-01 announcement, and several creators publish a companion repository of the mods they show.
- The dominant mod pattern across repositories is a band above the prompt showing live session data (context in tokens, 5-hour and weekly limits, cache countdown, cost, plan progress), followed by tool-call guards; games and "companions" are a visible third category.
- Security is the cross-cutting theme: the Anthropic post and docs state that mods are not sandboxed and run with the user's permissions, the changelog already contains a fix for a mod bypassing an organization's guard, and the in-depth third-party guides centre on `claude plugin validate` and reading the code before installing.
- Catalogues appeared before the ecosystem stabilized: several "awesome" lists and automated indexes were created within days, some scanning public mods for what they read, write, run or send over the network. Repositories created in mid-September and guides mentioning a September preview show activity predates the public launch.
- The API is still moving: the changelog adds or fixes mod APIs in nearly every release from 2.1.288 to 2.1.296, so tutorials age quickly and should be checked against the docs' v2.1.287 floor and current reference.

---

*Generated by tech-watch skill | Sources used: GitHub · YouTube · Web (Tier 2) · Owner domains*
*Scoring: Relevance 40% · Freshness 20% · Authority 20% · Depth 10% · Engagement 10%*
