# Tech Watch — AI agent evaluation
**Date**: 2026-10-09 | **Window**: 30 days | **Sources**: 20

> Scoring notes: GitHub freshness is based on the last push date (not creation date). Summaries of arXiv papers are based on title and truncated abstract only. Small YouTube channels (< 100 views) were given half authority (10/20). Tier 3 was not run (Tier 1 + 2 returned more than 12 relevant results).

---

## Executive Summary
The month's output converges on one idea: scoring an agent's final answer is no longer considered sufficient, and the work is moving to process-level evaluation (trajectories, tool calls, behavioral drift across versions) and to the reliability of the evaluators themselves (LLM judges, human raters, the meaning of a score). The unexpected finding is how much of the research now targets the measurement instrument rather than the agent: meta-evaluation of LM judges, rater effects in human scoring, and a proposed shared semantic standard for eval artifacts. Benchmarks are also fragmenting by domain (science workflows, voice, AIOps, regulated workflows) rather than consolidating around general-purpose leaderboards.

---

## Sources ranked by score

---

### 🔴 Essential (score 85–100)

**[1] From Vibes to Production: Evaluating and Shipping AI Agents That Work 101 — Laurie Voss, Arize AI**
🔗 https://www.youtube.com/watch?v=qZj7sqmidqA
📅 2026-10-05 | ⭐ Authority: High | 📊 Score: 100/100
**Summary**: Workshop-length talk (1h51) on the AI Engineer channel. It opens with a concrete failure case: an LLM correctness judge rejecting all 13 reports from a financial analysis agent, and works through why. Practical entry point for the judge-reliability problem the papers below treat formally.
**Score reason**: Exact match on query + 4-day-old long-form talk with 11.9k views
**Tags**: `llm-as-judge`, `production-evals`, `workshop`

**[2] truera/trulens**
🔗 https://github.com/truera/trulens
📅 Last push 2026-10-09 (created 2020-11-02) | ⭐ Authority: High | 📊 Score: 97/100
**Summary**: "Evaluation and Tracking for LLM Experiments and AI Agents". Long-lived open-source evaluation and observability library, explicitly tagged `agent-evaluation`, and still pushed to on the day of this report.
**Score reason**: Exact implementation of the topic + 3.6k stars, active today
**Tags**: `open-source`, `observability`, `agent-evaluation`

**[3] Why Your AI Agent Fails in Production (And How to Catch It)**
🔗 https://www.youtube.com/watch?v=wPdoZRbvaF4
📅 2026-09-30 | ⭐ Authority: High | 📊 Score: 95/100
**Summary**: 26-minute Google Cloud Tech episode on evaluating agents for production, framed around the claim that manual tweaking is not a testing strategy. A 25-second "Agent Evaluation walkthrough" teaser from the same channel was deduplicated into this entry.
**Score reason**: Exact match on query + 18.3k views from a first-party vendor channel
**Tags**: `production-readiness`, `google-cloud`, `tutorial`

**[4] EIO-Agents: The Missing Semantic Layer for AI Agent Evaluation**
🔗 https://arxiv.org/abs/2610.07675v1
📅 2026-10-06 | ⭐ Authority: High | 📊 Score: 93/100
**Summary**: Argues that agents are reaching production without a shared semantic standard for what their evaluations mean, across scores, traces, judge outputs and multi-juror results. Proposes a semantic layer to fill that gap.
**Score reason**: Query term in the title + arXiv paper from 3 days ago
**Tags**: `standardization`, `eval-semantics`, `arxiv`

**[5] Reliability of AI Agents: Rater Effects, Drift, and the Return to an Evaluation Program**
🔗 https://arxiv.org/abs/2610.07003v1
📅 2026-10-04 | ⭐ Authority: High | 📊 Score: 93/100
**Summary**: Looks at firms that evaluate deployed agents with repeated human ratings, and argues that observed score changes may reflect the measurement process as much as the agent. Filed under econ.GN, so it brings a measurement and economics angle that the cs.AI papers lack.
**Score reason**: Direct match on agent evaluation reliability + arXiv paper from 5 days ago
**Tags**: `human-raters`, `measurement-validity`, `drift`

**[6] harbor-framework/terminal-bench-science**
🔗 https://github.com/harbor-framework/terminal-bench-science
📅 Last push 2026-10-06 (created 2026-01-25) | ⭐ Authority: High | 📊 Score: 93/100
**Summary**: Terminal-Bench-Science, a benchmark evaluating AI agents on research workflows across scientific domains. Pairs naturally with source [9], which questions how such science benchmarks score agents.
**Score reason**: Agent benchmark repo pushed 3 days ago + 695 stars
**Tags**: `benchmark`, `ai-for-science`, `terminal-bench`

