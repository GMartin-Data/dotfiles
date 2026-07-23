# Common Explanation Gaps by Domain

## Programming

**Typical jargon traps:**
- "It iterates" → What does iterate mean concretely?
- "The function returns" → Returns to where? What happens next?
- "It's abstracted" → Abstracted how? What's hidden?
- "It handles the logic" → What logic? What decisions?

**Common logical jumps:**
- Skipping variable assignment → "Where did X come from?"
- Assuming loop understanding → "What repeats? When does it stop?"
- Implicit state changes → "What changed after that step?"

## Data Engineering

**Typical jargon traps:**
- "The pipeline ingests" → What does ingest mean physically?
- "It's partitioned" → Partitioned by what? Why does that help?
- "ETL" → What's extracted from where? Transformed how? Loaded where?
- "Schema" → What's a schema in concrete terms?

**Common logical jumps:**
- Assuming database knowledge → "What's a table? How is it different from a file?"
- Skipping serialization → "How does data travel between systems?"
- Implicit ordering → "What ensures this happens before that?"

## Machine Learning / AI

**Typical jargon traps:**
- "The model learns" → Learns how? What changes?
- "It optimizes" → What's being made better? Better at what?
- "Features" → Features of what? How are they numbers?
- "Training" → What happens during training, step by step?

**Common logical jumps:**
- Skipping gradient descent → "How does the model improve?"
- Assuming vector understanding → "What's a vector? Why numbers?"
- Implicit probability → "What does 'likely' mean mathematically?"

## Distributed Systems

**Typical jargon traps:**
- "It scales" → Scales what? How?
- "Consistency" → Consistent with what?
- "The node" → What's a node physically?
- "Replication" → Replicated where? When? By what?

**Common logical jumps:**
- Assuming network knowledge → "How do machines talk?"
- Skipping failure modes → "What if one part breaks?"
- Implicit timing → "What happens if A and B happen simultaneously?"

## General Patterns

**Red flag phrases (almost always hide gaps):**
- "It basically..."
- "It just..."
- "It's like..."  (without completing the analogy)
- "You know..."
- "Obviously..."
- "It handles..."
- "It takes care of..."

**Questions that expose depth:**
- "What would break if we removed this step?"
- "How would you verify this worked?"
- "What's the simplest example of this?"
- "If I had to do this manually, what would I do?"
