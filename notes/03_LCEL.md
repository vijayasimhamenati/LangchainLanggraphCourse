## **LangChain Expression Language (LCEL) and the Runnable Interface**.

---

## 🔗 LCEL & The Runnable Interface

To build real AI applications, you need to connect Prompts, Models, and Parsers together. **LangChain Expression Language (LCEL)** is the specialized syntax used to chain these components seamlessly. Under the hood, this syntax is powered by the **Runnable Interface**.

### Core Definitions

**LCEL (LangChain Expression Language)**

> A declarative way to easily compose chains together. It uses the standard Unix pipe operator (`|`) to take the output of the component on the left and pass it as the input to the component on the right.

**The Runnable Interface**

> The underlying protocol that makes LCEL work. Almost every core LangChain component (PromptTemplates, LLMs, OutputParsers) is a "Runnable." Because they all share this same interface, they all support standard methods like `.invoke()`, `.stream()`, and `.batch()`.

---

### 💻 Code Walkthrough: LCEL in Action

Here is a breakdown of how LCEL and Runnables work in a standard summarization script:

```python
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI

# 1. Environment Setup
load_dotenv()
```

- **What it does:** Loads your API keys (like `AZURE_OPENAI_API_KEY` and endpoint URLs) from a hidden `.env` file into your system environment so LangChain can authenticate securely.

```python
def main():
  # 2. Context Variables
  information = """... [Target text to be summarized] ..."""

  summary_prompt = """
    Given the following information, summarize it in a few sentences and 2 intresting
    facts about the person.
    {information} """

  # 3. The First Runnable (PromptTemplate)
  summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_prompt
    )

```

- **What it does:** We define our raw text (`information`) and our instructions (`summary_prompt`). We then wrap this into a `PromptTemplate`. This template is our **first Runnable**. When invoked, it expects a dictionary with the key `"information"`.

```python
  # 4. The Second Runnable (LLM)
  llm = AzureChatOpenAI(
        azure_deployment="gpt-4o",  # Must match your Foundry deployment name exactly
        temperature=0.7
    )

```

- **What it does:** Initializes the connection to a managed enterprise model. Instead of the public OpenAI API, this points specifically to a model hosted in an Azure AI Foundry environment. This `llm` object is our **second Runnable**. `temperature=0.7` gives the model a balance between accuracy and creative phrasing.

```python
  # 5. LCEL (The Pipe Operator)
  chain = summary_prompt_template | llm

```

- **What it does:** This is the magic of LCEL. It creates a unified pipeline. It tells LangChain: _"Take the PromptTemplate, fill in the variables to create a string, and immediately pipe (`|`) that formatted string into the Azure LLM."_

```python
  # 6. Execution via Runnable Interface
  response = chain.invoke({"information": information})
  print(response.content)

if __name__ == "__main__":
  main()

```

- **What it does:** Because our new `chain` is also a Runnable, we trigger it using the standard `.invoke()` method. We pass in the required dictionary. The response comes back as an `AIMessage` object, and we print its raw `.content`.

---

## 🧠 Interview Prep: LCEL & Runnables

### Practice Questions

While you _could_ write manual Python code (e.g., `formatted_prompt = template.format(data); response = llm.predict(formatted_prompt)`), LCEL provides massive production benefits out of the box.

| Feature                | Manual Python                               | LCEL                                  |
| ---------------------- | ------------------------------------------- | ------------------------------------- |
| **Streaming**          | Requires complex custom generator loops     | Native support (`chain.stream()`)     |
| **Async Support**      | Requires rewriting functions to `async def` | Native support (`chain.ainvoke()`)    |
| **Parallel Execution** | Requires threading/multiprocessing          | Native support via `RunnableParallel` |
| **Observability**      | Manual logging required                     | Auto-injects perfectly into LangSmith |

**How to say it in an interview:**
_"LCEL abstracts away the boilerplate of orchestrating data flow. By using the pipe operator, I instantly get streaming, asynchronous capabilities, and automatic LangSmith tracing for free, without having to write separate logic for each."_

The Runnable interface is a standardized contract in LangChain. If a class implements this interface, it guarantees it can be chained together with other Runnables.

The core methods you need to know are:

1. **`invoke()`:** Calls the chain on a single input (Standard synchronous execution).
2. **`stream()`:** Streams back chunks of the response as they are generated (Crucial for UI responsiveness).
3. **`batch()`:** Calls the chain on an array of inputs simultaneously (Great for processing lists of data efficiently).

> [!TIP]
> **Interview hack:** Mention that every synchronous method has an asynchronous equivalent (`ainvoke`, `astream`, `abatch`). This shows you are thinking about high-performance, non-blocking backend architecture (like FastAPI).

Understanding the data types flowing through the pipe is critical for debugging.

1. **`prompt` output:** The prompt template outputs a `PromptValue` (or a formatted string).
2. **`model` input / output:** The LLM receives the `PromptValue` and outputs an `AIMessage` (which contains the raw text and metadata).
3. **`parser` input / output:** The parser receives the `AIMessage`, extracts the text, and outputs a **Structured Python Object** (like a dictionary, list, or Pydantic model).
