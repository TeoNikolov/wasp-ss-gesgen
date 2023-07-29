# Copyright 2023 by Teodor Nikolov.
# All rights reserved.
# This file is part of the WASP Summer School 2023 Gesture Generation Application,
# and is released under the GPLv3 License. Please see the LICENSE
# file that should have been included as part of this package.

from fastapi import FastAPI, HTTPException, Response
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()	
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def home(response: Response):
	return FileResponse("./index.html")

@app.get("/styles/")
async def get_styles(response: Response):
	search_path = Path("/app/data/styles/")
	if not search_path.is_dir():
		raise HTTPException(status_code = 404, detail="No styles found.")
	
	bvh_files = [file.stem for file in search_path.glob("*.bvh")]
	if len(bvh_files) == 0:
		raise HTTPException(status_code = 404, detail="No styles found.")
	
	return bvh_files
