# Tech Watch — Claude Code mods
**Date**: 2026-10-10 | **Window**: 30 days | **Sources**: 20

**Pipeline counts**: 63 raw results (arXiv 0, GitHub 20, YouTube 15, web 28) | 55 on-topic (53 unique after deduplication) | 1 adjacent | 1 off-topic | 6 dropped for lack of a usable title | Tier 3 not run (unique on-topic >= 12)
**Enrichment**: 0 pages opened out of a budget of 10, 0 failures. `WebFetch` was not available in this run, so no web candidate could be verified: date, length and authority stay `unverified` for all 20 unique web candidates, which caps them at 59/100 (below the threshold). None is listed below.
**Scoring notes**: freshness of a repository is computed from its last push date. The 20 sources kept are the top 20 by score; ties at 89 are broken by star count. 14 more Tier 1 results scored 60 or above and were cut by the 20-source cap (12 repositories at 84-89, one video at 74, one repository at 72), plus one adjacent repository at 69.

---

## Executive Summary
Claude Code mods are a new extension mechanism: per the official Claude channel, functions the user writes that change what Claude Code renders, what goes into a prompt and more; community sources describe them as TypeScript/JavaScript plugins built on hooks. Within the 30-day window the topic went from a handful of repositories in mid-September to a dense wave of "top N mods" videos and mod collections published between 2026-10-02 and 2026-10-10, with two competing community catalogues already rebuilt continuously. The unexpected part is the imbalance: no research paper at all, and a recurring concern about what a mod can read, write, run or send over the network, visible in a catalogue's own description and in a podcast title, while most content is install-and-try material.

---

## Sources ranked by score

---

### 🔴 Essential (score 85–100)

**[1] 9 NEW Claude Mods that can truly change how you work**
🔗 https://www.youtube.com/watch?v=lDrAZ1wAyVs
📅 2026-10-08 | ⭐ Authority: High | 📊 Score: 100/100
**Summary**: Walkthrough of nine mods by Jay E (RoboNuggets), 12:47, with an accompanying PDF guide. The most viewed video of the batch (427,164 views), so a good proxy for which mods the wider audience is being pointed to.
**Score reason**: Direct match on query + published 2 days ago with the highest view count of the set
**Tags**: `claude-code-mods`, `showcase`, `video`

**[2] Claude Code Mods Can Do Basically Anything...**
🔗 https://www.youtube.com/watch?v=EiThSVZ8pME
📅 2026-10-04 | ⭐ Authority: High | 📊 Score: 100/100
**Summary**: Better Stack presents mods as small TypeScript plugins that run inside Claude Code, changing its behavior and drawing custom UI (7:37, 38,847 views). One of the few videos whose description is about the mechanism rather than a list of picks.
**Score reason**: Direct match on query + 6 days old with > 10k views
**Tags**: `claude-code-mods`, `typescript`, `explainer`

**[3] These Mods Take Claude Code to Another Level**
🔗 https://www.youtube.com/watch?v=UcvD53jqHRU
📅 2026-10-05 | ⭐ Authority: High | 📊 Score: 100/100
**Summary**: Mark Kashef's 15:41 walkthrough of mods, with the mods, code and prompts offered as a free download (38,239 views). Useful as a longer-form demonstration.
**Score reason**: Direct match on query + 5 days old with > 10k views
**Tags**: `claude-code-mods`, `showcase`, `video`

**[4] Claude Code Just Dropped Mods: Here Are 5 You Need**
🔗 https://www.youtube.com/watch?v=W5JSvXig3Ig
📅 2026-10-06 | ⭐ Authority: High | 📊 Score: 100/100
**Summary**: Sharbel A. covers five mods with their install commands and a custom mod-building prompt (11:33, 24,901 views). Relevant for the install path and the "ask Claude to build the mod" workflow.
**Score reason**: Direct match on query + 4 days old with > 10k views
**Tags**: `claude-code-mods`, `install`, `video`

**[5] Claude Mods Are Insane... You Need To Try These Right Now**
🔗 https://www.youtube.com/watch?v=ERNqRK6sMJY
📅 2026-10-09 | ⭐ Authority: High | 📊 Score: 100/100
**Summary**: AI LABS reviews seven Claude Code mods (13:28, 18,397 views). The most recent of the high-view showcase videos; the description is sponsor-led.
**Score reason**: Direct match on query + published yesterday with > 10k views
**Tags**: `claude-code-mods`, `showcase`, `video`

**[6] 3 Claude Code mods you need to build**
🔗 https://www.youtube.com/watch?v=WCwNECxFJ_Q
📅 2026-10-05 | ⭐ Authority: High | 📊 Score: 100/100
**Summary**: Build Great Products focuses on building three mods rather than installing existing ones (13:43, 13,017 views), with a playbook behind a community sign-up. One of the few build-oriented videos.
**Score reason**: Direct match on query + 5 days old with > 10k views
**Tags**: `claude-code-mods`, `build`, `video`

