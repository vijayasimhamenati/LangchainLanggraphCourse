## 📝 Prompt Templates in LangChain

Hardcoding prompts is messy. When building production AI applications, you need a safe, reproducible way to dynamically inject user inputs, maintain formatting, and manage your prompts as actual code. That is exactly what Prompt Templates do.

### Core Definitions

**PromptTemplate**

> The foundational class for creating dynamic text strings. It takes a template string with placeholders (like `{topic}`) and safely replaces them with user input before sending the final string to the LLM.

**ChatPromptTemplate**

> A specialized template designed specifically for Chat Models (like GPT-4 or Claude). Instead of a single flat string, it passes a structured list of messages, where each message has a specific "Role" (System, Human, or AI).

> [!NOTE]  
> If you are building anything modern, you will almost always use `ChatPromptTemplate` because most state-of-the-art models are fine-tuned for conversational roles rather than plain text completion.

---

## 🧠 Interview Prep: Prompt Templates

Here are the most common concepts you need to know regarding prompt management.

### Practice Questions

<details>
<summary><b>Q1: Why use LangChain's PromptTemplates instead of standard Python f-strings?</b> (Click to reveal)</summary>
<br>

At first glance, `f"Tell me a joke about {topic}"` seems easier. But for production systems, PromptTemplates provide essential safety and pipeline features that standard string formatting lacks.

| Feature         | Python f-strings                                     | LangChain PromptTemplates                         |
| :-------------- | :--------------------------------------------------- | :------------------------------------------------ | ------- |
| **Validation**  | Fails blindly at runtime if a variable is missing    | Validates all expected input variables upfront    |
| **Reusability** | Hard to save, share, or version control              | Can be serialized (saved and loaded as JSON/YAML) |
| **Partialing**  | Clunky to format some variables now and others later | Native support for `partial_variables`            |
| **Pipelines**   | Requires manual string passing                       | Pipes natively into chains (`template             | model`) |

**How to say it in an interview:**
_"f-strings are fine for quick scripts. But when I'm building an AI pipeline, PromptTemplates act as a strict contract. They validate that all required inputs are present before making an expensive API call, and they plug seamlessly into LangChain's execution graph."_

</details>

<details>
<summary><b>Q2: What are the different "Roles" used in a ChatPromptTemplate?</b> (Click to reveal)</summary>
<br>

Chat models don't just take raw text; they process an array of structured messages. You must assign roles to give the model context on how to behave.

1. **System Message:** The foundational instructions. Sets the persona, constraints, and rules (e.g., _"You are a senior database engineer. Reply only in SQL."_).
2. **Human (User) Message:** The actual query or input provided by the end-user.
3. **AI (Assistant) Message:** The model's previous responses. This is passed back to the model so it remembers the context of the conversation.

> [!TIP]  
> **Interview hack:** If an interviewer asks how to prevent "prompt injection" (where a user tries to trick the AI into ignoring instructions), mention that putting strict behavioral rules in the **System Message** is your first line of defense. Models are trained to prioritize System instructions over Human instructions.

</details>

<details>
<summary><b>Q3: What are "Partial Prompts" and when would you use them?</b> (Click to reveal)</summary>
<br>

**Partialing** a prompt means filling in _some_ of the variables immediately, while waiting to fill in the rest of the variables later down the pipeline.

**Common Use Case: Injecting data you don't want the user to worry about.**
If your prompt is: _"Today is {date}. Write an email to the user about {topic}."_

You don't want to calculate the `{date}` and pass it manually every single time you call the chain. You can bind the `{date}` variable to a function that automatically fetches the current time. This leaves only the `{topic}` variable required when actually running the chain.

</details>

---

## 🧱 Output Parsers in LangChain

Language models output raw, unstructured text. However, production applications usually require structured data (like JSON, a Python dictionary, or a specific database model). Output Parsers are the bridge that transforms raw LLM string responses into structured, programmatically usable objects.

### Core Definitions

**OutputParser**

> The base class responsible for taking a raw string or `BaseMessage` from an LLM and formatting it into a structured data type (like JSON, lists, or Pydantic objects).

**PydanticOutputParser**

> The most popular and robust parser in LangChain. It takes a Python Pydantic schema, automatically instructs the LLM to output data matching that schema, and validates the incoming response against it.

