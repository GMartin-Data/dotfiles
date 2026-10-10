# Tech Watch — AI agent evaluation
**Date**: 2026-10-10 | **Window**: 60 days | **Sources**: 20

**Pipeline counts**: 84 raw results (arXiv 20, GitHub 20, YouTube 15, web 29) | 8 dropped unlabeled (7 videos under 3 min, 1 result without a usable title) | 67 on-topic, 9 adjacent, 0 off-topic | 61 unique on-topic after deduplication | Tier 3 not run (61 >= 12)
**Enrichment**: 10 of 10 WebFetch used, 2 failures (sendbird.com: cross-host redirect; kunalganglani.com: HTTP 404), both left `unverified`
**Coverage note**: about 45 sources reach the 60 threshold; the list is capped at the 20 highest scores. Ties at the cap (score 75) were broken by engagement. No primary source was opened, so no contradiction check could be applied.
**Reading note**: summaries are based on titles, abstracts and descriptions returned by the search tools; Tier 1 sources were not opened (by design).

---

## Executive Summary
Over the last 60 days the centre of gravity of agent evaluation has moved from "which benchmark, which score" to "can the score be trusted": the bulk of the new research audits the measurement itself (LLM-judge error, reward integrity of the harness, leaderboard reliability, evidence sufficiency) rather than proposing new tasks. In parallel, practitioner content from large vendors and conference talks converges on trajectory-level evaluation and on release gating for production agents. The unexpected finding is how many independent proposals target a shared standard or semantic layer for evaluation results (trust layer, EIO-Agents, Evaluation Context Protocol), which signals that no such standard exists yet.

---

## Primary sources

No primary source found for this topic. "AI agent evaluation" is a practice, not a product or specification: it has no single vendor, maintainer or standards body. The discovery search `AI agent evaluation official documentation OR announcement` returned only vendor documentation for individual products (for example Amazon Bedrock AgentCore Evaluations, Maxim AI, NiCE Cognigy), each of which owns its product but not the topic, plus blog posts and a glossary. No domain-restricted primary search was therefore run, and no source is rated A Primary in the ranking.

---

## Sources ranked by score

---

### 🔴 Essential (score 85–100)

**[1] Why Your AI Agent Fails in Production (And How to Catch It)**
🔗 https://www.youtube.com/watch?v=wPdoZRbvaF4
📅 2026-09-30 | ⭐ Authority: B Expert | 📊 Score: 94/100
**Summary**: Google Cloud Tech episode (26 min) on how to evaluate AI agents for production, starting from the premise that manual tweaking is not a testing strategy. Useful as a vendor-side view of a structured evaluation workflow.
**Score reason**: Exact match + B Expert (Google Cloud Tech channel), published 10 days ago, 18.7k views
**Tags**: `production-evals`, `video`, `google-cloud`

**[2] From Vibes to Production: Evaluating and Shipping AI Agents That Work 101 — Laurie Voss, Arize AI**
🔗 https://www.youtube.com/watch?v=qZj7sqmidqA
📅 2026-10-05 | ⭐ Authority: B Expert | 📊 Score: 94/100
**Summary**: Workshop-length talk (1h51) on the AI Engineer channel. It opens on a concrete failure: an LLM correctness judge rejecting all 13 reports of a financial analysis agent, and investigates why. Directly about building and debugging agent evals.
**Score reason**: Exact match + B Expert (conference talk), published 5 days ago, 12.8k views
**Tags**: `llm-as-judge`, `workshop`, `production-evals`

**[3] A Trust Layer for Agent Evaluation**
🔗 https://arxiv.org/abs/2610.07274v1
📅 2026-10-05 | ⭐ Authority: B Expert | 📊 Score: 87/100
**Summary**: Argues that deterministic benchmark scores show an agent received credit, but not whether the credit was earned, honestly reported, or reproducible on a second run. Introduces a trust layer on top of agent evaluation to address this.
**Score reason**: Exact match + B Expert (arXiv paper), published 5 days ago
**Tags**: `eval-integrity`, `reproducibility`, `arxiv`

