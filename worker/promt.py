def build_prompt(diff: str) -> str:
    return f"""
You are a senior software engineer.

Review this pull request diff.
Focus only on:
- Bugs
- Security issues
- Performance problems

Do NOT comment on formatting or naming.
Respond in Markdown.

Diff:
{diff}
"""
