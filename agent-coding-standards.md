# Agent Coding Standards

# ALL CODE MUSE BE UP TO THIS STANDARD

## Follow Clean Code principles (Robert C. Martin) when writing code

- Specifically the correct order of functions

## No comments!

- Most likely there is absolutely no reason to add a comment
- If there is, it's probably a sign that the code is not clear

## Don't use dicts.

- str keys are red
- Use pydantic models instead

## Do not hallucinate

- If you are not sure, ask the user
- If you don't know the library, do the research

## Do not regress when moving code

- Make sure quality of moved code is at least as good as the original

## Don't make me ask you twice

- Follow all these rules
- Every time, all the time
- If it's hard, ask me how to solve it

## Only essential complexity, not accidental

- Use the simplest approach that works
- Question whether each line adds value or just complexity
