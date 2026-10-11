# Tech Watch — Claude Code mods
**Date**: 2026-10-11 | **Window**: 30 days | **Request**: "Claude Mods" | **Owner**: Anthropic | **Sources**: 20 ranked + 3 primary

| Source | Status | Raw | On-topic | In report |
|---|---|---|---|---|
| arXiv | empty | 0 | 0 | 0 |
| GitHub | ok | 20 | 19 | 3 |
| YouTube | ok | 15 | 15 | 12 |
| Web (Tier 2) | ok | 28 | 23 | 5 |
| Web (Tier 3) | not run (unique on-topic ≥ 12) | – | – | 0 |
| Owner domains | ok | 10 | – | 3 |

**Pipeline**: 63 raw → 57 on-topic, 0 adjacent, 1 homonyms, 5 dropped → 55 unique → 39 ≥ 60 → 20 ranked (cap 20).
**Enrichment**: 10/10 pages opened (3 primary), 0 failures, 1 truncated.
**Date test**: skipped (the docs overview mentions an "early access" period without dating it; meaning test alone).
**Notes** (at most 5 bullets; omit the line if none):
- Cap cut: 39 sources reached 60, 19 were cut by the cap of 20. Cut: dev.to/bobbyhalljr (77), Gundeep Ai (75), Solo Swift Crafter (75), hamzafer/claude-code-mods (74), nine at 72 (whyashthakker, zycck, promptadvisers starter kit, nateherkai, AgriciDaniel, augiefra, OneWave-AI, arasovic repositories; dev.to/yong_yu), Firecrawl video (68), karanb192/awesome-claude-code-mods (64, 477 stars, the largest catalogue, penalized by its September creation date), JohnnyVizz/claude-kit (64), and three at 62. The tie at 77 for the last two slots between three web pages with no engagement signal was broken by length, which the grid does not prescribe.
- Unopened pages: 13 unique Tier 2 web pages were not opened (budget exhausted). They stay `unverified`, cap at 59 and are excluded, not judged poor: it-connect.fr, pasqualepillitteri.it, claudekit.io, braindetox.kr, onewave-ai.com, blog.laozhang.ai, mindstudio.ai, dev.to/max_quimby, and five Medium posts. Owner pages listed by the search but not opened: mods API, admin, interface, gallery, plugins overview, changelog.
- Scoring interpretations: the three dev.to pages show day and month only; the year 2026 was taken because their content postdates the 2026-10-01 launch. StationX states only "Updated October 2026" (freshness scored 15, not 20). Steve Kinney and Kanaries are scored on their last-modified date, no publication date being stated. Better Stack, StationX and Steve Kinney were rated B (identified organization or established educator); rated C they would score 82, 76 and 81 and stay in the ranking.
- Contradiction check: enrichment extracts date, length and author only, so secondary claims were compared with the primary sources on titles, tool descriptions and search snippets. None contradicted. The StationX page was read to 100,000 of 103,463 characters.
- Filter detail: 1 homonym by meaning test (0xDarkMatter/claude-mods, a 2025 collection of skills, agents and commands). 5 web results dropped for an unusable title (site name or navigation text). The two localized docs pages returned by Tier 2 (`/docs/it/`, `/docs/de/`) designate the English "Create a mod" page listed under Primary sources.

---

## Executive Summary
Anthropic launched mods for Claude Code on 2026-10-01: JavaScript or TypeScript event handlers, shipped as plugins, that run inside the Claude Code process and can redraw the interface, rewrite prompts and intercept tool calls. Within ten days the topic produced a wave of "N mods you need" creator videos, dozens of small community repositories and at least two automated catalogues, while no research paper covers it. The point the primary sources insist on, and that the better secondary sources repeat, is that mods are not sandboxed and run with the user's full permissions, which makes pre-install review (`claude plugin validate`) and organization-level controls the real subject behind the enthusiasm.

---

## Primary sources

**Customize Claude Code with mods in TypeScript** — 🔗 https://claude.com/blog/claude-code-mods — 📅 2026-10-01
Launch announcement by Anthropic: mods are "available today" in the Claude Code CLI and desktop app, are not sandboxed, and a built-in `sec-default` guard mod applies on Team and Enterprise plans and on machines with managed settings; source of built-in mods is in the `mods` folder of `anthropics/claude-code`. No preview period and no required version are stated in the post.