**[7] Claude Code Mods: The Ultimate Customization Guide**
🔗 https://www.youtube.com/watch?v=8wZVnc99x_k
📅 2026-10-08 | ⭐ Authority: High | 📊 Score: 100/100
**Summary**: Eric Tech explains what mods are and frames them as changing how Claude Code looks and works, "not just what it knows" (9:53, 11,536 views). Useful for positioning mods against knowledge-oriented extensions.
**Score reason**: Direct match on query + 2 days old with > 10k views
**Tags**: `claude-code-mods`, `customization`, `explainer`

**[8] Claude Code Mods Are Game Changers. Set Up These 5 NOW.**
🔗 https://www.youtube.com/watch?v=9hetShMMp2s
📅 2026-10-02 | ⭐ Authority: High | 📊 Score: 95/100
**Summary**: Nate Herk's setup video for five mods (11:19, 221,816 views), among the earliest of the wave. Pairs with the author's own repository `nateherkai/claude-code-mods` (Cache Keeper, Recording Mode, Goal Meter, Collision Guard), which was cut by the 20-source cap.
**Score reason**: Direct match on query + 221k views, 8 days old
**Tags**: `claude-code-mods`, `setup`, `video`

**[9] Claude Mods Is The Biggest Claude Code Upgrade Since Skills**
🔗 https://www.youtube.com/watch?v=Rn4nmFRPe0s
📅 2026-10-02 | ⭐ Authority: High | 📊 Score: 95/100
**Summary**: Chase AI positions mods relative to skills (9:11, 212,406 views). The earliest video in the set dated 2026-10-02.
**Score reason**: Direct match on query + 212k views, 8 days old
**Tags**: `claude-code-mods`, `skills`, `video`

**[10] Claude Mods Just Dropped... Use these 3 NOW**
🔗 https://www.youtube.com/watch?v=moOBIaIb4a8
📅 2026-10-02 | ⭐ Authority: High | 📊 Score: 95/100
**Summary**: Jack Roberts presents three mods and a prompt for finding the mods that fit a given workflow (9:00, 41,372 views).
**Score reason**: Direct match on query + 41k views, 8 days old
**Tags**: `claude-code-mods`, `showcase`, `video`

**[11] Claude Code vient de lancer les mods : voici mes 5 indispensables**
🔗 https://www.youtube.com/watch?v=1Dlh_Mqze1s
📅 2026-10-09 | ⭐ Authority: High | 📊 Score: 95/100
**Summary**: French-language video by Tony Lotis on five mods and a skill for creating your own (13:20, 7,526 views). The only non-English source; the mods themselves sit behind a community sign-up.
**Score reason**: Direct match on query + published yesterday
**Tags**: `claude-code-mods`, `french`, `video`

**[12] Anthropic Mods for Claude Code: Too Much Power?**
🔗 https://www.youtube.com/watch?v=xG9UIliOX3E
📅 2026-10-03 | ⭐ Authority: High | 📊 Score: 95/100
**Summary**: Stacked Podcast episode (26:15, 7,582 views) that questions how much power mods hand to extensions. Only part of the episode is on mods: the description also covers an unrelated robotics story.
**Score reason**: Direct match on query + long-form discussion published 7 days ago
**Tags**: `claude-code-mods`, `risk`, `podcast`

**[13] Claude Code Mods Are INSANE (Master it in 9 minutes)**
🔗 https://www.youtube.com/watch?v=oL6yb21XhDQ
📅 2026-10-08 | ⭐ Authority: High | 📊 Score: 95/100
**Summary**: Short overview by Shab Noor (8:59). Very low reach (359 views): it ranks here on freshness and on the grid's flat authority score for YouTube, not on audience signal.
**Score reason**: Direct match on query + published 2 days ago
**Tags**: `claude-code-mods`, `overview`, `video`

**[14] Mods in Claude Code: change how Claude Code works**
🔗 https://www.youtube.com/watch?v=yUuFvL1lK4k
📅 2026-10-05 | ⭐ Authority: High | 📊 Score: 94/100
**Summary**: The official video from the Claude channel (3:21, 371,304 views): mods are functions you write that change what Claude Code renders and what goes into a prompt. The only first-party source in the report; it loses points on length only, and should anchor the reading of everything else.
**Score reason**: Official first-party video with 371k views, direct match on query
**Tags**: `claude-code-mods`, `official`, `anthropic`

