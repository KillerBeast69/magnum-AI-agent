# A Toy AI Agent with Gemini

If you've ever used OpenCode, Cursor, or Claude Code as an "agentic" AI tool, you'll understand what this project is.

This is a toy version of Claude Code using Google's Gemini API! As long as you have an LLM at your disposal, it's actually surprisingly simple to build a (somewhat) effective custom agent.

## What Does the Agent Do?

It's a CLI tool that:

1. **Accepts a coding task** (e.g., "strings aren't splitting in my app, pweeze fix 🥺👉🏽👈🏽").
2. **Chooses from a set of predefined functions** to work on the task. For example:
   * Scan the files in a directory
   * Read a file's contents
   * Overwrite a file's contents
   * Execute the Python interpreter on a file
3. **Repeats step 2** until the task is complete (or it fails miserably, which is possible).

For example, I had a buggy calculator app, so I used my agent to fix the code:

```bash
> uv run main.py "fix my calculator app, it's not starting correctly"
# Calling function: get_files_info
# Calling function: get_file_content
# Calling function: write_file
# Calling function: run_python_file
# Calling function: write_file
# Calling function: run_python_file
# Final response:
# Great! The calculator app now seems to be working correctly. The output shows the expression and the result in a formatted way.
```

## Prerequisites

* Python 3.10+ installed
* The `uv` project/package manager ([installation docs](https://docs.astral.sh/uv/))
* Access to a Unix-like shell (e.g., `zsh` or `bash`)
