# Tech Watch — Claude Code mods
**Date**: 2026-10-10 | **Window**: 30 days | **Sources**: 20

**Pipeline counts**: 63 raw results (arXiv 0, GitHub 20, YouTube 15, web 28) | 54 on-topic, 1 adjacent, 1 off-topic before deduplication | 7 dropped unlabeled (1 video under 3 minutes, 6 web results without a usable title, including two translated `code.claude.com` documentation pages) | 51 unique on-topic after deduplication | Tier 3 not run (51 >= 12)
**Enrichment**: 10 pages opened out of a budget of 10, 0 fetch failures; 4 pages (dev.to) show a day and month but no year, so their date stays `unverified`
**Selection**: 38 sources scored 70 or more; the 20 highest are kept (target 15-20). Ties at 89 were broken by GitHub stars. The best web articles peak at 85 and fall below the cut.
**Freshness basis**: publication date for videos, last push date for repositories.

---

## Executive Summary
Claude Code mods (plugins made of JavaScript or TypeScript functions, built on hooks, that run inside Claude Code and can draw UI above the prompt, guard tool calls and alter prompts) triggered a burst of content concentrated in nine days: the first large wave of videos is dated 2026-10-02, and 14 of the 20 repositories returned were created on or after that date. The dominant pattern is "N mods to install now" videos backed by companion repositories, followed almost immediately by catalogues and "awesome" lists that index public mods and what each one can read, write, run or send. Unexpected: several repositories (2026-09-14 to 2026-09-16) and one video (2026-09-18, describing mods as a "hidden feature") predate the main wave by two weeks, and no arXiv paper covers the topic yet.

---

## Sources ranked by score

---

### 🔴 Essential (score 85–100)

**[1] 9 NEW Claude Mods that can truly change how you work**
🔗 https://www.youtube.com/watch?v=lDrAZ1wAyVs
📅 2026-10-08 | ⭐ Authority: High | 📊 Score: 100/100
**Summary**: Jay E (RoboNuggets) presents nine Claude mods in 12:47, with a companion PDF guide. With 427,164 views it is the most watched video of the window on this topic.
**Score reason**: Direct match on query + YouTube video from 2 days ago with 427k views
**Tags**: `youtube`, `mod-roundup`, `workflow`

**[2] Claude Mods - The Biggest Claude Code Upgrade!**
🔗 https://www.youtube.com/watch?v=XaYubuLtW8M
📅 2026-10-03 | ⭐ Authority: High | 📊 Score: 100/100
**Summary**: Prompt Engineering explains that mods let you run your own JavaScript or TypeScript functions inside Claude Code, and that a mod can watch or change what happens in a session. 10:37, 65,136 views.
**Score reason**: Direct match on query + explanatory video from 7 days ago with 65k views
**Tags**: `youtube`, `explainer`, `typescript`

**[3] Claude Code Mods Can Do Basically Anything...**
🔗 https://www.youtube.com/watch?v=EiThSVZ8pME
📅 2026-10-04 | ⭐ Authority: High | 📊 Score: 100/100
**Summary**: Better Stack describes mods as small TypeScript plugins that run inside Claude Code, letting you change its behavior and draw your own interface elements. 7:37, 38,854 views.
**Score reason**: Direct match on query + developer-channel video from 6 days ago with 38k views
**Tags**: `youtube`, `explainer`, `custom-ui`

**[4] These Mods Take Claude Code to Another Level**
🔗 https://www.youtube.com/watch?v=UcvD53jqHRU
📅 2026-10-05 | ⭐ Authority: High | 📊 Score: 100/100
**Summary**: Mark Kashef walks through a set of mods in 15:41 and distributes the mods, code and prompts for free. 38,239 views.
**Score reason**: Direct match on query + long-form video from 5 days ago with 38k views
**Tags**: `youtube`, `mod-roundup`, `prompts`

**[5] Claude Mods Are Insane... You Need To Try These Right Now**
🔗 https://www.youtube.com/watch?v=ERNqRK6sMJY
📅 2026-10-09 | ⭐ Authority: High | 📊 Score: 100/100
**Summary**: AI LABS covers seven Claude Code mods in 13:28. Published yesterday, 18,444 views; the description carries a sponsor link.
**Score reason**: Direct match on query + video from 1 day ago with 18k views
**Tags**: `youtube`, `mod-roundup`, `sponsored`

**[6] 3 Claude Code mods you need to build**
🔗 https://www.youtube.com/watch?v=WCwNECxFJ_Q
📅 2026-10-05 | ⭐ Authority: High | 📊 Score: 100/100
**Summary**: Build Great Products focuses on building mods rather than installing them: three mods in 13:43, with a free playbook. 13,017 views.
**Score reason**: Direct match on query + build-oriented video from 5 days ago with 13k views
**Tags**: `youtube`, `build-your-own`, `tutorial`