**[4] EIO-Agents: The Missing Semantic Layer for AI Agent Evaluation**
🔗 https://arxiv.org/abs/2610.07675v1
📅 2026-10-06 | ⭐ Authority: B Expert | 📊 Score: 87/100
**Summary**: Starts from the lack of a shared semantic standard for what agent evaluations mean (scores, traces, judge outputs) as agents enter consequential production environments. Proposes a semantic layer for evaluation artifacts.
**Score reason**: Exact match + B Expert (arXiv paper), published 4 days ago
**Tags**: `standardization`, `semantic-layer`, `arxiv`

**[5] Agent Evaluation Reliability: More Tasks Won't (Always) Fix An Agent Leaderboard**
🔗 https://arxiv.org/abs/2610.00651v1
📅 2026-09-30 | ⭐ Authority: B Expert | 📊 Score: 87/100
**Summary**: Shows that leaderboard ranks can reflect the evaluation conditions, such as the scaffold, and not only the model. Questions the assumption that adding tasks is enough to make an agent leaderboard reliable.
**Score reason**: Exact match + B Expert (arXiv paper), published 10 days ago
**Tags**: `leaderboards`, `reliability`, `arxiv`

**[6] Agents Are Systems, Not Models: Rethinking Agentic Evaluation**
🔗 https://arxiv.org/abs/2610.01618v1
📅 2026-10-01 | ⭐ Authority: B Expert | 📊 Score: 87/100
**Summary**: Notes that evaluations now report cost, consistency and robustness beyond a single success rate, yet still treat the agent as fixed. Argues for evaluating the agent as a system rather than as a model.
**Score reason**: Exact match + B Expert (arXiv paper), published 9 days ago
**Tags**: `system-level-eval`, `methodology`, `arxiv`

**[7] Auditing Web Agent Evaluation on WebArena-Lite: Human Review of Outcomes and Trajectories**
🔗 https://arxiv.org/abs/2610.01491v1
📅 2026-10-01 | ⭐ Authority: B Expert | 📊 Score: 87/100
**Summary**: Human audit of web-agent evaluation, motivated by rule-based and LLM evaluators that only inspect the final outcome. Reviews both outcomes and trajectories on WebArena-Lite.
**Score reason**: Exact match + B Expert (arXiv paper), published 9 days ago
**Tags**: `web-agents`, `human-audit`, `trajectory`

**[8] Certified Selective Automation of LLM Agent Evaluation**
🔗 https://arxiv.org/abs/2609.34320v1
📅 2026-09-28 | ⭐ Authority: B Expert | 📊 Score: 87/100
**Summary**: Addresses the fact that agent evaluation still ends with a human reading trajectories because automatic judges carry no guarantee on their error rate. Asks what fraction of agent evaluation can be automated with a certificate.
**Score reason**: Exact match + B Expert (arXiv paper), published 12 days ago
**Tags**: `llm-as-judge`, `guarantees`, `arxiv`

**[9] Frozen Judges, Moving Agents: Version-Dependent LLM-Judge Error and the Limits of Judge-Assisted Agent Evaluation**
🔗 https://arxiv.org/abs/2609.34198v2
📅 2026-09-28 | ⭐ Authority: B Expert | 📊 Score: 87/100
**Summary**: Shows that a fixed LLM judge can make version-dependent mistakes when comparing an agent upgrade to its predecessor. Based on an analysis of 35 public coding-agent submissions.
**Score reason**: Exact match + B Expert (arXiv paper), published 12 days ago
**Tags**: `llm-as-judge`, `coding-agents`, `regression`

**[10] Measurement Boundaries in LLM Financial Agent Evaluation: Fixed-Tape Execution and Multi-Defect Auditing**
🔗 https://arxiv.org/abs/2609.32379v1
📅 2026-09-26 | ⭐ Authority: B Expert | 📊 Score: 87/100
**Summary**: Studies which controls are needed to interpret execution performance and audit scores in agent evaluations, using a financial agent harness. A domain case study of the limits of what an evaluation score can support.
**Score reason**: Exact match + B Expert (arXiv paper), published 14 days ago
**Tags**: `financial-agents`, `measurement`, `arxiv`

---

### 🟠 High value (score 70–84)

