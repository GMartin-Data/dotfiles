# Tech Watch — AI agent evaluation
**Date**: 2026-10-11 | **Window**: 30 days | **Request**: "AI agent evaluation" | **Owner**: unknown | **Sources**: 20 ranked + 0 primary

| Source | Status | Raw | On-topic | In report |
|---|---|---|---|---|
| arXiv | ok | 20 | 15 | 13 |
| GitHub | ok | 20 | 14 | 4 |
| YouTube | ok | 15 | 9 | 3 |
| Web (Tier 2) | ok | 28 | 26 | 0 |
| Web (Tier 3) | not run (unique on-topic ≥ 12) | – | – | 0 |
| Owner domains | not run (no single owner: the discovery search `AI agent evaluation official documentation OR announcement` returned 10 pages from unrelated vendors, no owner domain to restrict to) | – | – | 0 |

**Pipeline**: 83 raw → 64 on-topic, 14 adjacent, 0 homonyms, 5 dropped → 60 unique → 44 ≥ 60 → 20 ranked (cap 20).
**Enrichment**: 10/10 pages opened (0 primary), 1 failures, 0 truncated.
**Date test**: not applicable.
**Notes**:
- Cap cut: 24 sources scoring ≥ 60 are not listed. Five tied at 72 for the last two places with no engagement signal to separate them; exact relevance, then a verified date, was used as an extra tie-break. Cut at 72: arXiv 2610.11015 (voice user simulators), Langfuse "AI agent evaluation" guide (https://langfuse.com/resources/engineering/ai-agent-evaluation, date unverified), Mercor "How to evaluate AI agents" (https://www.mercor.com/resources/apex/how-to-evaluate-ai-agents/, only an "Updated On: Sep 16, 2026" date found). No web page made the top 20.
- Web: 10 of the 22 unique web candidates stay `unverified` and are excluded, not judged poor: 9 were not opened (budget exhausted) and 1 fetch failed (sendbird.com answered with a 301 to delight.ai, not followed: no retry).
- Opened web pages with no publication date on the page (Langfuse, IBM Think, Mercor, dev.to "Posted on Jul 2" without a year) were scored with freshness `unverified` = 5. Reading times ("13 min read", "16 min read") were not accepted as a length: those pages got the `unverified` depth and fell below 60.
- All 14 on-topic repositories were created before the window: freshness is the last push date, capped at 10. Authority B was given only to repositories of an identified organization (NVIDIA, ServiceNow, strands-agents, Microsoft, IBM); the others are C.
- arXiv summaries rely on the title and the truncated abstract returned by the tool; papers were not opened. Paper [14] uses "agent evaluation" in a game-theoretic sense (offline feedback, equilibrium learning) and may be further from LLM agent evals than its title suggests.

---

## Executive Summary
The dominant theme of the last 30 days is not new benchmarks but distrust of existing ones: most of the research output questions whether agent scores are earned, reproducible and comparable, pointing at LLM-judge error, verifier brittleness, scaffold effects and ambiguous task policies. On the practitioner side, talks and tooling converge on trajectory-level evaluation (tool calls and execution path, not only the final answer) and on evals as release gates. Unexpected: no vendor or standards body owns the topic, and several papers independently propose a "layer" above raw scores (trust, semantics, certification) rather than better metrics.

---

## Primary sources

No primary source found for this topic. "AI agent evaluation" is a practice, not a product: the discovery search (`AI agent evaluation official documentation OR announcement`) returned documentation from unrelated vendors (AWS Bedrock AgentCore, Automation Anywhere, PraisonAI, Maxim, Relevance AI) and no single owner, so no owner-restricted search was run. Without a primary source, no secondary source was judged contradictory.

---

## Sources ranked by score

---

### 🔴 Essential (score 85–100)

**[1] From Vibes to Production: Evaluating and Shipping AI Agents That Work 101 — Laurie Voss, Arize AI**
🔗 https://www.youtube.com/watch?v=qZj7sqmidqA
📅 2026-10-05 | ⭐ Authority: B Expert | 📊 Score: 94/100
**Summary**: A 1h51 workshop on the AI Engineer channel. It starts from a concrete failure: an LLM correctness judge rejects all 13 reports of a financial analysis agent, and the talk examines why. The longest practitioner source of the watch on going from informal checks to production evals.
**Score reason**: Exact match + B Expert (conference talk), published 6 days ago, 13,869 views
**Tags**: `llm-as-judge`, `production-evals`, `workshop`

**[2] Why Your AI Agent Fails in Production (And How to Catch It)**
🔗 https://www.youtube.com/watch?v=wPdoZRbvaF4
📅 2026-09-30 | ⭐ Authority: B Expert | 📊 Score: 89/100
**Summary**: A 26-minute Google Cloud Tech episode arguing that manual tweaking is not a testing strategy and showing how to evaluate agents for production. A vendor view of a structured evaluation workflow. The channel also published a 55-second companion clip ("How to build AI agent evals in 4 steps"), dropped as a Short.
**Score reason**: Exact match + B Expert (vendor channel, not topic owner), published 11 days ago, 18,942 views
**Tags**: `production-evals`, `google-cloud`, `testing-strategy`

**[3] A Trust Layer for Agent Evaluation**
🔗 https://arxiv.org/abs/2610.07274v1
📅 2026-10-05 | ⭐ Authority: B Expert | 📊 Score: 87/100
**Summary**: Argues that deterministic benchmark scores show an agent received credit, but not whether the credit was earned, reported honestly, or would hold on a second run. Introduces a trust layer on top of agent evaluation to address those three gaps.
**Score reason**: Exact match + B Expert (arXiv paper), published 6 days ago
**Tags**: `benchmark-integrity`, `reproducibility`, `trust`

**[4] EIO-Agents: The Missing Semantic Layer for AI Agent Evaluation**
🔗 https://arxiv.org/abs/2610.07675v1
📅 2026-10-06 | ⭐ Authority: B Expert | 📊 Score: 87/100
**Summary**: States that agents reach production without a shared semantic standard for what their evaluations mean: scores, traces and judge outputs are not comparable across tools. Proposes a semantic layer for agent evaluation artifacts.
**Score reason**: Exact match + B Expert (arXiv paper), published 5 days ago
**Tags**: `standardization`, `semantics`, `interoperability`

**[5] TRACE: Diagnosing Verifier Brittleness in Agentic Evaluation**
🔗 https://arxiv.org/abs/2610.11678v1
📅 2026-10-08 | ⭐ Authority: B Expert | 📊 Score: 87/100
**Summary**: Verifier scores serve both as benchmark metrics and as training rewards for LLM agents, and a score change is routinely read as a capability change. The paper studies when it instead reflects the verifier's own brittleness.
**Score reason**: Exact match + B Expert (arXiv paper), published 3 days ago
**Tags**: `verifiers`, `benchmark-validity`, `diagnostics`

**[6] Transect: Retaining Observability for Long-Horizon LLM Agent Evaluations**
🔗 https://arxiv.org/abs/2610.08364v2
📅 2026-10-06 | ⭐ Authority: B Expert | 📊 Score: 87/100
**Summary**: Frontier evaluations increasingly use open-ended, long-horizon tasks whose transcripts span hundreds of pages across multi-agent networks. The paper addresses how to keep such evaluations observable for the humans who must review them.
**Score reason**: Exact match + B Expert (arXiv paper), published 5 days ago
**Tags**: `long-horizon`, `observability`, `transcripts`

---

### 🟠 High value (score 70–84)

**[7] Certified Selective Automation of LLM Agent Evaluation**
🔗 https://arxiv.org/abs/2609.34320v1
📅 2026-09-28 | ⭐ Authority: B Expert | 📊 Score: 82/100
**Summary**: Agent evaluation still ends with a human reading trajectories because automatic judges carry no guarantee on their error rate. The paper asks what fraction of agent evaluation can be automated with a certified bound.
**Score reason**: Exact match + B Expert (arXiv paper), published 13 days ago
**Tags**: `llm-as-judge`, `human-review`, `guarantees`

**[8] Agent Evaluation Reliability: More Tasks Won't (Always) Fix An Agent Leaderboard**
🔗 https://arxiv.org/abs/2610.00651v1
📅 2026-09-30 | ⭐ Authority: B Expert | 📊 Score: 82/100
**Summary**: Shows that leaderboard ranks can reflect evaluation conditions such as the scaffold, not only the model, so that adding tasks does not necessarily make a ranking reliable. Directly relevant to anyone using agent leaderboards for deployment decisions.
**Score reason**: Exact match + B Expert (arXiv paper), published 11 days ago
**Tags**: `leaderboards`, `reliability`, `scaffold-effects`

**[9] Agents Are Systems, Not Models: Rethinking Agentic Evaluation**
🔗 https://arxiv.org/abs/2610.01618v1
📅 2026-10-01 | ⭐ Authority: B Expert | 📊 Score: 82/100
**Summary**: Evaluations now report cost, consistency and robustness beyond a success rate, but still treat the agent as a fixed object. The paper argues an agent is a system of components and that evaluation should be rethought accordingly.
**Score reason**: Exact match + B Expert (arXiv paper), published 10 days ago
**Tags**: `system-level-evaluation`, `methodology`, `position-paper`

**[10] Measurement Boundaries in LLM Financial Agent Evaluation: Fixed-Tape Execution and Multi-Defect Auditing**
🔗 https://arxiv.org/abs/2609.32379v1
📅 2026-09-26 | ⭐ Authority: B Expert | 📊 Score: 82/100
**Summary**: Asks which controls are needed to interpret execution performance and audit scores in agent evaluations, through two studies on a financial agent harness. A domain case study on the limits of what a score can support.
**Score reason**: Exact match + B Expert (arXiv paper), published 15 days ago
**Tags**: `finance`, `auditing`, `measurement-validity`

**[11] Auditing Web Agent Evaluation on WebArena-Lite: Human Review of Outcomes and Trajectories**
🔗 https://arxiv.org/abs/2610.01491v1
📅 2026-10-01 | ⭐ Authority: B Expert | 📊 Score: 82/100
**Summary**: Web agent evaluation often relies on rule-based or LLM evaluators that inspect only the final outcome. The paper audits this on WebArena-Lite with human review of both outcomes and trajectories. Shares its first author with [7].
**Score reason**: Exact match + B Expert (arXiv paper), published 10 days ago
**Tags**: `web-agents`, `webarena`, `human-audit`

**[12] Frozen Judges, Moving Agents: Version-Dependent LLM-Judge Error and the Limits of Judge-Assisted Agent Evaluation**
🔗 https://arxiv.org/abs/2609.34198v2
📅 2026-09-28 | ⭐ Authority: B Expert | 📊 Score: 82/100
**Summary**: A fixed LLM judge can make mistakes that depend on the version of the agent it grades, which biases upgrade comparisons. The analysis covers 35 public coding-agent submissions.
**Score reason**: Exact match + B Expert (arXiv paper), published 13 days ago
**Tags**: `llm-as-judge`, `coding-agents`, `regression-testing`

**[13] NVIDIA/SkillEvaluator**
🔗 https://github.com/NVIDIA/SkillEvaluator
📅 created 2026-06-24, last push 2026-10-10 | ⭐ Authority: B Expert | 📊 Score: 80/100
**Summary**: A multi-tier framework for evaluating agent skills: quality gates, semantic overlap detection, synthetic evaluation dataset generation, and live evaluation measuring how a skill changes agent behavior. Shifts the unit of evaluation from the agent to the skill.
**Score reason**: Exact match + B Expert (NVIDIA organization), pushed 1 day ago (freshness capped at 10), 556 stars
**Tags**: `agent-skills`, `quality-gates`, `synthetic-datasets`

**[14] Context-dependent agent evaluation with orthogonal equilibrium learning**
🔗 https://arxiv.org/abs/2609.31897v1
📅 2026-09-25 | ⭐ Authority: B Expert | 📊 Score: 77/100
**Summary**: Studies how to evaluate agents under contextual information (a prompt, a task, a user group) from offline feedback. More theoretical than the rest of the ranking; see the last header note on its scope.
**Score reason**: Exact match + B Expert (arXiv paper), published 16 days ago
**Tags**: `offline-evaluation`, `context-dependent`, `theory`

**[15] strands-agents/evals**
🔗 https://github.com/strands-agents/evals
📅 created 2025-07-31, last push 2026-10-08 | ⭐ Authority: B Expert | 📊 Score: 75/100
**Summary**: An evaluation framework for AI agents and LLM applications, maintained under the strands-agents organization alongside its agent SDK. An example of evaluation shipped as a first-party companion of an agent framework.
**Score reason**: Exact match + B Expert (maintainer of a related project), pushed 3 days ago (freshness capped at 10), 235 stars
**Tags**: `evaluation-framework`, `python`, `strands`

**[16] ServiceNow/eva**
🔗 https://github.com/ServiceNow/eva
📅 created 2026-03-24, last push 2026-10-06 | ⭐ Authority: B Expert | 📊 Score: 75/100
**Summary**: An end-to-end framework for evaluating voice agents. Covers a modality where text-only evaluation harnesses do not apply.
**Score reason**: Exact match + B Expert (ServiceNow organization), pushed 5 days ago (freshness capped at 10), 227 stars
**Tags**: `voice-agents`, `end-to-end`, `evaluation-framework`

**[17] Production AI Agents 09 · Read an agent evaluation: paired cases, missing outcomes, release gates**
🔗 https://www.youtube.com/watch?v=pWhDOzYzyrY
📅 2026-10-07 | ⭐ Authority: C Community | 📊 Score: 75/100
**Summary**: Lesson 9 of a "Production AI Agents" course (7 min). Compares two agent releases on the same twelve synthetic cases and shows how to read the result: paired cases, missing outcomes, release gates.
**Score reason**: Exact match + C Community (YouTube creator), published 4 days ago, 50 views
**Tags**: `release-gates`, `paired-comparison`, `course`

**[18] harbor-framework/harbor**
🔗 https://github.com/harbor-framework/harbor
📅 created 2025-08-04, last push 2026-10-11 | ⭐ Authority: C Community | 📊 Score: 74/100
**Summary**: A framework for evaluating and improving agents, tagged `evals`, `rl-environments` and `terminal-bench`. The most starred on-topic repository of the watch and still pushed to on the day of the report.
**Score reason**: Exact match + C Community repository, 5,988 stars, pushed today (freshness capped at 10)
**Tags**: `evals`, `rl-environments`, `terminal-bench`

**[19] Skill-based Agentic Evaluation for Real-time Data Science Tasks**
🔗 https://arxiv.org/abs/2609.16487v1
📅 2026-09-15 | ⭐ Authority: B Expert | 📊 Score: 72/100
**Summary**: A framework for evaluating data-science agents on live, continuously updated data, using executable ground truth and format-agnostic factoid scoring. Addresses evaluation when the correct answer changes over time.
**Score reason**: Exact match + B Expert (arXiv paper), published 26 days ago
**Tags**: `data-science-agents`, `live-data`, `executable-ground-truth`

**[20] Policy Loopholes in Agent Evaluation: When Policy Ambiguity Masquerades as Agent Error**
🔗 https://arxiv.org/abs/2609.14400v1
📅 2026-09-13 | ⭐ Authority: B Expert | 📊 Score: 72/100
**Summary**: Agent benchmarks that test policy compliance assume each policy determines a unique correct action. The paper shows natural-language policies violate this through silence, ambiguity or contradiction, so that some recorded agent errors are benchmark errors.
**Score reason**: Exact match + B Expert (arXiv paper), published 28 days ago
**Tags**: `policy-compliance`, `benchmark-validity`, `ambiguity`

---

### 🟡 Worth including (score 60–69)

None listed: every source in this band was cut by the cap of 20 (see Notes).

---

## Adjacent, not ranked

- **mozilla-ai/any-agent** — https://github.com/mozilla-ai/any-agent — a single interface over agent frameworks; evaluation is a feature, the object is the framework abstraction.
- **JuryFlow: Disagreement-Guided Human-in-the-Loop Multi-Agent Evaluation** — https://arxiv.org/abs/2609.40103v1 — multi-agent LLM judging of AI-generated content, not evaluation of agents.
- **How to Choose an LLM for AI Agents: Evaluation, Cost & Reliability** — https://www.youtube.com/watch?v=GT1dRSU9tAU — model selection for agents; evaluation is the means, not the subject.

---

## Trends identified

- Research is auditing the evaluators rather than the agents: at least six of the thirteen ranked papers ([5], [7], [8], [11], [12], [20]) show a score moving for reasons other than agent capability (judge version, verifier brittleness, scaffold, policy ambiguity).
- LLM-as-judge is treated as necessary but unreliable on both sides: papers quantify or bound its error ([7], [12]) and the leading practitioner talk opens on a judge rejecting every output ([1]).
- Several independent proposals add a layer above raw scores (trust [3], semantics [4], certification [7], observability [6]), which suggests the field lacks a shared standard for what an agent evaluation result means.
- Tooling is specializing by unit and modality: skills (NVIDIA [13]), voice (ServiceNow [16]), live data-science tasks ([19]), next to general harnesses ([15], [18]).
- Practitioner content frames evaluation as a release process (paired cases, release gates, production failures: [1], [2], [17]) and consistently asks for trajectory-level checks instead of final-answer checks.

---

*Generated by tech-watch skill | Sources used: arXiv · GitHub · YouTube*
*Scoring: Relevance 40% · Freshness 20% · Authority 20% · Depth 10% · Engagement 10%*
