_Magik is an LLM output testing SDK + observability platform that helps you write tests and monitor your app in production_.
<br /><br />

# Overview

Reliability of output is one of the biggest challenges for people trying to use LLM apps in production.<br />

Since LLM outputs are non-deterministic, it’s very hard to measure how good the output is.

Eyeballing the responses from an LLM can work in development, but it’s not a great solution.

> _In production, it’s virtually impossible to eyeball thousands of responses. Which means you have very little visibility into how well your LLM is performing._

- Do you know when your LLM app is hallucinating?
- How do you know how well it's _really_ performing?
- Do you know how often it’s producing a critically bad output?
- How do you know what your users are seeing?
- How do you measure how good your LLM responses are? And if you can’t measure it, how do you improve the accuracy?

<br />

> If these sound like problems to you (today or in the future), please reach out to us at hello@magiklabs.app. We’d love to hear more!

<img width="1576" alt="llm-screenshot-1" src="https://github.com/magiklabs/magik-sdk/assets/7515552/bc87aefa-505f-4732-84cd-b7fe57857850">

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
Create some marketing copy for a tweet of less than 280 characters for my app {app_name}.

My app helps people generate sales emails using AI.

Make sure the marketing copy contains a complete and valid link to my app.

Here is the link to my app: https://magiklabs.app.
```

You can write tests like this:

```python
from magik.evaluators import (
    contains_none,
    contains_link,
    contains_valid_link,
    is_positive_sentiment,
    length_less_than,
)

# Local context - this is used as the "ground truth" data that you can compare against in your tests
test_context = {}

# Define tests here
def define_tests(context: dict):
    return [
        {
            "description": "output contains a link",
            "eval": contains_link(),
            "prompt_vars": {
                "app_name": "Uber",
            },
            "failure_labels": ["bad_response_format"],
        },
        {
            "description": "output contains a valid link",
            "eval": contains_valid_link(),
            "prompt_vars": {
                "app_name": "Magik",
            },
            "failure_labels": ["bad_response_format"],
        },
        {
            "description": "output sentiment is positive",
            "eval": is_positive_sentiment(),
            "prompt_vars": {
                "app_name": "Lyft",
            },
            "failure_labels": ["negative_sentiment"],
        },
        {
            "description": "output length is less than 280 characters",
            "eval": length_less_than(280),
            "prompt_vars": {
                "app_name": "Facebook",
            },
            "failure_labels": ["negative_sentiment", "critical"],
        },
        {
            "description": "output does not contain hashtags",
            "eval": contains_none(['#']),
            "prompt_vars": {
                "app_name": "Datadog",
            },
            "failure_labels": ["bad_response_format"],
        },
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