**Mods overview - Claude Code Docs** — 🔗 https://code.claude.com/docs/en/plugins/mods/overview — 📅 unverified
Reference for requirements and availability: mods are on by default, need Claude Code v2.1.287 or later in the terminal and v2.1.286 in the Desktop app; hooks run in every session type but drawing appears only in the terminal and the Desktop Code tab (not in the VS Code chat panel, `claude -p` or cloud sessions). Mentions an undated early-access period (`CLAUDE_CODE_ENABLE_FUNCTION_HOOKS`, now ignored), the sample mods in `anthropics/claude-code-playground` (`token-weather`, `blast-radius`, `replay-theater`) and the ways to turn mods off (`--safe-mode`, `disableAllHooks`).

**Create a mod - Claude Code Docs** — 🔗 https://code.claude.com/docs/en/plugins/mods/create — 📅 unverified
Official tutorial: ask Claude for a mod (built-in `plugin-authoring` skill, files written under `~/.claude/dev-mods/<session id>/`, hot reload after approval) or write one by hand (`plugin.json`, `hooks/hooks.json` with a `modules` key, `register.js`), then check it with `claude plugin validate` and `claude plugin test`. Requires v2.1.287 or later; no Node.js or build step.

---

## Sources ranked by score

---

### 🔴 Essential (score 85–100)

**[1] Mods in Claude Code: change how Claude Code works**
🔗 https://www.youtube.com/watch?v=yUuFvL1lK4k
📅 2026-10-05 | ⭐ Authority: A Primary | 📊 Score: 94/100
**Summary**: The official video from the Claude channel. It presents mods as functions you write that change what Claude Code renders, what goes into a prompt and how tool calls are handled. Short (3:21), it is the vendor's own framing of the feature.
**Score reason**: Exact match + A Primary (official channel), published 6 days ago, 382k views
**Tags**: `official`, `overview`, `video`

**[2] Claude Code Mods Can Do Basically Anything...**
🔗 https://www.youtube.com/watch?v=EiThSVZ8pME
📅 2026-10-04 | ⭐ Authority: B Expert | 📊 Score: 88/100
**Summary**: Better Stack's developer channel describes mods as small TypeScript plugins that run inside Claude Code to change its behavior and draw custom interface elements. A compact technical overview (7:37) from an engineering organization rather than a creator channel.
**Score reason**: Exact match + B Expert (engineering organization channel), published 7 days ago, 39k views
**Tags**: `overview`, `typescript`, `video`

**[3] Claude Code Mods (course page, AI development setup)**
🔗 https://stevekinney.com/courses/ai-development-setup/claude-code-mods
📅 2026-10-06 (last modified) | ⭐ Authority: B Expert | 📊 Score: 87/100
**Summary**: A course chapter of about 1,800 words by Steve Kinney on when a mod is the right tool and when a settings hook or a skill is enough. It is the ranked source most focused on the decision between mods, hooks, skills and MCP servers.
**Score reason**: Exact match + B Expert (established course author), last modified 5 days ago, about 1,800 words
**Tags**: `decision-guide`, `hooks-vs-mods`, `course`

**[4] 9 NEW Claude Mods that can truly change how you work**
🔗 https://www.youtube.com/watch?v=lDrAZ1wAyVs
📅 2026-10-08 | ⭐ Authority: C Community | 📊 Score: 85/100
**Summary**: A walkthrough of nine mods by Jay E (RoboNuggets), with a companion PDF guide. The most viewed video of the watch, and representative of the "list of mods to install" format that dominates the coverage.
**Score reason**: Exact match + C Community (YouTube creator), published 3 days ago, 502k views
**Tags**: `mod-list`, `workflow`, `video`

**[5] These Mods Take Claude Code to Another Level**
🔗 https://www.youtube.com/watch?v=UcvD53jqHRU
📅 2026-10-05 | ⭐ Authority: C Community | 📊 Score: 85/100
**Summary**: Mark Kashef demonstrates a set of mods and shares their code and build prompts (15:41). Useful for seeing mods built from prompts rather than installed ready-made.
**Score reason**: Exact match + C Community (YouTube creator), published 6 days ago, 39k views
**Tags**: `demo`, `build-prompts`, `video`

**[6] Claude Mods Are Insane... You Need To Try These Right Now**
🔗 https://www.youtube.com/watch?v=ERNqRK6sMJY
📅 2026-10-09 | ⭐ Authority: C Community | 📊 Score: 85/100
**Summary**: AI LABS presents seven Claude Code mods in 13:28. One of the most recent videos of the window; sponsored content in the description.
**Score reason**: Exact match + C Community (YouTube creator), published 2 days ago, 26k views
**Tags**: `mod-list`, `demo`, `video`