**OutputFixingParser**

> A wrapper parser used for error recovery. If the primary parser fails because the LLM made a syntax error (e.g., missing a comma in JSON), the `OutputFixingParser` automatically catches the error, sends the bad output and the error back to the LLM, and asks it to fix the formatting.

---

### ⚙️ How It Works Internally (Under the Hood)

When you invoke a chain containing an Output Parser (e.g., `prompt | model | parser`), LangChain executes a silent, two-step process:

1. **Instruction Injection:** When the prompt is compiled, the parser secretly injects formatting instructions into the end of your prompt. For example, if you use a JSON parser, it appends text like: _"The output must be formatted as a JSON object matching this schema: ... Do not include any markdown wrappers."_
2. **Post-Processing & Validation:** Once the LLM returns the raw string response, the parser intercepts it. It cleans up minor artifacts (like stripping whitespace or markdown ```json code blocks) and passes it to a validator. If validation passes, it returns the structured object. If it fails, it raises a `OutputParserException`.

---

## 🧠 Interview Prep: Output Parsers

Review these high-frequency questions to confidently discuss data structuring and error handling in an interview.

### Practice Questions

<details>
<summary><b>Q1: Why use an Output Parser instead of just asking the LLM to "return JSON"?</b> (Click to reveal)</summary>
<br>

Simply telling an LLM to "return JSON" is highly unreliable in production. Models frequently append conversational text (e.g., _"Sure, here is your JSON:"_) or make minor syntax errors that break standard parsers like Python's `json.loads()`.

**Advantages of LangChain Output Parsers:**

- **Automated Prompting:** They dynamically generate complex schema instructions so you don't have to manually write formatting rules in your prompt.
- **Type Safety & Validation:** They guarantee that the output doesn't just look like JSON, but actively matches your required data types (e.g., validating that an age field is an integer, not a string).
- **Self-Healing:** They plug into error-correction chains that can automatically fix broken syntax without failing the entire user request.

**How to say it in an interview:**
_"Prompting an LLM to return JSON is only half the battle. In production, you need type guarantees. LangChain Output Parsers handle the hidden grunt work: injecting precise formatting schema constraints into the prompt, stripping out accidental markdown wrappers, and validating the keys and types before the data hits your backend logic."_

</details>

<details>
<summary><b>Q2: What is the difference between an Output Parser and OpenAI's native "Structured Outputs" (or JSON Mode)?</b> (Click to reveal)</summary>
<br>

| Feature            | OpenAI Structured Outputs                      | LangChain Output Parsers                                         |
| :----------------- | :--------------------------------------------- | :--------------------------------------------------------------- |
| **Vendor Lock-in** | Works only with supported OpenAI models        | Vendor-agnostic (works with Claude, Ollama, Llama, etc.)         |
| **Enforcement**    | Enforced at the API level via grammar sampling | Enforced post-generation via software validation                 |
| **Flexibility**    | Rigid schema requirements                      | Can parse complex structures, CSV lists, or custom text patterns |

> [!TIP]
> **Interview hack:** A great architectural point to bring up is hybrid design. You can tell the interviewer: _"For maximum reliability with OpenAI models, I combine both. I enable JSON mode at the model level to force JSON generation, and wrap it in a LangChain Pydantic parser to handle the validation and Python type-casting."_

</details>

<details>
<summary><b>Q3: How do you handle a scenario where an LLM fails to output valid structured data?</b> (Click to reveal)</summary>
<br>

You should never let a parsing error crash an application. LangChain provides two primary patterns to handle parsing failures gracefully:

1. **`OutputFixingParser` (The Auto-Fix Pattern):**
   If the initial parse fails, this parser takes the broken output, combines it with the original schema and the parsing error message, and sends a quick follow-up prompt to a model (often a cheaper, faster model) saying: _"You generated this invalid output. Fix the syntax error according to this exception."_

2. **Fallbacks (The Plan B Pattern):**
   Using LCEL (LangChain Expression Language), you can append a `.with_fallbacks()` block to your chain. If the primary structured chain throws an exception, it seamlessly switches to an alternative chain—such as a chain that uses a larger, smarter model or falls back to a safe default database record.

</details>