**[7] Claude Code Mods Are Game Changers. Set Up These 5 NOW.**
🔗 https://www.youtube.com/watch?v=9hetShMMp2s
📅 2026-10-02 | ⭐ Authority: High | 📊 Score: 95/100
**Summary**: Nate Herk sets up five mods in 11:19; one of the first videos of the wave, with 221,836 views. His companion repository `nateherkai/claude-code-mods` lists four mods: Cache Keeper, Recording Mode, Goal Meter and Collision Guard.
**Score reason**: Direct match on query + 221k views, 8 days old
**Tags**: `youtube`, `mod-roundup`, `setup`

**[8] Claude Mods Is The Biggest Claude Code Upgrade Since Skills**
🔗 https://www.youtube.com/watch?v=Rn4nmFRPe0s
📅 2026-10-02 | ⭐ Authority: High | 📊 Score: 95/100
**Summary**: Chase AI positions mods as the largest Claude Code change since skills. 9:11, 212,410 views, published the same day as the other first-wave videos.
**Score reason**: Direct match on query + 212k views, 8 days old
**Tags**: `youtube`, `positioning`, `skills-vs-mods`

**[9] Claude Mods Just Dropped... Use these 3 NOW**
🔗 https://www.youtube.com/watch?v=moOBIaIb4a8
📅 2026-10-02 | ⭐ Authority: High | 📊 Score: 95/100
**Summary**: Jack Roberts presents three mods in 9:00 and shares a prompt meant to help viewers find the mods that suit them. 41,372 views.
**Score reason**: Direct match on query + 41k views, 8 days old
**Tags**: `youtube`, `mod-roundup`, `prompts`

**[10] Anthropic Mods for Claude Code: Too Much Power?**
🔗 https://www.youtube.com/watch?v=xG9UIliOX3E
📅 2026-10-03 | ⭐ Authority: High | 📊 Score: 95/100
**Summary**: Stacked Podcast episode (26:15) that questions how much power mods hand to third-party code; the only critical-angle video in the set. The episode also covers an unrelated robotics story, so only part of it is on mods. 7,582 views.
**Score reason**: Direct match on query + long-form discussion from 7 days ago
**Tags**: `youtube`, `podcast`, `risk`

**[11] Claude Code vient de lancer les mods : voici mes 5 indispensables**
🔗 https://www.youtube.com/watch?v=1Dlh_Mqze1s
📅 2026-10-09 | ⭐ Authority: High | 📊 Score: 95/100
**Summary**: French-language video by Tony Lotis presenting five mods he considers essential, plus a skill for creating your own. 13:20, 7,526 views.
**Score reason**: Direct match on query + video from 1 day ago
**Tags**: `youtube`, `french`, `mod-roundup`

**[12] Claude Code Mods Are INSANE (Master it in 9 minutes)**
🔗 https://www.youtube.com/watch?v=oL6yb21XhDQ
📅 2026-10-08 | ⭐ Authority: High | 📊 Score: 95/100
**Summary**: Shab Noor's 8:59 introduction to Claude Code mods, aimed at operators rather than developers. Very low reach so far (359 views).
**Score reason**: Direct match on query + video from 2 days ago
**Tags**: `youtube`, `beginner`, `operators`

**[13] Mods in Claude Code: change how Claude Code works**
🔗 https://www.youtube.com/watch?v=yUuFvL1lK4k
📅 2026-10-05 | ⭐ Authority: High | 📊 Score: 94/100
**Summary**: The official video from the Claude channel: mods are functions you write that change what Claude Code renders and what goes into a prompt. Short (3:21) but the primary source of the set, with 371,304 views.
**Score reason**: Direct match on query + official channel, 371k views (short format costs depth points)
**Tags**: `youtube`, `official`, `anthropic`

**[14] karanb192/awesome-claude-code-mods**
🔗 https://github.com/karanb192/awesome-claude-code-mods
📅 created 2026-09-15, last push 2026-10-10 | ⭐ Authority: High | 📊 Score: 89/100
**Summary**: Community catalogue of public Claude Code mods (described as function hooks), scanned from GitHub and annotated with what each mod can read, write, run or send over the network. Most starred repository of the set (453 stars), browsable at mods.aidojo.si.
**Score reason**: Direct match on query + GitHub repo pushed today, 453 stars
**Tags**: `github`, `catalogue`, `permissions-audit`