**[7] Claude Code Just Dropped Mods: Here Are 5 You Need**
🔗 https://www.youtube.com/watch?v=W5JSvXig3Ig
📅 2026-10-06 | ⭐ Authority: C Community | 📊 Score: 85/100
**Summary**: Sharbel A. covers five mods with their install commands and a custom mod-building prompt (11:33). Practical angle on installation through the plugin mechanism.
**Score reason**: Exact match + C Community (YouTube creator), published 5 days ago, 25k views
**Tags**: `mod-list`, `install`, `video`

**[8] Diese 10 Claude Code Mods solltest du unbedingt kennen**
🔗 https://www.youtube.com/watch?v=ji4ANdb_M6Y
📅 2026-10-10 | ⭐ Authority: C Community | 📊 Score: 85/100
**Summary**: German-language video by Julian Ivanov presenting ten mods (17:27), noting that mods exist since the beginning of October. The most recent source of the watch and a sign that the topic has spread beyond English-language channels.
**Score reason**: Exact match + C Community (YouTube creator), published 1 day ago, 17k views
**Tags**: `mod-list`, `german`, `video`

**[9] 3 Claude Code mods you need to build**
🔗 https://www.youtube.com/watch?v=WCwNECxFJ_Q
📅 2026-10-05 | ⭐ Authority: C Community | 📊 Score: 85/100
**Summary**: Build Great Products focuses on building three mods rather than installing existing ones (13:43), with a companion playbook. Complements the list-style videos with an authoring angle.
**Score reason**: Exact match + C Community (YouTube creator), published 6 days ago, 13k views
**Tags**: `authoring`, `demo`, `video`

**[10] Claude Code vient de lancer les mods : voici mes 5 indispensables**
🔗 https://www.youtube.com/watch?v=1Dlh_Mqze1s
📅 2026-10-09 | ⭐ Authority: C Community | 📊 Score: 85/100
**Summary**: French-language video by Tony Lotis on five mods and a skill for creating your own (13:20). The main French-language source returned for the topic.
**Score reason**: Exact match + C Community (YouTube creator), published 2 days ago, 12k views
**Tags**: `mod-list`, `french`, `video`

---

### 🟠 High value (score 70–84)

**[11] Claude Code Mods: The Ultimate Customization Guide**
🔗 https://www.youtube.com/watch?v=8wZVnc99x_k
📅 2026-10-08 | ⭐ Authority: C Community | 📊 Score: 82/100
**Summary**: Eric Tech explains what mods are and how they change the way Claude Code looks and works, "not just what it knows" (9:53). An explanatory video rather than a list.
**Score reason**: Exact match + C Community (YouTube creator), published 3 days ago, 13k views
**Tags**: `explainer`, `customization`, `video`

**[12] Claude Code Mods: The Complete Guide + 34 Videos (2026)**
🔗 https://app.stationx.net/articles/claude-code-mods
📅 2026-10 (updated; day unverified, page corrected on 2026-10-05) | ⭐ Authority: B Expert | 📊 Score: 82/100
**Summary**: A very long guide by Nathan House (StationX, security training) that cross-checks the official docs, 34 YouTube videos and the author's own mods, and states that it was fact-checked and corrected. Returned by two of the three Tier 2 searches; its security angle (unsandboxed code, validate before install) matches the primary sources.
**Score reason**: Exact match + B Expert (identified security training organization), updated October 2026, well over 1,500 words
**Tags**: `guide`, `security`, `fact-check`

**[13] Claude Code Mods Tutorial: Build and Test Your First Mod, Plus 15 Community Examples**
🔗 https://docs.kanaries.net/topics/AICoding/claude-code-mods
📅 2026-10-07 (last updated) | ⭐ Authority: C Community | 📊 Score: 81/100
**Summary**: A tutorial of about 5,000 words (Soren Atelier, Kanaries) covering building and testing a first mod, then fifteen community examples. One of the few written sources that covers testing as well as authoring.
**Score reason**: Exact match + C Community (vendor content page outside its field), updated 4 days ago, about 5,000 words
**Tags**: `tutorial`, `testing`, `community-examples`

**[14] Claude Code Mods Are Game Changers. Set Up These 5 NOW.**
🔗 https://www.youtube.com/watch?v=9hetShMMp2s
📅 2026-10-02 | ⭐ Authority: C Community | 📊 Score: 80/100
**Summary**: Nate Herk's video on five mods, published the day after the launch (11:19). Companion repository: https://github.com/nateherkai/claude-code-mods (Cache Keeper, Recording Mode, Goal Meter, Collision Guard), cut by the cap at 72.
**Score reason**: Exact match + C Community (YouTube creator), published 9 days ago, 226k views
**Tags**: `mod-list`, `companion-repo`, `video`