**[11] BenchShield: Formal Model-Backed Instrumentation for Reward Integrity in LLM-Agent Evaluation Infrastructure**
🔗 https://arxiv.org/abs/2609.11028v1
📅 2026-09-10 | ⭐ Authority: B Expert | 📊 Score: 82/100
**Summary**: Treats agent benchmarks as interactive infrastructure in which agents observe state, call tools, modify workspaces and receive rewards. Proposes formal-model-backed instrumentation to protect the integrity of those rewards.
**Score reason**: Exact match + B Expert (arXiv paper), published 30 days ago
**Tags**: `reward-integrity`, `benchmark-security`, `arxiv`

**[12] How to evaluate AI agents: A complete guide**
🔗 https://www.mercor.com/resources/apex/how-to-evaluate-ai-agents/
📅 2026-09-16 (page "Updated On"; no separate publication date shown) | ⭐ Authority: B Expert | 📊 Score: 82/100
**Summary**: Long-form guide (about 6,000 words, estimated) covering frameworks, metrics, repeated testing and failure analysis. Stresses repeated runs because agent behavior varies between attempts.
**Score reason**: Exact match + B Expert (Mercor, identified organization), updated 24 days ago, long-form
**Tags**: `guide`, `metrics`, `repeated-runs`

**[13] harbor-framework/harbor**
🔗 https://github.com/harbor-framework/harbor
📅 Created 2025-08-04, last push 2026-10-10 | ⭐ Authority: B Expert | 📊 Score: 80/100
**Summary**: Framework for evaluating and improving agents, tagged `evals`, `rl-environments`, `terminal-bench`. The most-starred evaluation harness in the results, and the infrastructure behind the Harbor Adapters paper listed below.
**Score reason**: Exact match + B Expert (maintainer organization of a related benchmark project), 5,978 stars; freshness capped (repository predates the window)
**Tags**: `harness`, `terminal-bench`, `github`

**[14] sunblaze-ucb/cybergym**
🔗 https://github.com/sunblaze-ucb/cybergym
📅 Created 2025-06-02, last push 2026-08-28 | ⭐ Authority: B Expert | 📊 Score: 80/100
**Summary**: Large-scale cybersecurity evaluation framework assessing AI agents on real-world vulnerability analysis tasks. A domain-specific benchmark from an identified research group.
**Score reason**: Exact match + B Expert (research group), 945 stars; freshness capped (repository predates the window)
**Tags**: `cybersecurity`, `benchmark`, `github`

**[15] NVIDIA/SkillEvaluator**
🔗 https://github.com/NVIDIA/SkillEvaluator
📅 Created 2026-06-24, last push 2026-10-10 | ⭐ Authority: B Expert | 📊 Score: 80/100
**Summary**: Multi-tier framework for evaluating agent skills: quality gates, semantic overlap detection, synthetic evaluation dataset generation and live agent evaluation measuring how skills change agent behavior. Extends agent evaluation to the skill layer.
**Score reason**: Exact match + B Expert (NVIDIA), 555 stars; freshness capped (created 108 days ago, outside the window)
**Tags**: `agent-skills`, `quality-gates`, `github`

**[16] ClaimReceipt: Verifying Evidence Sufficiency and Coverage in Agent Evaluations**
🔗 https://arxiv.org/abs/2609.01992v1
📅 2026-09-02 | ⭐ Authority: B Expert | 📊 Score: 77/100
**Summary**: Separates two evidentiary questions in agent evaluations: whether a reported claim can be recomputed from retained evidence, and whether retained records cover the committed experiment. Targets verifiability of reported results.
**Score reason**: Exact match + B Expert (arXiv paper), published 38 days ago
**Tags**: `eval-integrity`, `evidence`, `arxiv`

**[17] Harbor Adapters and Harbor-Index: Infrastructure and a Curated Meta-Dataset for Large-Scale Agentic Evaluation**
🔗 https://arxiv.org/abs/2609.04298v3
📅 2026-09-03 | ⭐ Authority: B Expert | 📊 Score: 77/100
**Summary**: Introduces Harbor Adapters, a unified evaluation infrastructure, to cope with the growing number of agentic benchmarks that each need complex environments and agent integrations. Pairs it with a curated meta-dataset.
**Score reason**: Exact match + B Expert (arXiv paper), published 37 days ago
**Tags**: `harness`, `meta-benchmark`, `arxiv`

