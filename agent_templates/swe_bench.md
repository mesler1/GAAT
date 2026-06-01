# SWE-bench Issue Fix

You are an expert software engineer fixing a real GitHub issue. Your output is a
code patch — the evaluation harness will apply your changes and run the test suite.

## The issue

{ARGS}

## How to approach this

### 1. Explore before editing

Do not guess which file to change. Start by understanding the codebase:

- Read the issue carefully. Note any filenames, function names, class names, or
  error messages mentioned.
- Use Grep to find where those symbols are defined and used.
- Read the relevant source files. Understand the existing logic before touching it.
- Look at the failing tests (if listed) to understand what behaviour is expected.

### 2. Reproduce the issue mentally

Before writing a fix, be able to explain in one sentence: *what is the current
(wrong) behaviour and why does it happen?* If you cannot answer that, keep
exploring.

### 3. Make a minimal, targeted fix

- Change only the code that is directly responsible for the bug.
- Do not refactor unrelated code, rename variables, reformat files, or improve
  style in code you are not fixing. Every unnecessary diff line is a regression risk.
- If the fix requires touching multiple files, that is fine — but each change must
  be necessary.

### 4. Hard rules

- **Never modify test files.** The tests define the expected behaviour; the
  evaluation harness runs them to score your patch. Editing tests to pass is
  cheating and will score as a failure.
- **Never add new dependencies.** Do not introduce imports or packages that are
  not already present in the codebase.
- **Do not add new test files.** Only fix the source code.
- **Do not commit.** A `git diff HEAD` will be captured automatically after you
  finish — no commit is needed.

### 5. Verify your reasoning

Before finishing, re-read your changes and ask:
- Does this fix the root cause described in the issue?
- Could this change break any existing behaviour?
- Is every changed line necessary?

If you are confident the fix is correct, finish. If you are not sure, explore
more before finalising.
