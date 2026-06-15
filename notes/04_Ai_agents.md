## ⛓️ Chains vs. AI Agents vs. Agentic AI

Moving from standard LLM prompts to production-grade applications requires choosing the right architecture. As you scale, you move from static, predictable pipelines (Chains) to dynamic, goal-oriented systems (Agents).

### Core Definitions

**Chains**

> A hardcoded sequence of steps. The execution path is fully determined by the developer. Input goes into Step A, the output goes into Step B, and so on. There is zero runtime decision-making by the LLM regarding _where_ the data goes next.

**AI Agents**

> An architecture where the LLM acts as a reasoning engine. You provide the LLM with a goal and a set of **Tools** (APIs, databases, web search). The LLM autonomously decides _which_ tool to use, calls it, evaluates the output, and decides the next step until the goal is met.

**Agentic AI / Agentic Workflows**

> The broader design paradigm of shifted execution. Instead of treating an LLM like a single-turn question-answering machine (zero-shot), you wrap it in iterative loops (reflection, self-correction, planning). It refers to systems designed to behave with a high degree of autonomy, memory, and persistence.

---

### ⚙️ The Architectural Spectrum

In production, you are always balancing **Predictability** against **Flexibility**.

[Chains] -------------------------> [AI Agents] -------------------------> [Agentic AI]

- Hardcoded Paths - LLM chooses tools - Multi-agent systems
- 100% Predictable - Semi-predictable - Fully autonomous
- Low Latency - Medium Latency - High Latency & Cost

1. **Chains:** Best for structured workflows (e.g., standard RAG, data extraction pipelines). It's cheap, deterministic, and fast.
2. **Agents:** Best when the inputs vary wildly and you can't predict every edge case (e.g., a customer support assistant that needs to check order status _or_ process a refund depending on user intent).
3. **Agentic AI:** Best for complex, open-ended objectives (e.g., an AI software engineer like Devin that writes code, tests it, encounters a bug, reads the log, and fixes its own mistake).

---

## 🧠 Interview Prep: Chains vs. Agents

### Practice Questions

<details>
<summary><b>Q1: When would you choose a strict Chain over an autonomous Agent in production?</b> (Click to reveal)</summary>
<br>

In a production environment, **predictability and latency are king.** You should choose a Chain whenever the business logic is fixed.

| Factor             | Chains                                          | AI Agents                                             |
| :----------------- | :---------------------------------------------- | :---------------------------------------------------- |
| **Control**        | Absolute. You know exactly what code runs next. | Variable. The LLM decides the execution graph.        |
| **Cost & Latency** | Low. Minimal LLM calls per request.             | High. Can loop multiple times, inflating tokens/time. |
| **Debugging**      | Easy. Standard stack traces work.               | Difficult. Requires tracing LLM reasoning loops.      |

**How to say it in an interview:**
_"If the workflow can be drawn cleanly on a whiteboard as a flowchart with fixed rules, use a Chain. For example, if I'm building a legal document summarizer, I want a deterministic chain: Extract Text → Translate → Summarize. If I used an Agent here, I risk the LLM deciding to search the web or loop indefinitely, blowing up both latency and my OpenAI token bill without adding any value."_

</details>

<details>
<summary><b>Q2: How do Agents actually work under the hood? Explain the ReAct framework.</b> (Click to reveal)</summary>
<br>

Most modern agents rely on the **ReAct (Reasoning and Acting)** prompt paradigm. It forces the LLM to alternate between thinking and executing tools in a loop.

**The Internal Loop Steps:**

1. **Thought:** The LLM analyzes the user's objective and decides what it needs to do (e.g., _"The user wants the stock price of Apple. I don't know it, so I need to check the web."_).
2. **Action:** The LLM outputs a specifically formatted string targeting a tool (e.g., `Action: GoogleSearch(query="Apple stock price")`).
3. **Observation:** The backend code intercepts this string, runs the actual Python tool function, and pipes the result back into the prompt context (e.g., _"Observation: AAPL is currently trading at $180"_).
4. **Repeat/Final Answer:** The LLM reads the observation and either takes another action or delivers the final answer to the user.

> [!IMPORTANT]
> **Production Note:** The LLM itself does _not_ call the API. The LLM simply returns text indicating its intent. Your application framework (like LangChain or LangGraph) parses that text, runs the Python code for the tool, and returns the result back to the model.

</details>

<details>
<summary><b>Q3: What are the primary failure modes of Agentic AI systems, and how do you mitigate them?</b> (Click to reveal)</summary>
<br>

Agentic workflows are notoriously difficult to control. Interviewers love asking about error handling here because it separates junior builders from engineers who have actually deployed to production.

**Top 3 Failure Modes:**

1. **Infinite Loops (The Doom Loop):** The agent tries a tool, fails, reads the error, and tries the exact same tool again with the same parameters, repeating forever.
   - _Mitigation:_ Set a strict `max_iterations` ceiling (e.g., maximum 5 loops) or use LangGraph to explicitly catch repetitive states.
2. **Tool Abuse / Hallucinated Arguments:** The LLM invents parameters that the underlying Python function doesn't accept.
   - _Mitigation:_ Use strict JSON schemas or Pydantic validation via OpenAI tool binding to force the model's output to strictly align with your function signatures.
3. **Context Window Bloat:** As the agent loops, the prompt history grows massive. The model loses focus (Needle-in-a-Haystack problem) and costs skyrocket.
   - _Mitigation:_ Implement explicit memory management, such as trimming old messages or using an LLM to summarize the interaction history at each step.

</details>