**[7] coze-dev/coze-loop**
🔗 https://github.com/coze-dev/coze-loop
📅 Last push 2026-10-09 (created 2025-06-24) | ⭐ Authority: High | 📊 Score: 92/100
**Summary**: Agent optimization platform covering development, debugging, evaluation and monitoring in one lifecycle. Evaluation is one of several pillars rather than the sole focus, hence slightly reduced relevance.
**Score reason**: 5.8k stars, tagged agent-evaluation, active today
**Tags**: `agentops`, `platform`, `full-lifecycle`

**[8] alibaba/skill-up**
🔗 https://github.com/alibaba/skill-up
📅 Last push 2026-10-09 (created 2026-05-09) | ⭐ Authority: High | 📊 Score: 92/100
**Summary**: "An evaluation and evolution tool for Agent Skills." Five-month-old repo that treats the skill, not the whole agent, as the unit under evaluation, the same framing as paper [10].
**Score reason**: 1.2k stars in five months + dedicated to evaluating agent skills
**Tags**: `agent-skills`, `skill-evaluation`, `go`

**[9] Are We Measuring Scientific Intelligence? Rethinking the Evaluation of AI Scientists**
🔗 https://arxiv.org/abs/2610.04915v1
📅 2026-10-04 | ⭐ Authority: High | 📊 Score: 89/100
**Summary**: Critiques benchmarks that hand an agent a question and a dataset and score only its final answer against a fixed key. Domain-specific (data-driven science), but the critique of final-answer scoring generalizes.
**Score reason**: Direct critique of agent benchmark design + arXiv paper from 5 days ago
**Tags**: `ai-scientist`, `benchmark-critique`, `final-answer-scoring`

**[10] Continuous Process-Level Evaluation for Evolving Enterprise AI Agent Skills**
🔗 https://arxiv.org/abs/2610.01833v1
📅 2026-10-01 | ⭐ Authority: High | 📊 Score: 88/100
**Summary**: Starts from the observation that enterprise agent skills change as tool APIs, models and specifications change, and that final-output evaluation can miss process-level behavioral drift. Presents a continuous evaluation framework to catch it.
**Score reason**: Exact match on query (process-level agent evaluation) + arXiv, 8 days old
**Tags**: `process-level-eval`, `behavioral-drift`, `enterprise`

**[11] PADMÉ: Preference Alignment Data Synthesis for Meta-Evaluation of LM Agent Evaluators**
🔗 https://arxiv.org/abs/2609.36086v1
📅 2026-09-28 | ⭐ Authority: High | 📊 Score: 88/100
**Summary**: Addresses whether an LM evaluator scoring agentic behavior across multiple criteria actually aligns with human judgment. Synthesizes data to meta-evaluate such evaluators.
**Score reason**: Direct match on evaluating agent evaluators + arXiv, 11 days old
**Tags**: `meta-evaluation`, `llm-as-judge`, `human-alignment`

**[12] mozilla-ai/any-agent**
🔗 https://github.com/mozilla-ai/any-agent
📅 Last push 2026-10-01 (created 2025-03-25) | ⭐ Authority: High | 📊 Score: 87/100
**Summary**: A single interface to use and evaluate different agent frameworks. Useful for comparing the same agent task across frameworks under one evaluation harness.
**Score reason**: 1.2k stars, tagged agent-evaluation + pushed 8 days ago
**Tags**: `framework-agnostic`, `agent-evaluation`, `mozilla`

---

### 🟠 High value (score 70–84)

**[13] EvalResearchBench: Can AI Agents Design Their Own Evaluations?**
🔗 https://arxiv.org/abs/2610.04184v1
📅 2026-10-03 | ⭐ Authority: High | 📊 Score: 83/100
**Summary**: Framed around recursive self-improvement: evaluation feedback guides research, but repeatedly running complex benchmarks is costly. Benchmarks whether agents can design evaluations themselves. Adjacent to the query (agents as eval authors rather than eval subjects).
**Score reason**: Close to the query + arXiv paper from 6 days ago
**Tags**: `eval-design`, `recursive-self-improvement`, `benchmark`

**[14] Evaluating Bounded Autonomy in Regulated Agentic AI: A Diagnostic Harness with Constitutional Rewards, Escalation Labels, and Runtime Governance**
🔗 https://arxiv.org/abs/2609.37501v1
📅 2026-09-28 | ⭐ Authority: High | 📊 Score: 83/100
**Summary**: Proposes RegLLM, a diagnostic harness for regulated agentic workflows instrumenting six trustworthiness signals, including citation validity, source grounding, schema compliance and escalation. Relevant where "did it escalate when it should" matters as much as task success.
**Score reason**: Agent evaluation harness for a specific setting + arXiv, 11 days old
**Tags**: `regulated-ai`, `bounded-autonomy`, `diagnostic-harness`

**[15] microsoft/AIOpsLab**
🔗 https://github.com/microsoft/AIOpsLab
📅 Last push 2026-10-01 (created 2024-10-11) | ⭐ Authority: High | 📊 Score: 82/100
**Summary**: Framework for the design, development and evaluation of autonomous AIOps agents. Domain-specific evaluation environment for operations and incident-handling agents.
**Score reason**: 1k stars, Microsoft-maintained + pushed 8 days ago
**Tags**: `aiops`, `evaluation-framework`, `microsoft`