**[15] Claude Mods Is The Biggest Claude Code Upgrade Since Skills**
🔗 https://www.youtube.com/watch?v=Rn4nmFRPe0s
📅 2026-10-02 | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Chase AI's first-reaction video positioning mods relative to skills (9:11). One of the earliest and most viewed reactions to the launch.
**Score reason**: Exact match + C Community (YouTube creator), published 9 days ago, 213k views
**Tags**: `first-look`, `skills-vs-mods`, `video`

**[16] Tickloop/claude-mods**
🔗 https://github.com/Tickloop/claude-mods
📅 2026-10-08 (created) | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: A TypeScript collection of Claude Code mods created three days before this watch and already at 77 stars. A concrete code base to read alongside the official tutorial.
**Score reason**: Exact match + C Community repository created 3 days ago, 77 stars
**Tags**: `repository`, `typescript`, `mod-collection`

**[17] wh000wh000/awesome-claude-mods**
🔗 https://github.com/wh000wh000/awesome-claude-mods
📅 2026-10-04 (created) | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: An "evidence-graded" index of Claude Code mods, plugins and hooks, published in 20 languages and rebuilt every two hours according to its description. Shows the catalogue layer forming around the feature.
**Score reason**: Exact match + C Community repository created 7 days ago, 47 stars
**Tags**: `repository`, `catalogue`, `index`

**[18] promptadvisers/claude-mods-computer-use-threads**
🔗 https://github.com/promptadvisers/claude-mods-computer-use-threads
📅 2026-10-05 (created) | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: Two mods with source, build prompts, setup and tests: a Codex computer-use bridge and coordinated Claude sessions. Companion repository from the same organization: https://github.com/promptadvisers/claude-mods-starter-kit (ten beginner mods and a template), cut by the cap at 72.
**Score reason**: Exact match + C Community repository created 6 days ago, 11 stars
**Tags**: `repository`, `multi-session`, `tests`

**[19] I Built Mods for Claude. Here's What Happened**
🔗 https://nandigamharikrishna.substack.com/p/i-built-mods-for-claude-heres-what
📅 2026-10-06 | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: A first-hand account of about 1,500 words by Hari Krishna ("Tech in General" Substack) on building mods. A practitioner report rather than a restatement of the announcement.
**Score reason**: Exact match + C Community (Substack post), published 5 days ago, about 1,500 words
**Tags**: `experience-report`, `authoring`, `substack`

**[20] What are Claude Code mods? What they can draw and where they run in the desktop app**
🔗 https://dev.to/nakadadev/what-are-claude-code-mods-what-they-can-draw-and-where-they-run-in-the-desktop-app-58pc
📅 2026-10-06 | ⭐ Authority: C Community | 📊 Score: 77/100
**Summary**: A post of about 1,300 words by Haruki Nakada on what mods can draw and how they behave in the Desktop app. The author also runs the modscode.com gallery, so the post carries a stake in the ecosystem.
**Score reason**: Exact match + C Community (dev.to post), published 5 days ago, about 1,300 words
**Tags**: `desktop-app`, `interface`, `dev.to`

---

### 🟡 Worth including (score 60–69)

No source in this band made the ranking: the cap of 20 was reached at 77 (see Notes for the sources cut).

---

## Trends identified

- Creator video is the dominant channel: 12 of the 20 ranked sources are YouTube videos, most of them "N mods you need" lists published within nine days of the launch, in English, German and French, several above 200k views.
- Security is the common thread of the serious sources: both primary pages state that mods are not sandboxed and run with the user's permissions, and the guides and catalogues that add value do so around review before install (`claude plugin validate`, capability scans, "evidence-graded" indexes).
- The repository landscape is wide and shallow: 19 on-topic repositories in the window, most created between 2026-10-02 and 2026-10-08 with under 200 stars, and the recurring use case is a band above the prompt (context, usage limits, cost, plan progress).
- Mods are mostly built by asking Claude: the official tutorial leads with "Ask Claude for a mod" and creators distribute build prompts and builder skills alongside, or instead of, source code.
- Activity predates the announcement: three repositories and one video date from mid-September 2026, consistent with the early-access period the documentation mentions without dating; research coverage is absent (0 arXiv papers).

---

*Generated by tech-watch skill | Sources used: GitHub · YouTube · Web (Tier 2) · Owner domains*
*Scoring: Relevance 40% · Freshness 20% · Authority 20% · Depth 10% · Engagement 10%*
