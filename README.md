# Basic AI Assistant (Beginner-friendly)

This project gives you hands-on experience building a simple AI assistant on your own computer. It uses a small open model (FLAN-T5-small) to generate text, plus handy tools (todos, reminders, calculator, unit converter) in a single command-line app.

## Quick start

1) Create a Python virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2) Try the CLI:

```bash
python -m assistant.cli --help
python -m assistant.cli chat "Explain gravity like I'm 10"
python -m assistant.cli todo add "Study Python 30 minutes"
python -m assistant.cli todo list
python -m assistant.cli reminder add "Drink water" --at "in 1 hour"
python -m assistant.cli calc "(2+3)*4"
python -m assistant.cli convert 5 km mi
```

Data saves to `/workspace/data` by default.

## How it works (high level)

- `assistant/nlp.py`: loads a small text generation model and turns a prompt into a reply.
- `assistant/cli.py`: command-line interface built with Typer; routes subcommands to features.
- JSON files store todos and reminders.

## Learning path (for a 13-year-old future AI engineer!)

- Day 1: Run the CLI, read `nlp.py`, and edit the `generate` parameters (max tokens, temperature). Observe differences.
- Day 2: Add a new command: `summarize` that takes a long text and returns a short summary using the same model.
- Day 3: Add a new unit to `convert` (e.g., Celsius/Fahrenheit). Write tests with `pytest`.
- Day 4: Replace the model with `distilbert-base-uncased` for classification and add a `sentiment` command.
- Day 5: Ship! Record a short demo video using the CLI.

## Tips

- Read errors carefully; they are your best teacher.
- Keep changes small and test often (`--help` for every command).
- Commit your work often if you use git.
