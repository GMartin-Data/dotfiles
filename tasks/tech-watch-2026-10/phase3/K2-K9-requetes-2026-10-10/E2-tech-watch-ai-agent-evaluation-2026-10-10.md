# Tech Watch — AI agent evaluation
**Date**: 2026-10-10 | **Window**: 30 days | **Sources**: 20

---

## Executive Summary
The dominant theme of the last 30 days is not new agent benchmarks but distrust of the measurement itself: most of the retained arXiv papers audit judges, verifiers, leaderboards and harness effects rather than proposing new tasks. On the tooling side, open-source activity is concentrated on harness-style frameworks (environments, trace-based evaluation, skill evaluation) and on specialised verticals such as voice agents and agent red-teaming. Unexpected finding: no general web article could reach the top 20, the Tier 2 web results being mostly vendor-authored guides with unverified dates.

---

## Sources ranked by score

Scoring notes (interpretations where the criteria are silent):
- GitHub freshness is computed on the **last push date**, not on a publication date. It is a weak proxy that favours any actively maintained repository.
- A substantial framework repository is scored 10 on technical depth, like a full tutorial.
- arXiv papers have no engagement signal available: 3 pts each.
- Summaries are based on the titles, abstracts excerpts and descriptions returned by the search tools; the sources themselves were not read in full.

---

### 🔴 Essential (score 85–100)

**[1] harbor-framework/harbor**
🔗 https://github.com/harbor-framework/harbor
📅 Last push 2026-10-10 (created 2025-08-04) | ⭐ Authority: High | 📊 Score: 100/100
**Summary**: Python framework "for evaluating and improving agents", tagged evals, rl-environments and terminal-bench. With close to 6k stars it is the most starred result directly on topic.
**Score reason**: Exact match on the topic + 5,978 stars with a push on the day of the report
**Tags**: `framework`, `harness`, `terminal-bench`

**[2] NVIDIA/SkillEvaluator**
🔗 https://github.com/NVIDIA/SkillEvaluator
📅 Last push 2026-10-10 (created 2026-06-24) | ⭐ Authority: High | 📊 Score: 100/100
**Summary**: Multi-tier framework for evaluating agent skills: quality gates, semantic overlap detection, synthetic evaluation dataset generation, and live evaluation measuring how skills change agent behaviour. It targets the evaluation of skills rather than of whole agents, a recent angle.
**Score reason**: Exact match (agent skill evaluation) + 554 stars in under four months, pushed today
**Tags**: `agent-skills`, `synthetic-data`, `quality-gates`

**[3] From Vibes to Production: Evaluating and Shipping AI Agents That Work 101 — Laurie Voss, Arize AI**
🔗 https://www.youtube.com/watch?v=qZj7sqmidqA
📅 2026-10-05 | ⭐ Authority: High | 📊 Score: 100/100
**Summary**: 1h51 workshop on the AI Engineer channel. It starts from an LLM correctness judge rejecting all 13 reports of a financial analysis agent and investigates why, which makes it a practical counterpart to the judge-reliability papers below.
**Score reason**: Exact match, full-length workshop + 12.7k views in five days
**Tags**: `workshop`, `llm-as-judge`, `production`

**[4] strands-agents/evals**
🔗 https://github.com/strands-agents/evals
📅 Last push 2026-10-08 (created 2025-07-31) | ⭐ Authority: High | 📊 Score: 95/100
**Summary**: Evaluation framework for AI agents and LLM applications from the Strands Agents project. Relevant as an evaluation layer attached to an agent SDK.
**Score reason**: Exact match + pushed two days ago (235 stars, moderate engagement)
**Tags**: `framework`, `python`, `agent-sdk`

**[5] agentevals-dev/agentevals**
🔗 https://github.com/agentevals-dev/agentevals
📅 Last push 2026-10-09 (created 2026-02-24) | ⭐ Authority: High | 📊 Score: 95/100
**Summary**: Framework-agnostic evaluation built on OpenTelemetry traces. It illustrates the approach of evaluating agents from their traces rather than from a framework-specific harness.
**Score reason**: Exact match + pushed yesterday (163 stars, moderate engagement)
**Tags**: `opentelemetry`, `traces`, `framework-agnostic`

**[6] AgentEvalHQ/AgentEval**
🔗 https://github.com/AgentEvalHQ/AgentEval
📅 Last push 2026-10-10 (created 2026-01-02) | ⭐ Authority: High | 📊 Score: 95/100
**Summary**: .NET toolkit for agent evaluation (tool usage validation, RAG quality metrics, stochastic evaluation, model comparison), built first for Microsoft Agent Framework and Microsoft.Extensions.AI. It positions itself as the .NET equivalent of RAGAS, PromptFoo and DeepEval.
**Score reason**: Exact match + pushed today (155 stars, moderate engagement)
**Tags**: `dotnet`, `tool-use`, `stochastic-evaluation`