**[15] hamzafer/claude-code-mods**
🔗 https://github.com/hamzafer/claude-code-mods
📅 created 2026-10-02, last push 2026-10-09 | ⭐ Authority: High | 📊 Score: 89/100
**Summary**: A collection of mods built on hooks that add live lines above the prompt, guards, panes and games: context bar, usage meter, Codex review watch, Markdown preview, Spotify now playing. TypeScript, 176 stars.
**Score reason**: Direct match on query + GitHub repo pushed 1 day ago, 176 stars
**Tags**: `github`, `mod-collection`, `typescript`

**[16] JohnnyVizz/claude-kit**
🔗 https://github.com/JohnnyVizz/claude-kit
📅 created 2026-10-04, last push 2026-10-04 | ⭐ Authority: High | 📊 Score: 89/100
**Summary**: Public Claude Code skills and mods in one TypeScript repository. The description is minimal and mixes skills with mods, so the share of mod content is not known from the listing. 121 stars.
**Score reason**: Match on query + GitHub repo pushed 6 days ago, 121 stars
**Tags**: `github`, `skills`, `mod-collection`

**[17] Tickloop/claude-mods**
🔗 https://github.com/Tickloop/claude-mods
📅 created 2026-10-08, last push 2026-10-08 | ⭐ Authority: High | 📊 Score: 89/100
**Summary**: A collection of Claude Code mods in TypeScript, created two days ago and already at 77 stars. The listing gives no detail on which mods it contains.
**Score reason**: Direct match on query + GitHub repo pushed 2 days ago, 77 stars
**Tags**: `github`, `mod-collection`, `typescript`

**[18] darrell-tw/darrelltw-mods**
🔗 https://github.com/darrell-tw/darrelltw-mods
📅 created 2026-09-16, last push 2026-10-05 | ⭐ Authority: High | 📊 Score: 89/100
**Summary**: Mods by Darrell Wang that draw bands above the prompt without consuming model tokens, starting with a Taiwan and US stock board. Created 2026-09-16, before the main wave. 65 stars.
**Score reason**: Direct match on query + GitHub repo pushed 5 days ago, 65 stars
**Tags**: `github`, `prompt-bands`, `early-adopter`

**[19] whyashthakker/awesome-claude-code-mods**
🔗 https://github.com/whyashthakker/awesome-claude-code-mods
📅 created 2026-10-03, last push 2026-10-03 | ⭐ Authority: High | 📊 Score: 89/100
**Summary**: A collection announced as 100+ mods usable with Claude Code. A second "awesome" list next to source 14, without the per-mod permission annotations. 43 stars.
**Score reason**: Direct match on query + GitHub repo pushed 7 days ago, 43 stars
**Tags**: `github`, `awesome-list`, `mod-collection`

**[20] zycck/claude-mods**
🔗 https://github.com/zycck/claude-mods
📅 created 2026-10-02, last push 2026-10-08 | ⭐ Authority: High | 📊 Score: 89/100
**Summary**: A single-purpose mod set: live plan progress bars displayed above the prompt. TypeScript, 42 stars.
**Score reason**: Direct match on query + GitHub repo pushed 2 days ago, 42 stars
**Tags**: `github`, `progress-bar`, `typescript`

---

### 🟠 High value (score 70–84)

None in the final selection: the 20 retained sources all score 89 or more. Eighteen further sources scored 70 to 89 and were cut by the 20-source target (11 GitHub repositories, 1 video, 6 web articles).

---

### 🟡 Worth including (score 60–69)

None retained: the total exceeds 20 sources.

---

## Trends identified

- **Launch-week concentration**: 13 of the 14 eligible videos were published between 2026-10-02 and 2026-10-09, and most share the same "install these N mods now" format; only two sources (6 and the builder-oriented repositories) focus on writing a mod yourself.
- **Indexing followed within days**: three catalogues or awesome lists appeared in the window, one of them annotating each mod with what it can read, write, run or send over the network, which suggests that trust in third-party mods is already a concern.
- **The UI surface dominates**: repository descriptions converge on the same objects, namely bands and live lines above the prompt, usage and context meters, panes, and tool-call guards; mods that change prompts or behavior are far less represented than visual ones.
- **Creators ship code with their videos**: several video authors publish a companion repository or a free pack, so the videos and the GitHub results are two faces of the same content rather than independent signals.
- **Early signals before the wave, no research yet**: repositories from 2026-09-14 to 2026-09-16 and a 2026-09-18 video calling mods a "hidden feature" predate the main wave; arXiv returned 0 papers, as expected for a product feature this recent.

---

*Generated by tech-watch skill | Sources: arXiv · GitHub · YouTube · Web search*
*Scoring: Relevance 40% · Freshness 20% · Authority 20% · Depth 10% · Engagement 10%*
