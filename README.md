_Magik is an LLM output testing SDK + observability platform that helps you write tests and monitor your app in production_.
<br /><br />

# Overview

Reliability of output is one of the biggest challenges for people trying to use LLM apps in production.<br />

Since LLM outputs are non-deterministic, it’s very hard to measure how good the output is.

Eyeballing the responses from an LLM can work in development, but it’s not a great solution. 

> _In production, it’s virtually impossible to eyeball thousands of responses. Which means you have very little visibility into how well your LLM is performing._

- Do you know when your LLM app is hallucinating?
- How do you know how well it's *really* performing?
- Do you know how often it’s producing a critically bad output?
- How do you know what your users are seeing?
- How do you measure how good your LLM responses are? And if you can’t measure it, how do you improve the accuracy?

<br />

> If these sound like problems to you (today or in the future), please reach out to us at hello@magiklabs.app. We’d love to hear more!

<img width="1576" alt="llm-screenshot-1" src="https://github.com/magiklabs/magik-sdk/assets/7515552/2027dbda-d725-4afa-b975-f8976bb1a1df">

<br /><br /><br />


# Documentation
`pip install magik`

See https://docs.magiklabs.app for instructions on how to write and run tests.

- [Overview](https://docs.magiklabs.app/)
- [Quick Start](https://docs.magiklabs.app/quick-start)
- [Writing Tests](https://docs.magiklabs.app/reference/writing-tests)
  - [Evaluator Functions](https://docs.magiklabs.app/reference/writing-tests/evaluator-functions)
  - [What kind of tests can I write](https://docs.magiklabs.app/reference/writing-tests/what-kind-of-tests-can-i-write)
  - [How does the LLM grader work?](https://docs.magiklabs.app/reference/writing-tests/how-does-the-llm-grader-work)
- [Running Tests](https://docs.magiklabs.app/reference/running-tests)
- [Deploying Tests](https://docs.magiklabs.app/reference/deploying-tests)
- [Logging your production data](https://docs.magiklabs.app/reference/logging-your-production-data)

<br />

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

Answer his questions in a polite tone.

Be as respectful as possible. Do not mention that you are an AI.

Do not refer to the customer by any name other than {name}.

Do not use his email address or customer ID number.
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
      "eval_function": not_contains_email,
      "eval_function_args": [],
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