**[15] karanb192/awesome-claude-code-mods**
🔗 https://github.com/karanb192/awesome-claude-code-mods
📅 2026-10-10 (last push; created 2026-09-15) | ⭐ Authority: High | 📊 Score: 89/100
**Summary**: Community catalogue of public Claude Code mods (described as function hooks), scanned from GitHub, stating for each mod what it can read, write, run or send over the network; browsable at mods.aidojo.si. The most starred repository of the set (453) and the only one that documents capabilities per mod.
**Score reason**: Exact match on topic, pushed today, 453 stars
**Tags**: `catalogue`, `security`, `awesome-list`

**[16] hamzafer/claude-code-mods**
🔗 https://github.com/hamzafer/claude-code-mods
📅 2026-10-09 (last push; created 2026-10-02) | ⭐ Authority: High | 📊 Score: 89/100
**Summary**: Collection of mods described as plugins built on hooks: live lines above the prompt, guards, panes and games, including a context bar, usage meter, Codex review watch, Markdown preview and Spotify now playing. A concrete sample of the UI surface mods can occupy (176 stars).
**Score reason**: Exact match on topic, pushed yesterday, 176 stars
**Tags**: `mod-collection`, `typescript`, `ui`

**[17] JohnnyVizz/claude-kit**
🔗 https://github.com/JohnnyVizz/claude-kit
📅 2026-10-04 (last push; created 2026-10-04) | ⭐ Authority: High | 📊 Score: 89/100
**Summary**: Public Claude Code skills and mods (121 stars, TypeScript). The description gives no further detail, and the repository mixes mods with skills.
**Score reason**: Match on topic, pushed 6 days ago, 121 stars
**Tags**: `mod-collection`, `skills`, `typescript`

**[18] Tickloop/claude-mods**
🔗 https://github.com/Tickloop/claude-mods
📅 2026-10-08 (last push; created 2026-10-08) | ⭐ Authority: High | 📊 Score: 89/100
**Summary**: A collection of Claude Code mods (77 stars, TypeScript), created two days before this report. The description gives no detail on the individual mods.
**Score reason**: Exact match on topic, pushed 2 days ago
**Tags**: `mod-collection`, `typescript`

**[19] darrell-tw/darrelltw-mods**
🔗 https://github.com/darrell-tw/darrelltw-mods
📅 2026-10-05 (last push; created 2026-09-16) | ⭐ Authority: High | 📊 Score: 89/100
**Summary**: Mods by Darrell Wang that draw bands above the prompt with zero model tokens, starting with a Taiwan and US stock board (65 stars). Illustrates the "display without spending tokens" use of mods.
**Score reason**: Exact match on topic, pushed 5 days ago
**Tags**: `prompt-band`, `zero-token`, `mod-collection`

**[20] whyashthakker/awesome-claude-code-mods**
🔗 https://github.com/whyashthakker/awesome-claude-code-mods
📅 2026-10-03 (last push; created 2026-10-03) | ⭐ Authority: High | 📊 Score: 89/100
**Summary**: Collection of 100+ mods usable with Claude Code (43 stars). A second catalogue-style entry point alongside [15], without the per-mod capability information.
**Score reason**: Exact match on topic, pushed 7 days ago
**Tags**: `catalogue`, `awesome-list`, `typescript`

---

### 🟠 High value (score 70–84)

None listed: the 20-source cap was reached within the Essential band.

---

### 🟡 Worth including (score 60–69)

None listed: the 20-source cap was reached within the Essential band.

---

## Trends identified

- Launch-week saturation: 14 of the 15 videos were published between 2026-10-02 and 2026-10-09, most of them in a "N mods you need" format with the mods offered behind a community or newsletter sign-up. Only two (Build Great Products, Better Stack) lead with building or with the mechanism.
- Repositories converge on the same surfaces: bands or lines above the prompt, panes, status lines, usage and context meters, and tool-call guards recur across independent collections.
- Curation appeared almost immediately: three catalogue-type repositories exist (`karanb192/awesome-claude-code-mods`, `whyashthakker/awesome-claude-code-mods`, and `wh000wh000/awesome-claude-mods`, cut by the cap), two of them pushed on the day of this report.
- Trust in third-party mods is an early theme: one catalogue lists what each mod can read, write, run or send over the network, a knowledge-base repository covers "how to check one before you install it", and a podcast asks whether mods carry too much power. Web search results repeat a claim that mods are not sandboxed; no page was opened in this run, so that claim is unverified here.
- Activity predates the early-October wave: three repositories were created between 2026-09-14 and 2026-09-16 and a Firecrawl video dated 2026-09-18 calls mods a "hidden feature". No research paper matched the topic.

---

*Generated by tech-watch skill | Sources: arXiv · GitHub · YouTube · Web search*
*Scoring: Relevance 40% · Freshness 20% · Authority 20% · Depth 10% · Engagement 10%*
