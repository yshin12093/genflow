# MCP vs RL

MCP and reinforcement learning sit on **different layers** of an agent stack. They are often compared because both improve what an agent can *do*, but they solve different problems:

| | **MCP (Model Context Protocol)** | **RL (Reinforcement Learning)** |
|---|---|---|
| **What it is** | An open protocol for connecting models to tools, data, and prompts | A training method that improves behavior from reward signals |
| **Layer** | Interface / runtime connectivity | Policy optimization / learning |
| **Changes** | *What* an agent can reach (APIs, files, DBs, other agents) | *How well* an agent chooses actions over time |
| **When it helps** | You need portable, reusable tool access | You have a measurable outcome and can run many trials |
| **When it does not** | It does not teach the model better judgment by itself | It does not give the model new tools or data sources |

They compose: MCP can be the **environment interface**; RL can be the **policy** that learns to use that environment well.

## MCP in one paragraph

[Model Context Protocol](https://www.anthropic.com/news/model-context-protocol) is an open standard (JSON-RPC) for exposing **tools**, **resources**, and **prompts** to any compatible client. A server implements the integration once (GitHub, Postgres, S3, Neo4j, a hospital EHR, …). Any MCP client — Claude, Cursor, custom agents — can discover and call those capabilities without a one-off connector per model vendor.

MCP is closer to USB or HTTP than to a training algorithm: it standardizes the plug, not the skill of the operator.

What MCP does **not** do:

- Decide *when* to call a tool, or which of 200 tools is right
- Optimize multi-step workflows from outcome feedback
- Replace workflow orchestration (GenFlow’s graph + Step Functions)

Vendor tool APIs (OpenAI function calling, Anthropic tool use, Gemini function calling) are the *in-model* runtime. MCP is the *cross-vendor* protocol those runtimes can speak.

## RL in one paragraph

Reinforcement learning (including RLHF, RLAIF, and agentic RL / RFT) updates a policy so that trajectories with higher reward become more likely. For LLM agents, the “actions” are usually: which tool to call, with which arguments, whether to stop, and what to write next.

Typical loop:

1. Roll out the agent on a task (possibly calling tools for many turns)
2. Score the trajectory (task success, rubric, verifier, human preference)
3. Update the model (PPO, GRPO, DPO, etc.) so better traces are more likely

RL does **not** invent a GitHub API or a Neo4j schema. It only improves choice among actions the agent can already take. Environments, isolation, and long-horizon rollouts are the expensive parts; frameworks such as [MCP-Universe RL](https://arxiv.org/html/2608.22167) use MCP *as that environment interface* so existing servers plug into training.

## Side-by-side

| Question | MCP | RL |
|---|---|---|
| New database / SaaS / file store | Add or reuse an MCP server | No effect until the tool exists |
| Model keeps calling the wrong tool | Better descriptions / fewer tools / routing | Train on success/failure of tool choice |
| Portable across Claude, GPT, Gemini | Yes — one protocol | Weights are model-specific |
| Needs labeled outcomes | No | Yes (explicit reward, verifier, or judge) |
| Cost profile | Engineering + runtime tokens | GPU rollouts, environment isolation, reward design |
| Failure mode | Tool sprawl, context bloat, auth/ops | Reward hacking, sparse credit assignment, costly eval |
| GenFlow analogue today | Agents have **no** external tools; they only chat | Agents have **no** learned policy; routing is a fixed `NEXT_AGENT` edge |

## They are not substitutes

A common false choice is “should we add MCP or train with RL?”

- **MCP without a good policy** still yields an agent that can *see* 80 tools and pick poorly, dump huge results into context, or stop too early.
- **RL without tools** can only polish text (or whatever actions already exist). It cannot query a knowledge base or update a graph that was never exposed.
- **The production pattern** is: expose capabilities via MCP (or an equivalent tool layer), then optionally train or finetune a policy that uses those capabilities well.

Recent work treats them as a stack, not a fork: MCP-U RL trains software-engineering, research, and general tool-use agents by talking to MCP servers; ATLAS uses reinforcement finetuning so small models learn *which* tools to load instead of stuffing every schema into context.

## Mapping onto GenFlow

GenFlow already separates **workflow structure** (Neo4j `Agent` nodes and `NEXT_AGENT` edges) from **execution** (Lambda + Step Functions) from **the model** (`llm_client`). MCP and RL slot into different parts of that split.

```
                    ┌─────────────────────────────────────┐
                    │  RL / RFT (optional)                │
                    │  reward: task success, medical      │
                    │  accuracy, latency, cost            │
                    │  updates: routing, tool choice,     │
                    │  stop/continue, prompt policy       │
                    └─────────────────┬───────────────────┘
                                      │ trains
                                      ▼
  Neo4j graph ──► Step Functions ──► Agent node ──► LLM
  (who follows     (orchestration)    (role +        (policy)
   whom)                               messages)
                                      │
                                      ▼
                               MCP servers (optional)
                               S3, SNS, RAG, Neo4j,
                               EHR, calculators, …
```

### Where MCP would land

Today each agent is a prompt pair (`system_message`, `user_message`) and a single LLM completion. [Future work](../README.md#future-work) already calls out S3, SNS, SQS, and knowledge bases. MCP is the clean way to attach those without a custom adapter per provider:

- An **MCP client** inside `process_agent` (or a sidecar Lambda) lists tools from configured servers.
- Agent nodes in Neo4j can point at *which servers* they may use (`[:CAN_USE]->(:McpServer)`), keeping tool access in the graph the same way routing already lives in the graph.
- The same S3/RAG/Neo4j servers would work from Claude, GPT, or DeepSeek because GenFlow already multiplexes providers in `llm_client`.

MCP matches GenFlow’s existing design rule: **change capability by updating the graph, not by redeploying orchestration**.

### Where RL would land

README future work also mentions automated graph updates, agent behavior learning, and workflow optimization. That is an RL (or at least bandit / policy-learning) problem:

| Signal (reward) | What could be learned |
|---|---|
| Evaluator agent scores (this repo’s medical example already has an evaluator node) | Whether earlier agents’ answers were useful |
| Downstream verifier / rubric | Tool choice and argument quality |
| Step Functions metrics (duration, retries, cost) | Shorter paths, skip useless agents |
| Human thumbs / clinical override | Preference alignment of the whole chain |

Concretely, RL could update:

1. **Routing policy** — replace a static `NEXT_AGENT` edge with a learned choice among candidate next agents.
2. **Tool policy** — which MCP tool to call, when to stop calling tools.
3. **Prompt / agent policy** — weights or adapters so the psychiatrist / checker / evaluator roles get better at their jobs.

The graph remains the source of *legal* actions (allowed next agents, allowed MCP servers). RL chooses among those actions.

### Practical order for this codebase

1. **Keep the graph as the workflow source of truth** (already true).
2. **Add MCP for tools** when agents need data or side effects — highest leverage relative to current chat-only nodes.
3. **Log trajectories** (agent id, prompt, completion, tool calls, next hop, outcome) from Step Functions / Lambda. Without traces, RL has nothing to train on.
4. **Add RL only where reward is cheap and honest** — e.g. the existing evaluator node, unit-style verifiers, or task success — not as a first step.

Skipping (2) and (3) and jumping to RL would train a better essay-writer, not a better *workflow*. Skipping RL forever is also fine: many production graphs stay hand-authored and still benefit from MCP.

## Decision guide

| Goal | Prefer |
|---|---|
| Connect GenFlow agents to S3, RAG, Neo4j, or SaaS | MCP |
| Same tools from OpenAI, Anthropic, and DeepSeek | MCP |
| Reduce tokens when many tools exist | MCP + on-demand tool loading (or code execution over MCP); RL can later learn *what* to load |
| Improve medical-eval chain quality using the evaluator’s score | RL / RFT on logged traces |
| Auto-rewire `NEXT_AGENT` from outcome data | RL or simpler bandits on the graph |
| One-off demo of a new agent role | Neither — add a node and an edge |

**Short version:** MCP gives GenFlow agents hands. RL teaches those agents (and the graph) better judgment. Build the hands first; collect rewards; then, if the loop is closed, train.