**[7] ServiceNow/eva**
🔗 https://github.com/ServiceNow/eva
📅 Last push 2026-10-06 (created 2026-03-24) | ⭐ Authority: High | 📊 Score: 95/100
**Summary**: End-to-end framework for evaluating voice agents. It covers a vertical (voice) that also appears in this window's arXiv and YouTube results.
**Score reason**: Exact match on a specialised vertical + pushed four days ago (227 stars)
**Tags**: `voice-agents`, `end-to-end`, `asr`

**[8] AgentSafeLabs/safelabs-eval**
🔗 https://github.com/AgentSafeLabs/safelabs-eval
📅 Last push 2026-10-09 (created 2026-05-25) | ⭐ Authority: High | 📊 Score: 95/100
**Summary**: Red-teaming and evaluation framework for AI agents organised around an OWASP-inspired ASI01-ASI10 taxonomy. It brings the security dimension of agent evaluation.
**Score reason**: Exact match on the security side + pushed yesterday (470 stars, just under the 500 threshold)
**Tags**: `red-teaming`, `agent-security`, `owasp`

**[9] Why Your AI Agent Fails in Production (And How to Catch It)**
🔗 https://www.youtube.com/watch?v=wPdoZRbvaF4
📅 2026-09-30 | ⭐ Authority: High | 📊 Score: 95/100
**Summary**: 26-minute Google Cloud Tech episode on how to evaluate agents for production, opposing structured evaluation to manual tweaking. A vendor-produced but substantial tutorial.
**Score reason**: Exact match, full tutorial + 18.7k views
**Tags**: `tutorial`, `production`, `google-cloud`

**[10] A Trust Layer for Agent Evaluation**
🔗 https://arxiv.org/abs/2610.07274v1
📅 2026-10-05 | ⭐ Authority: High | 📊 Score: 93/100
**Summary**: Argues that deterministic benchmark scores show that an agent received credit, but not whether the credit was earned, reported honestly, or would hold on a second run. Proposes a trust layer on top of agent evaluation.
**Score reason**: Direct match on query + arXiv paper from 5 days ago
**Tags**: `benchmark-validity`, `trust`, `reproducibility`

**[11] EIO-Agents: The Missing Semantic Layer for AI Agent Evaluation**
🔗 https://arxiv.org/abs/2610.07675v1
📅 2026-10-06 | ⭐ Authority: High | 📊 Score: 93/100
**Summary**: Starts from the lack of a shared semantic standard for what agent evaluations mean (scores, traces, judge outputs) as agents enter production in consequential environments. Proposes a semantic layer to fill that gap.
**Score reason**: Direct match on query + arXiv paper from 4 days ago
**Tags**: `standardization`, `semantics`, `production`

**[12] TRACE: Diagnosing Verifier Brittleness in Agentic Evaluation**
🔗 https://arxiv.org/abs/2610.11678v1
📅 2026-10-08 | ⭐ Authority: High | 📊 Score: 93/100
**Summary**: Verifier scores serve both as benchmark metrics and as training rewards, and a score change is routinely read as a capability change. The paper examines the case where it instead reflects the verifier's own brittleness.
**Score reason**: Direct match on query + arXiv paper from 2 days ago
**Tags**: `verifiers`, `benchmark-validity`, `diagnostics`

**[13] Transect: Retaining Observability for Long-Horizon LLM Agent Evaluations**
🔗 https://arxiv.org/abs/2610.08364v2
📅 2026-10-06 | ⭐ Authority: High | 📊 Score: 93/100
**Summary**: Addresses the observability problem of open-ended, long-horizon agentic evaluations whose transcripts span hundreds of pages across multi-agent networks.
**Score reason**: Direct match on query + arXiv paper from 4 days ago
**Tags**: `long-horizon`, `observability`, `transcripts`

**[14] P90-RushB/AgentArk**
🔗 https://github.com/P90-RushB/AgentArk
📅 Last push 2026-09-30 (created 2025-08-21) | ⭐ Authority: High | 📊 Score: 90/100
**Summary**: General-purpose environment framework for scalable multimodal agent evaluation and RL. Like harbor, it couples evaluation environments with RL use.
**Score reason**: Exact match + pushed 10 days ago (211 stars, moderate engagement)
**Tags**: `environments`, `multimodal`, `rl`

**[15] Agent Evaluation Reliability: More Tasks Won't (Always) Fix An Agent Leaderboard**
🔗 https://arxiv.org/abs/2610.00651v1
📅 2026-09-30 | ⭐ Authority: High | 📊 Score: 88/100
**Summary**: Shows that leaderboard ranks can reflect evaluation conditions such as the scaffold, and not only the model. The title's claim is that adding tasks does not always fix this.
**Score reason**: Direct match on query + arXiv paper from 10 days ago
**Tags**: `leaderboards`, `reliability`, `scaffold-effects`

