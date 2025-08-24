from __future__ import annotations

from typing import List

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


class TextGenerator:
	def __init__(self, model_name: str = "google/flan-t5-small", device: str | None = None) -> None:
		self.model_name = model_name
		self.tokenizer = AutoTokenizer.from_pretrained(model_name)
		self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
		self.device = device
		if device:
			self.model.to(device)

	def generate(
		self,
		prompt: str,
		max_new_tokens: int = 128,
		temperature: float = 0.7,
		min_new_tokens: int = 20,
		num_beams: int = 4,
	) -> str:
		inputs = self.tokenizer(prompt, return_tensors="pt")
		if self.device:
			inputs = {k: v.to(self.device) for k, v in inputs.items()}
		outputs = self.model.generate(
			**inputs,
			do_sample=False if num_beams > 1 else True,
			temperature=temperature,
			max_new_tokens=max_new_tokens,
			min_new_tokens=min_new_tokens,
			num_beams=num_beams,
			early_stopping=True,
		)
		text: List[str] = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)
		return text[0].strip() if text else ""