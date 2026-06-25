# 🤖 AI Coding Agent

> An autonomous AI agent that can read, write, and execute code — powered by Google Gemini.

![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat&logo=python)
![Gemini](https://img.shields.io/badge/Gemini-2.5_Flash-4285F4?style=flat&logo=google)
![Status](https://img.shields.io/badge/status-active-brightgreen)

---

## Overview

This project is an autonomous AI coding agent built around Google's Gemini 2.5 Flash model. Given a natural-language prompt, the agent enters an agentic loop — reasoning about what to do, calling sandboxed file system tools, observing results, and repeating — until it arrives at a final text response or reaches the 20-turn limit. All tool operations are restricted to a configurable working directory, preventing path traversal. The included `calculator/` sub-project serves as a realistic target environment for the agent to explore, modify, and run.

---

## Key Features

- 🔄 **Agentic Tool-Call Loop** — Up to 20 turns of Gemini tool calls and result observation per invocation; the loop terminates when the model emits a final text-only response
- 📁 **Four Sandboxed File System Tools** — All exposed to the model via `google.genai.types.FunctionDeclaration` schemas:
  - `get_files_info` — List directory contents with file size and `is_dir` flag
  - `get_file_content` — Read a file (truncated at 10,000 characters with a visible truncation notice)
  - `run_python_file` — Execute a `.py` file in a subprocess with optional CLI args; captures stdout, stderr, and exit codes; 30-second timeout
  - `write_file` — Write or overwrite a file, creating parent directories as needed
- 🔒 **Working Directory Sandbox** — Every tool resolves paths using `pathlib.Path.resolve()` and rejects any request targeting a path outside the working directory root before executing
- 🐍 **Subprocess Python Execution** — Scripts run via `subprocess.run()` with `capture_output=True`; non-zero exit codes, stdout, and stderr are all reported back to the model as structured results
- 🗣️ **Verbose Mode** — `--verbose` flag exposes prompt and response token counts, full function call arguments, and raw function response objects for inspection and debugging
- 🌡️ **Deterministic Responses** — Model is configured with `temperature=0` for reproducible, fact-grounded outputs

---

## Tech Stack

| Technology | Role |
|---|---|
| Python 3.13 | Primary language |
| `google-genai 1.12.1` | Gemini API client (function declarations, tool calls, content types) |
| `python-dotenv 1.1.0` | Loads `GEMINI_API_KEY` from `.env` |
| `subprocess` | Sandboxed Python file execution |
| `pathlib`, `os` | Secure path resolution and file operations |
| `argparse` | CLI argument parsing |

---

## Installation

**Prerequisites:** Python 3.13+, a Google Gemini API key, and either `uv` or `pip`

```bash
# 1. Clone the repository
git clone https://github.com/your-username/ai-agent.git
cd ai-agent

# 2. Install dependencies with uv (recommended)
uv sync

# Or with pip
pip install google-genai==1.12.1 python-dotenv==1.1.0

# 3. Add your Gemini API key
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

---

## Usage

```bash
# Ask the agent a question about the codebase
python main.py "How many files are in the calculator directory and what do they do?"

# Ask the agent to run existing tests
python main.py "Run the tests in tests.py and tell me if they all pass."

# Ask the agent to debug and fix code autonomously
python main.py "Run the tests. If any fail, read the relevant source files and fix them, then run tests again."

# Enable verbose mode to see all tool calls and token usage
python main.py --verbose "Read main.py and explain its architecture."
```

**Example verbose output:**
```
User prompt: Run the tests in tests.py and tell me if they all pass.
Prompt tokens: 312
Response tokens: 47
 - Calling function: run_python_file({'file_path': 'tests.py'})
-> {'result': 'STDOUT: .........\n----------------------------------------------------------------------\nRan 9 tests in 0.003s\n\nOK'}
All 9 tests pass successfully. The calculator handles addition, subtraction,
multiplication, division, operator precedence, and edge cases correctly.
```

**Run the integration test scripts:**
```bash
# Test each tool function independently
python test_get_files_info.py
python test_get_file_content.py
python test_run_python_file.py
python test_write_file.py
```

---

## Project Structure

```
ai-agent/
├── main.py              # Entry point: argparse, Gemini client setup, agentic loop
├── prompts.py           # system_prompt: defines the agent's role and available operations
├── config.py            # MAX_CHARS = 10000 (file read truncation limit)
│
├── functions/
│   ├── call_function.py      # Dispatches Gemini function_call objects to Python handlers;
│   │                         # injects working_directory="./calculator" into all calls
│   ├── get_files_info.py     # Lists dir contents; validates path stays within working dir
│   ├── get_file_content.py   # Reads file with MAX_CHARS cap and truncation notice
│   ├── run_python_file.py    # Executes .py files via subprocess; validates path + extension
│   └── write_file.py         # Writes content to file; creates parent dirs; validates path
│
├── calculator/               # Target working directory for the agent
│   ├── main.py               # CLI entry point for the calculator app
│   ├── tests.py              # unittest suite (9 test cases)
│   └── pkg/
│       ├── calculator.py     # Two-stack shunting-yard algorithm for +, -, *, /
│       └── render.py         # Formats results as indented JSON output
│
├── test_get_files_info.py    # Manual integration tests for get_files_info
├── test_get_file_content.py  # Manual integration tests for get_file_content
├── test_run_python_file.py   # Manual integration tests for run_python_file
├── test_write_file.py        # Manual integration tests for write_file
└── pyproject.toml
```

---

## Agentic Loop Architecture

```
User prompt
    │
    ▼
Build initial messages list
    │
    ▼ (up to 20 iterations)
┌─────────────────────────────────────────┐
│  client.models.generate_content()       │
│  model = gemini-2.5-flash               │
│  temperature = 0                        │
│  tools = [available_functions]          │
└───────────────────┬─────────────────────┘
                    │
         ┌──────────▼──────────┐
         │  function_calls?    │
         └──────┬──────┬───────┘
              YES      NO
               │        │
               ▼        ▼
         call_function  Print response.text
               │        and return
               ▼
    Append tool results to messages
               │
               └──────────────── next iteration
```

---

## Security Notes

- All tool functions call `Path.resolve()` and verify the result is relative to the resolved working directory before performing any I/O or execution.
- `run_python_file` enforces a `.py` extension check and a 30-second subprocess timeout.
- The working directory is hardcoded to `./calculator` in `call_function.py` and is never exposed to user input.

---

## Contributing

To add a new tool, implement the Python function in `functions/`, define its `types.FunctionDeclaration` schema, add it to `available_functions` in `functions/call_function.py`, and register it in `function_map`. All tool functions must accept `working_directory` as their first parameter and perform path traversal validation before any I/O.

---
