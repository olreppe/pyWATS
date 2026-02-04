# Agent-First Coding Workflow (Concise Playbook)

This playbook captures a practical, research-aligned workflow for working with AI coding agents (e.g. Copilot / ChatGPT agents) in real projects.

The goal is speed and solution quality without over-constraining the first pass.

---

## Core principle

Do not try to fully specify the correct solution up front.

Let the agent explore first, then apply strong constraints during review and repair.

This reliably produces better momentum and avoids brittle, over-directed prompts.

---

## Why this works (short)

Language models are very sensitive to framing.

Exploratory prompts encourage breadth and initiative.
Restrictive prompts early on increase the chance of:
- misinterpreting constraints
- resolving conflicting instructions incorrectly
- producing overly narrow or safe solutions

Research consistently shows that:
generate → critique → revise
outperforms one-shot prompting.

---

## Recommended loop

### 1. Exploration pass (breadth first)

Purpose: produce a working, reasonable first solution quickly.

Prompt pattern:

- Make a first pass.
- Choose sensible defaults if something is underspecified.
- Keep going instead of stopping for clarification.

Do not include heavy constraints here.

---

### 2. Critique pass (hard constraints)

Purpose: surface real problems, not rewrite yet.

Ask explicitly for:

- correctness
- edge cases
- API / contract mismatches
- integration risks
- performance or scalability concerns
- security or robustness issues

Output should be a structured issue list.

---

### 3. Patch pass (minimal change)

Purpose: fix only what matters.

Prompt pattern:

- apply fixes for the listed issues
- keep the diff minimal
- explain behavior changes only

---

## Practical prompt skeleton

### Exploration

"""
Make a first implementation pass.
If something is unclear, choose a reasonable default and continue.
Focus on producing a complete working solution.
"""

### Critique

"""
Review the solution against:
- correctness
- edge cases
- API contracts
- integration with the existing codebase
- maintainability
List concrete issues only.
"""

### Patch

"""
Fix the listed issues.
Keep changes minimal.
Explain any behavior changes.
"""

---

## Guidance on tone and constraints

Small changes in wording and framing change output distribution.

In practice:

- early prompts should be permissive and exploratory
- later prompts should be precise and demanding

This separation of intent is more important than politeness or enthusiasm itself.

---

## Key takeaway

Use agents as fast explorers first and strict engineers second.

Trying to force correctness too early reduces both speed and solution quality.
