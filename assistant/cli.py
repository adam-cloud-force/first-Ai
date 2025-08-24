from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional

import typer
from dateutil import parser as date_parser
from rich.console import Console
from rich.table import Table

from .nlp import TextGenerator

app = typer.Typer(help="Basic AI assistant CLI")
console = Console()
DATA_DIR = Path("/workspace/data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

TODOS_PATH = DATA_DIR / "todos.json"
REMINDERS_PATH = DATA_DIR / "reminders.json"


def _load_json(path: Path, default):
	if not path.exists():
		return default
	with path.open("r", encoding="utf-8") as f:
		return json.load(f)


def _save_json(path: Path, data) -> None:
	with path.open("w", encoding="utf-8") as f:
		json.dump(data, f, indent=2)


@dataclass
class Todo:
	id: int
	title: str
	completed: bool = False


@dataclass
class Reminder:
	id: int
	message: str
	due_at_iso: str

	@property
	def due_at(self) -> datetime:
		return datetime.fromisoformat(self.due_at_iso)


@app.command()
def chat(prompt: str, max_new_tokens: int = 128, temperature: float = 0.7):
	"""Chat with the local model (FLAN-T5-small)"""
	generator = TextGenerator()
	response = generator.generate(prompt, max_new_tokens=max_new_tokens, temperature=temperature)
	console.print(f"[bold cyan]You:[/] {prompt}")
	console.print(f"[bold green]AI:[/] {response}")


@app.command()
def todo(action: str = typer.Argument(..., help="add|list|done|delete"), title: Optional[str] = typer.Argument(None), todo_id: Optional[int] = typer.Option(None, "--id", help="Todo id for done/delete")):
	"""Manage todos stored in JSON."""
	todos_raw = _load_json(TODOS_PATH, [])
	todos: List[Todo] = [Todo(**t) for t in todos_raw]

	def _next_id() -> int:
		return (max((t.id for t in todos), default=0) + 1)

	if action == "add":
		if not title:
			raise typer.BadParameter("Title is required for add")
		new_todo = Todo(id=_next_id(), title=title)
		todos.append(new_todo)
		_save_json(TODOS_PATH, [asdict(t) for t in todos])
		console.print(f"Added todo #{new_todo.id}: {new_todo.title}")
	elif action == "list":
		table = Table(title="Todos")
		table.add_column("ID")
		table.add_column("Title")
		table.add_column("Completed")
		for t in todos:
			table.add_row(str(t.id), t.title, "✅" if t.completed else "❌")
		console.print(table)
	elif action == "done":
		if todo_id is None:
			raise typer.BadParameter("--id is required for done")
		for t in todos:
			if t.id == todo_id:
				t.completed = True
				break
		_save_json(TODOS_PATH, [asdict(t) for t in todos])
		console.print(f"Marked todo #{todo_id} as done")
	elif action == "delete":
		if todo_id is None:
			raise typer.BadParameter("--id is required for delete")
		todos = [t for t in todos if t.id != todo_id]
		_save_json(TODOS_PATH, [asdict(t) for t in todos])
		console.print(f"Deleted todo #{todo_id}")
	else:
		raise typer.BadParameter("Unknown action. Use add|list|done|delete")


@app.command()
def reminder(action: str = typer.Argument(..., help="add|list|delete"), message: Optional[str] = typer.Argument(None), at: Optional[str] = typer.Option(None, "--at", help="Natural date/time e.g. 'tomorrow 5pm'"), reminder_id: Optional[int] = typer.Option(None, "--id")):
	"""Manage reminders stored in JSON."""
	reminders_raw = _load_json(REMINDERS_PATH, [])
	reminders: List[Reminder] = [Reminder(**r) for r in reminders_raw]

	def _next_id() -> int:
		return (max((r.id for r in reminders), default=0) + 1)

	if action == "add":
		if not message:
			raise typer.BadParameter("Message is required for add")
		if not at:
			raise typer.BadParameter("--at is required, e.g., 'in 2 hours' or '2025-08-01 17:00'")
		parsed_dt = date_parser.parse(at, fuzzy=True, default=datetime.now())
		new_r = Reminder(id=_next_id(), message=message, due_at_iso=parsed_dt.isoformat())
		reminders.append(new_r)
		_save_json(REMINDERS_PATH, [asdict(r) for r in reminders])
		console.print(f"Added reminder #{new_r.id} for {parsed_dt:%Y-%m-%d %H:%M}")
	elif action == "list":
		table = Table(title="Reminders")
		table.add_column("ID")
		table.add_column("Message")
		table.add_column("Due At")
		for r in reminders:
			table.add_row(str(r.id), r.message, f"{r.due_at:%Y-%m-%d %H:%M}")
		console.print(table)
	elif action == "delete":
		if reminder_id is None:
			raise typer.BadParameter("--id is required for delete")
		reminders = [r for r in reminders if r.id != reminder_id]
		_save_json(REMINDERS_PATH, [asdict(r) for r in reminders])
		console.print(f"Deleted reminder #{reminder_id}")
	else:
		raise typer.BadParameter("Unknown action. Use add|list|delete")


@app.command()
def calc(expression: str):
	"""Evaluate a simple math expression safely."""
	allowed_names = {k: v for k, v in vars(__import__("math")).items() if not k.startswith("__")}
	allowed_names.update({"abs": abs, "round": round})
	try:
		result = eval(expression, {"__builtins__": {}}, allowed_names)  # noqa: S307 (controlled env)
		console.print(f"{expression} = [bold]{result}[/bold]")
	except Exception as e:  # noqa: BLE001
		console.print(f"[red]Error:[/] {e}")


@app.command()
def convert(value: float, from_unit: str, to_unit: str):
	"""Convert between units: length (m, km, mi), weight (g, kg, lb)."""
	length = {
		"m": 1.0,
		"km": 1000.0,
		"mi": 1609.34,
	}
	weight = {
		"g": 1.0,
		"kg": 1000.0,
		"lb": 453.592,
	}

	def _convert(units: dict[str, float]) -> Optional[float]:
		if from_unit in units and to_unit in units:
			return value * units[from_unit] / units[to_unit]
		return None

	ans = _convert(length)
	if ans is None:
		ans = _convert(weight)
	if ans is None:
		console.print("[red]Unsupported unit conversion[/red]")
		raise typer.Exit(1)
	console.print(f"{value} {from_unit} = [bold]{ans}[/bold] {to_unit}")


if __name__ == "__main__":
	app()