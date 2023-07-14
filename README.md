_Magik is an LLM output testing SDK + observability platform that helps you write tests and monitor your app in production_.
<br /><br />

# Overview

Reliability of output is one of the biggest challenges for people trying to use LLM apps in production.<br />

LLM responses are non-deterministic by nature. This makes it particularly challenging to use them for certain types of tasks:

- If you're building a AI assistant that helps answer legal questions, and you cannot afford to have hallucinations, or misinformation.
- If you're building a code generation AI, you might need to make sure the code is correct, and works as expected.
- If you're building a customer support agent, you might need to make it sure it responds with accurate answers in a specified format, and does not contain sensitive information like PII.

We are trying to solve these problems with a **test-driven approach towards LLM observability.**
<br /><br /><br />

# Use Cases

Who is this product meant for?

- If you're in the early stages of building an LLM app:
- If you have an LLM app in production
  <br /><br />

### If you're in the early stages of building an LLM app:

---

Test-driven development can speed up your development very nicely, and can help you engineer your prompts to be more robust.

For example, assuming your prompt looks like this:

```
You are an AI customer support chatbot. You are trying to help a customer named {name} who needs some information.

Answer his questions in a polite tone. Be as respectful as possible. Do not mention that you are an AI. Do not refer to the customer by any name other than {name}. Do not use his email address or customer ID number.
```

You can write tests like this:

```python
tests = [
  # Test that output does not contain restricted keywords
  {
      "description": "output does not contain restricted keywords",
      "eval_function": contains_none,
      "eval_function_args": [restricted_keywords],
      "prompt_vars": { name: "Sara" },
      "failure_labels": ["contains_restricted_words"],
  },
  # Test that output does not contain an email
  {
      "description": "output does not contain email",
      "eval_function": regex,
      "eval_function_args": [email_matcher],
      "prompt_vars": { name: "John" },
      "failure_labels": ["contains_email", "pii_leak", "critical"],
  }
]
```

<br /><br />

### If you have an LLM app in production:

---

You can use our **evaluation & monitoring platform** to:

- Observe the prompt, response pairs in production, and analyze response times, cost, token usage, etc for different prompts and date ranges.

- Evaluate your production responses against your own tests to get a quantifiable understanding of how well your LLM app is performing.

  - For example, You can run the tests you defined against the LLM responses you are getting in production to measure how your app is performing with real data.

- Filter by failure labels, severity, prompt, etc to identify different types of errors that are occurring in your LLM outputs.

See https://magiklabs.app for more details, or contact us at [hello@magiklabs.app](mailto:hello@magiklabs.app)

<br /><br />

### Upcoming Features

---

Soon, you will also be able to:

- Fail bad outputs before they get to your users.

  - For example, if the LLM response contains sensitive information like PII, you can detect that in real-time, and cut it off before it reaches the end user.

- Set up alerts to notify you about critical errors in production.

<br /><br />

# Platform

Contact us at [hello@magiklabs.app](mailto:hello@magiklabs.app) to get access to our LLM observability platform where you can run the tests you've defined here against your LLM responses in production.
