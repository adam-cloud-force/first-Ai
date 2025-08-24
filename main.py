from __future__ import annotations

from pathlib import Path

import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, FileResponse
from fastapi import HTTPException

from assistant.api import app

# Mount static frontend under /web to avoid shadowing API routes
static_dir = Path("/workspace/web"); static_dir.mkdir(parents=True, exist_ok=True)
app.mount("/web-static", StaticFiles(directory=str(static_dir), html=False), name="static")

# Serve index.html explicitly and fallback for client routing
@app.get("/web/", include_in_schema=False)
async def web_root():
	index_path = static_dir / "index.html"
	if not index_path.exists():
		raise HTTPException(status_code=404, detail="index.html not found")
	return FileResponse(str(index_path))

@app.get("/web/{path:path}", include_in_schema=False)
async def web_catch_all(path: str):
	candidate = static_dir / path
	if candidate.exists() and candidate.is_file():
		return FileResponse(str(candidate))
	# Fallback to SPA index
	return FileResponse(str(static_dir / "index.html"))

# Redirect root to /web/
@app.get("/")
async def root_redirect():
	return RedirectResponse(url="/web/")

if __name__ == "__main__":
	uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)