**[16] Agents Are Systems, Not Models: Rethinking Agentic Evaluation**
🔗 https://arxiv.org/abs/2610.01618v1
📅 2026-10-01 | ⭐ Authority: High | 📊 Score: 88/100
**Summary**: Notes that evaluations now report cost, consistency and robustness but still treat the agent as a fixed object, and argues for evaluating it as a system.
**Score reason**: Direct match on query + arXiv paper from 9 days ago
**Tags**: `position-paper`, `system-level`, `methodology`

**[17] Auditing Web Agent Evaluation on WebArena-Lite: Human Review of Outcomes and Trajectories**
🔗 https://arxiv.org/abs/2610.01491v1
📅 2026-10-01 | ⭐ Authority: High | 📊 Score: 88/100
**Summary**: Human audit of a web agent benchmark whose rule-based or LLM evaluators inspect only the final outcome, with review of both outcomes and trajectories.
**Score reason**: Direct match on query + arXiv paper from 9 days ago
**Tags**: `web-agents`, `human-audit`, `trajectories`

**[18] Certified Selective Automation of LLM Agent Evaluation**
🔗 https://arxiv.org/abs/2609.34320v1
📅 2026-09-28 | ⭐ Authority: High | 📊 Score: 88/100
**Summary**: Starts from the fact that agent evaluation still ends with a human reading trajectories because automatic judges carry no error guarantee, and asks what fraction of evaluations can be automated with a guarantee.
**Score reason**: Direct match on query + arXiv paper from 12 days ago
**Tags**: `llm-as-judge`, `guarantees`, `human-in-the-loop`

**[19] Frozen Judges, Moving Agents: Version-Dependent LLM-Judge Error and the Limits of Judge-Assisted Agent Evaluation**
🔗 https://arxiv.org/abs/2609.34198v2
📅 2026-09-28 | ⭐ Authority: High | 📊 Score: 88/100
**Summary**: Analyses 35 public coding-agent submissions to show that a fixed LLM judge can make version-dependent mistakes when comparing an agent upgrade with its predecessor.
**Score reason**: Direct match on query + arXiv paper from 12 days ago
**Tags**: `llm-as-judge`, `coding-agents`, `regression-testing`

**[20] Measurement Boundaries in LLM Financial Agent Evaluation: Fixed-Tape Execution and Multi-Defect Auditing**
🔗 https://arxiv.org/abs/2609.32379v1
📅 2026-09-26 | ⭐ Authority: High | 📊 Score: 88/100
**Summary**: Studies, in a financial agent harness, which controls are needed to interpret execution performance and audit scores. Domain-specific, but the question is the general one of measurement limits.
**Score reason**: Direct match on query + arXiv paper from 14 days ago
**Tags**: `finance`, `measurement`, `auditing`

---

### 🟠 High value (score 70–84)

None retained: the 20-source target was filled at score 88. Candidates left out in this band include plurai-ai/intellagent and agentscope-ai/OpenJudge (85, first below the cut), the arXiv papers "Policy Loopholes in Agent Evaluation" and "Skill-based Agentic Evaluation for Real-time Data Science Tasks" (78), and mozilla-ai/any-agent (75).

---

### 🟡 Worth including (score 60–69)

None retained (band only used when the total is under 20). Tier 2 web guides (Langfuse, IBM Developer, Mercor, Kunal Ganglani) fall in or below this band: quality-blog authority at best and no verified publication date.

---

## Trends identified

- **Evaluating the evaluator**: seven of the ten retained papers question the instrument rather than the agent (verifier brittleness, version-dependent judge error, certified automation of judging, human audit of a benchmark, leaderboard reliability, measurement boundaries, trust layer).
- **From model to system**: several sources converge on the idea that a score belongs to a scaffold-plus-model system under given conditions, not to a model (leaderboard reliability paper, "Agents Are Systems, Not Models").
- **Final outcome is not enough**: papers and practitioner content both push towards trajectory and trace inspection (WebArena-Lite audit, Transect, OpenTelemetry-based agentevals), a point also made consistently by the Tier 2 web guides.
- **Open-source tooling is fragmenting by niche**: besides general harnesses (harbor, strands evals), active repositories target a stack (.NET), a modality (voice), a concern (security red-teaming) or a unit of evaluation (skills).
- **Standardisation attempts are appearing**: a semantic layer (EIO-Agents) and a trust layer are proposed in the same week, a sign that shared meaning of evaluation results is seen as missing.

---

*Generated by tech-watch skill | Sources: arXiv · GitHub · YouTube · Web search*
*Scoring: Relevance 40% · Freshness 20% · Authority 20% · Depth 10% · Engagement 10%*
