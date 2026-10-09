# Scoring Criteria

Score each result 0–100 by summing the five weighted criteria below.
Apply in order — stop early if a result clearly won't reach 60.

---

## Criteria

| # | Criterion | Weight | How to assess |
|---|-----------|--------|---------------|
| 1 | **Semantic relevance** | 40% | Does the title/abstract/description directly address the query? Score 40 if exact match, 20 if adjacent topic, 0 if tangential. |
| 2 | **Freshness** | 20% | ≤ 7 days = 20pts. Decays linearly: 8–14d = 15pts, 15–21d = 10pts, 22–30d = 5pts, > 30d = 0pts. |
| 3 | **Source authority** | 20% | Tier 1 high-priority (arXiv, GitHub, YouTube) = 20pts. Tier 2 quality blog/newsletter = 12pts. General web = 6pts. SEO-optimized or low-signal = 0pts. |
| 4 | **Technical depth** | 10% | Research paper or full tutorial (> 1500 words) = 10pts. Short post or video clip (< 5min) = 4pts. |
| 5 | **Engagement signals** | 10% | GitHub stars > 500, YouTube views > 10k, or explicit citation count = 10pts. Some signals = 5pts. None available = 3pts (don't penalize absence). |

---

## Score labels

| Range | Label | Meaning |
|-------|-------|---------|
| 85–100 | 🔴 Tier 1 / Essential | Include prominently, likely to anchor NotebookLM analysis |
| 70–84 | 🟠 High value | Include, solid signal |
| 60–69 | 🟡 Worth including | Include if total results < 20 |
| < 60 | Excluded | Drop unless Tier 3 run returns nothing better |

---

## Score reasoning

For each included result, write a one-line `score_reason` summarizing the top 2 factors.
> Example: "Direct match on query + arXiv publication from 3 days ago"
> Example: "GitHub repo with 2.1k stars, exact implementation of topic"
