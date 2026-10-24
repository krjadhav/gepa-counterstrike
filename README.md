# GEPA Counter Strike

There's emperical evidence that AI models can engage in "scheming" (=misaligned power-seeking. perhaps strategically pursuing some long-term goal that goes against our interests). Such models could use tactics such as faking alignment, acting incompetent, sabotaging work,

**Could we intercept these efforts? How can we handle risk from scheming?**

one approach is to use probability theory. essentially,

```text
P(doom ∩ scheming) = P(scheming) *  P(doom | scheming)
```

By focussing on `P(doom | scheming)`, we can probably be okay even if the model is scheming against us.

This idea is very similar to how orgs handle insider threats. Instead of just focussing on never hiring anyone who is compromised, assume employees could be compromised and set policies to mitigate the risks.

**What are some control techniques?**

Let’s say you have three types of workers:
- **untrusted models (U)**: low trust, low cost, high competence
- **humans (H)**: high trust, high cost, high competence
- **trusted models (T)**: high trust, low cost, low to moderate competence


**1/ Trusted Monitoring:**

```text
fn solve(problem):
  ans = U(problem)
  monitor_score = T(make_monitor_prompt(problem, ans))
  if monitor_score > THRESHOLD:
    if H(make_auditor_prompt(problem, ans)) == "bad":
      raise BadActionException()
  return ans
```

First, ask the stronger, untrusted model to write code. Then ask the weaker trusted model to review that code for suspicion. Human reviewers then inspect the highest-scoring submission.

Problem with this strategy is that weaker model tends to miss smart attacks.

**2/ Trusted Monitoring with Fallback:**

Using the trusted monitoring strategy

- set threshold to flag the most suspicous (say top 2%) and have humans review them
- discard the next most suspicious (say top 8%) of sketchy solutions and have the weaker model re-write them.
- use untrusted model's answers for the rest.

The tradeoff here is you sacrifice answer quality on the fraction of tasks a weaker model takes up. However, it drastically reduces danger.

**3/ Untrusted Monitoring with Collusion Busting**

You can ask another copy of the untrusted stronger model to review the answer. The problem with this strategy is it's possible for them to coordinate and lie.

The countermeasure is to remove any signs of collusion. A trusted model could paraphrase or mask the content to remove secret coordination signals from an untrusted reviewer.
