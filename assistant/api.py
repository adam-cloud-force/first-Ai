from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .nlp import TextGenerator

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

app = FastAPI(title="AI Assistant API")
_text_generator: TextGenerator | None = None


def get_text_generator() -> TextGenerator:
	global _text_generator
	if _text_generator is None:
		_text_generator = TextGenerator()
	return _text_generator


class ChatRequest(BaseModel):
	prompt: str
	max_new_tokens: int = 128
	temperature: float = 0.7


class ChatResponse(BaseModel):
	response: str


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
	generator = get_text_generator()
	text = generator.generate(req.prompt, max_new_tokens=req.max_new_tokens, temperature=req.temperature)
	return ChatResponse(response=text)


class TodoItem(BaseModel):
	id: int
	title: str
	completed: bool = False


@app.get("/todos", response_model=List[TodoItem])
async def list_todos():
	return _load_json(TODOS_PATH, [])


class TodoCreate(BaseModel):
	title: str


@app.post("/todos", response_model=TodoItem)
async def add_todo(todo: TodoCreate):
	todos_raw = _load_json(TODOS_PATH, [])
	new_id = (max((t["id"] for t in todos_raw), default=0) + 1)
	item = {"id": new_id, "title": todo.title, "completed": False}
	todos_raw.append(item)
	_save_json(TODOS_PATH, todos_raw)
	return item


@app.patch("/todos/{todo_id}", response_model=TodoItem)
async def update_todo(todo_id: int, completed: Optional[bool] = None, title: Optional[str] = None):
	todos_raw = _load_json(TODOS_PATH, [])
	for t in todos_raw:
		if t["id"] == todo_id:
			if completed is not None:
				t["completed"] = completed
			if title is not None:
				t["title"] = title
			_save_json(TODOS_PATH, todos_raw)
			return t
	raise HTTPException(status_code=404, detail="Todo not found")


@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
	todos_raw = _load_json(TODOS_PATH, [])
	new_list = [t for t in todos_raw if t["id"] != todo_id]
	if len(new_list) == len(todos_raw):
		raise HTTPException(status_code=404, detail="Todo not found")
	_save_json(TODOS_PATH, new_list)
	return {"ok": True}


class ReminderItem(BaseModel):
	id: int
	message: str
	due_at_iso: str


@app.get("/reminders", response_model=List[ReminderItem])
async def list_reminders():
	return _load_json(REMINDERS_PATH, [])


class ReminderCreate(BaseModel):
	message: str
	due_at_iso: str


@app.post("/reminders", response_model=ReminderItem)
async def add_reminder(reminder: ReminderCreate):
	reminders_raw = _load_json(REMINDERS_PATH, [])
	new_id = (max((r["id"] for r in reminders_raw), default=0) + 1)
	item = {"id": new_id, "message": reminder.message, "due_at_iso": reminder.due_at_iso}
	reminders_raw.append(item)
	_save_json(REMINDERS_PATH, reminders_raw)
	return item


@app.delete("/reminders/{reminder_id}")
async def delete_reminder(reminder_id: int):
	reminders_raw = _load_json(REMINDERS_PATH, [])
	new_list = [r for r in reminders_raw if r["id"] != reminder_id]
	if len(new_list) == len(reminders_raw):
		raise HTTPException(status_code=404, detail="Reminder not found")
	_save_json(REMINDERS_PATH, new_list)
	return {"ok": True}


class CalcRequest(BaseModel):
	expression: str


class CalcResponse(BaseModel):
	result: float | int | str


@app.post("/calc", response_model=CalcResponse)
async def calc(req: CalcRequest):
	allowed_names = {k: v for k, v in vars(__import__("math")).items() if not k.startswith("__")}
	allowed_names.update({"abs": abs, "round": round})
	try:
		result = eval(req.expression, {"__builtins__": {}}, allowed_names)
		return CalcResponse(result=result)
	except Exception as e:  # noqa: BLE001
		raise HTTPException(status_code=400, detail=str(e))


class ConvertRequest(BaseModel):
	value: float
	from_unit: str
	to_unit: str


class ConvertResponse(BaseModel):
	value: float
	from_unit: str
	to_unit: str
	converted: float


@app.post("/convert", response_model=ConvertResponse)
async def convert(req: ConvertRequest):
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
		if req.from_unit in units and req.to_unit in units:
			return req.value * units[req.from_unit] / units[req.to_unit]
		return None

	ans = _convert(length)
	if ans is None:
		ans = _convert(weight)
	if ans is None:
		raise HTTPException(status_code=400, detail="Unsupported unit conversion")
	return ConvertResponse(value=req.value, from_unit=req.from_unit, to_unit=req.to_unit, converted=ans)