**[16] Production AI Agents 09 · Read an agent evaluation: paired cases, missing outcomes, release gates**
🔗 https://www.youtube.com/watch?v=pWhDOzYzyrY
📅 2026-10-07 | ⭐ Authority: Medium | 📊 Score: 79/100
**Summary**: 7-minute course lesson comparing two agent releases on the same twelve synthetic cases. Covers reading an eval result rather than building one: paired comparison, missing outcomes, release gating.
**Score reason**: Exact match on query + 2 days old; small channel (31 views) lowers authority
**Tags**: `release-gates`, `paired-comparison`, `course`

**[17] Schuster Braun — Evaluating AI Agent Tooling**
🔗 https://www.youtube.com/watch?v=oR02aI9UZgI
📅 2026-10-07 | ⭐ Authority: Medium | 📊 Score: 79/100
**Summary**: 12-minute Carolina Code Conference talk on the evaluation harnesses now being built to test agentic tooling. Practitioner view on evaluating the tools agents use rather than the agent alone.
**Score reason**: Direct match on query + 2 days old; small channel (15 views) lowers authority
**Tags**: `conference-talk`, `eval-harness`, `agent-tooling`

**[18] Defining AI Agents: A Compendium of Criteria, Metrics, and Benchmarks**
🔗 https://arxiv.org/abs/2609.11018v1
📅 2026-09-10 | ⭐ Authority: High | 📊 Score: 78/100
**Summary**: Survey arguing that the lack of a standard definition of "agent" complicates evaluation, comparison and reproducibility. Good reference source for a NotebookLM corpus: it catalogs criteria, metrics and benchmarks in one place.
**Score reason**: Exact match (survey of agent metrics and benchmarks); 29 days old limits freshness
**Tags**: `survey`, `metrics`, `benchmarks`

**[19] VAmoS Part Deux: Harder, More Realistic Voice-Agent Simulation**
🔗 https://arxiv.org/abs/2609.38512v1
📅 2026-09-29 | ⭐ Authority: High | 📊 Score: 78/100
**Summary**: Introduces VAmoS Energy, a benchmark of 100 utility-related calls combining multiple requests, background speech and impatient customers. Representative of the push toward simulation-based evaluation for voice agents.
**Score reason**: Domain-specific agent benchmark + arXiv, 10 days old
**Tags**: `voice-agents`, `simulation`, `benchmark`

**[20] VoltAgent/awesome-ai-agent-papers**
🔗 https://github.com/VoltAgent/awesome-ai-agent-papers
📅 Last push 2026-10-02 (created 2026-02-10) | ⭐ Authority: High | 📊 Score: 74/100
**Summary**: Curated list of 2026 AI agent research papers, with evaluation as one of its sections. Not a primary source, but a maintained index for following the topic beyond this 30-day window.
**Score reason**: 1.8k stars, pushed 7 days ago; evaluation is only one section (adjacent)
**Tags**: `awesome-list`, `paper-index`, `curation`

---

### 🟡 Worth including (score 60–69)

None included: per the scoring rules this band is only used when fewer than 20 sources score 70 or above. The Tier 2 web results all landed here or below (publication dates older than 30 days or not verifiable, so 0 freshness points), for example the Langfuse PydanticAI/MCP agent evaluation cookbook, the IBM and Dataiku agent evaluation tutorials, and Kunal Ganglani's 3-level production framework (2026-07-12), each at about 65/100.

---

## Trends identified

- **From final output to process.** Papers [9] and [10] both name final-answer scoring as the blind spot, and the practitioner material from Tier 2 web search describes the full trajectory (tool selection, arguments, error recovery) as the unit of evaluation. Research and practice agree on this point.
- **The evaluator is now the object of study.** [1] (a judge rejecting every report), [5] (rater effects in human scoring), [11] (meta-evaluation of LM evaluators) and [4] (no shared meaning for scores and judge outputs) all question the instrument rather than the agent.
- **"Skills" are emerging as a unit of evaluation.** [8] and [10] independently evaluate agent skills and their evolution over time, rather than a monolithic agent, which makes evaluation a continuous regression problem as APIs and models change.
- **Benchmarks are specializing by domain.** Science workflows ([6], [9]), voice ([19]), AIOps ([15]) and regulated workflows ([14]) each get their own harness; no new general-purpose agent benchmark surfaced in this window.
- **Evaluation is being absorbed into agent platforms.** [2], [7] and [12] bundle evaluation with tracing, monitoring or framework abstraction, and several general agent frameworks that scored below the cut (google/adk-python, google/agents-cli, trpc-group/trpc-agent-go) list evaluation as a built-in feature.

---

*Generated by tech-watch skill | Sources: arXiv · GitHub · YouTube · Web search*
*Scoring: Relevance 40% · Freshness 20% · Authority 20% · Depth 10% · Engagement 10%*
