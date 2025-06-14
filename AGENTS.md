This repository contains Python utilities and data files used to generate Spanish verb conjugation flashcards for Anki.

General guidelines for Codex agents:

* **Encoding** – All code that reads or writes the CSV files must use UTF‑8 encoding. Many of the files contain Spanish accented characters.
* **Secrets** – Do not commit any API keys or `.env` files. The project uses `python-dotenv` to manage secrets locally.
* **Formatting** – Format all Python source files with `black` (line length 88). Run `black .` before committing. Include the `--check` flag in programmatic checks.
* **Linting & Syntax** – Run the unit tests with `pytest` and ensure Python files compile by running `python -m compileall -q .` as part of your checks.
* **Commit style** – Use short imperative commit messages (e.g. "Add helper for RAE scraper").
* **Large data** – Avoid committing large CSV or audio files unless explicitly requested.

Programmatic checks to run after making changes:

```bash
black --check .
python -m compileall -q .
pytest
```
