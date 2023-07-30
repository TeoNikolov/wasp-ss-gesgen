# Copyright 2023 by Teodor Nikolov.
# All rights reserved.
# This file is part of the WASP Summer School 2023 Gesture Generation Application,
# and is released under the GPLv3 License. Please see the LICENSE
# file that should have been included as part of this package.

import os
from pathlib import Path
import uuid

from fastapi import FastAPI, HTTPException, Response, Form, File, UploadFile
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles
from typing_extensions import Annotated

from celery import Celery

celery_workers = Celery(
	"tasks",
	broker=os.environ["CELERY_BROKER_URL"],
	backend=os.environ["CELERY_RESULT_BACKEND"],
)

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

@app.post("/generate_bvh/", status_code=202)
async def generate_bvh(
	style : str = Form(...),
	audio : UploadFile = File(...),
	temperature : float = Form(...)
):
	if len(style) == 0:
		raise HTTPException(status_code = 400, detail=f"Style name cannot be empty!")

	if audio.content_type != "audio/wav":
		raise HTTPException(status_code = 400, detail=f"Audio must be a WAV file! Got {audio.content_type}")

	if temperature < 0 or temperature > 1:
		raise HTTPException(status_code = 400, detail=f"Temperature must be between 0 and 1! Got {temperature}")

	try:
		# save audio to shared storage
		audio_content = await audio.read()
		audio_filename = str(uuid.uuid4()) + ".wav"
		audio_filepath = "/shared_storage/" + audio_filename
		with open(audio_filepath, "wb") as out_audio_file:
			out_audio_file.write(audio_content)

		task_args = {
			"style": style,
			"audio_filepath": audio_filepath,
			"temperature": temperature
		}
		task = celery_workers.send_task("tasks.generate_bvh", kwargs=task_args)
		return "BVH generation started."
	except Exception:
		raise HTTPException(status_code = 500, detail="Failed to process audio file.")