**[18] EarlyEval: Cheaper Agent Evaluation via Early Outcome Prediction**
🔗 https://arxiv.org/abs/2609.02783v1
📅 2026-09-02 | ⭐ Authority: B Expert | 📊 Score: 77/100
**Summary**: Targets the cost of agent evaluation, where one pass of a frontier model over an agentic benchmark can cost hundreds to thousands of dollars. Proposes predicting outcomes early to cut that cost.
**Score reason**: Exact match + B Expert (arXiv paper), published 38 days ago
**Tags**: `eval-cost`, `early-stopping`, `arxiv`

**[19] Disclosure-Gated User Simulation for Companion-Agent Evaluation**
🔗 https://arxiv.org/abs/2609.00982v1
📅 2026-09-01 | ⭐ Authority: B Expert | 📊 Score: 77/100
**Summary**: Addresses a known failure of LLM-played users in scalable evaluation: the simulated user is too cooperative, which flatters the system under test. Proposes disclosure-gated simulation for companion agents.
**Score reason**: Exact match + B Expert (arXiv paper), published 39 days ago
**Tags**: `user-simulation`, `conversational-agents`, `arxiv`

**[20] strands-agents/evals**
🔗 https://github.com/strands-agents/evals
📅 Created 2025-07-31, last push 2026-10-08 | ⭐ Authority: B Expert | 📊 Score: 75/100
**Summary**: Evaluation framework for AI agents and LLM applications, maintained alongside the Strands Agents project. Representative of evaluation shipping as a first-class companion to an agent SDK.
**Score reason**: Exact match + B Expert (maintainer of a related project), 235 stars; freshness capped (repository predates the window)
**Tags**: `framework`, `sdk-companion`, `github`

---

### 🟡 Worth including (score 60–69)

No source in this band was kept: the cap of 20 was reached at score 75. Sources scoring 60–75 that were cut by the cap include ServiceNow/eva (75), two short course videos (75), plurai-ai/intellagent (74), the Langfuse agent evaluation guide (72, date `unverified`), five arXiv papers from August 2026 (72), and several community repositories (67–69).

---

## Adjacent, not ranked

- **trpc-group/trpc-agent-go** — https://github.com/trpc-group/trpc-agent-go — an agent-building framework in Go; evaluation is one feature among many.
- **JuryFlow: Disagreement-Guided Human-in-the-Loop Multi-Agent Evaluation** — https://arxiv.org/abs/2609.40103v1 — uses multiple LLM judges to evaluate AI-generated content; the agents are the evaluators, not the object evaluated.
- **Context-dependent agent evaluation with orthogonal equilibrium learning** — https://arxiv.org/abs/2609.31897v1 — offline, equilibrium-based evaluation of agents under context; a learning-theory object rather than the evaluation of LLM agents.

---

## Trends identified

- **Evaluating the evaluation.** Most of the recent papers do not introduce a benchmark; they audit scores that already exist: leaderboard reliability, reward integrity, evidence sufficiency, outcome finality, human re-review of automated verdicts.
- **LLM-as-judge is under sustained scrutiny.** Several independent papers measure judge error on agent trajectories (version-dependent error, certified automation, voice and mobile judge benchmarks), and the top conference talk opens on a judge wrongly rejecting every output.
- **The unit of evaluation is the system and its trajectory, not the model and its final answer.** Research ("agents are systems", scaffold effects on rank) and practitioner guides (trajectory, tool use, repeated runs) agree on this point.
- **A standardization push without a standard.** A trust layer, a semantic layer (EIO-Agents) and a portable contract (Evaluation Context Protocol) were all proposed within the window, while Harbor positions itself as shared harness infrastructure across benchmarks.
- **Evaluation is specializing and getting expensive.** Domain-specific work (voice, mobile, web, financial, cybersecurity, companion agents) is multiplying, and cost is now a research topic of its own (EarlyEval).

---

*Generated by tech-watch skill | Sources: arXiv · GitHub · YouTube · Web search*
*Scoring: Relevance 40% · Freshness 20% · Authority 20% · Depth 10% · Engagement 10%*
