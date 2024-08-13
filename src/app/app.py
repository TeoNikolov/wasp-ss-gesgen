# Copyright 2023 by Teodor Nikolov.
# All rights reserved.
# This file is part of the WASP Summer School 2023 Gesture Generation Application,
# and is released under the GPLv3 License. Please see the LICENSE
# file that should have been included as part of this package.

import os
from pathlib import Path
import uuid
from zipfile import ZipFile
import io
from io import BytesIO

from fastapi import FastAPI, HTTPException, Response, Form, File, UploadFile
from starlette.responses import FileResponse, StreamingResponse
from starlette.staticfiles import StaticFiles
from typing_extensions import Annotated

from celery import Celery
import celery.states as states

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

@app.get("/poses/")
async def get_poses(response: Response):
	search_path = Path("/app/data/start_poses/")
	if not search_path.is_dir():
		raise HTTPException(status_code = 404, detail="No poses found.")
	
	bvh_files = [file.stem for file in search_path.glob("*.bvh")]
	if len(bvh_files) == 0:
		raise HTTPException(status_code = 404, detail="No poses found.")
	
	return bvh_files

@app.get("/pose_images/{image_name}")
async def get_image(image_name: str):
    image_path = Path(f"/app/data/start_poses/images/{image_name}")
    if not image_path.is_file():
        raise HTTPException(status_code=404, detail="Image not found.")
    
    return FileResponse(image_path)

@app.post("/generate_bvh/", status_code=202)
async def generate_bvh(
	style : str = Form(...),
	audio : UploadFile = File(...),
	temperature : float = Form(...),
	seed : int = Form(...),
	pose : str = Form(...)
):
	if len(style) == 0:
		raise HTTPException(status_code = 400, detail=f"Style name cannot be empty!")

	if len(pose) == 0:
		raise HTTPException(status_code = 400, detail=f"Pose name cannot be empty!")

	if audio.content_type != "audio/wav":
		raise HTTPException(status_code = 400, detail=f"Audio must be a WAV file! Got {audio.content_type}")

	if temperature < 0 or temperature > 1:
		raise HTTPException(status_code = 400, detail=f"Temperature must be between 0 and 1! Got {temperature}")

	if not isinstance(seed, int):
		raise HTTPException(status_code = 400, detail=f"Seed is not an integer!")

	try:
		# save audio to shared storage
		audio_content = await audio.read()
		audio_filename = str(uuid.uuid4()) + ".wav"
		audio_filepath = "/shared_storage/" + audio_filename
		with open(audio_filepath, "wb") as out_audio_file:
			out_audio_file.write(audio_content)

		task_args = {
			"style": style,
			"pose": pose,
			"audio_filepath": audio_filepath,
			"temperature": temperature,
			"seed": seed
		}
		task = celery_workers.send_task("gesgen.tasks.generate_bvh", kwargs=task_args, queue="q_gesgen")
		return task.id
	except Exception:
		raise HTTPException(status_code = 500, detail="Failed to process audio file.")

@app.post("/visualise/", status_code=202)
async def visualise(
	audio : UploadFile = File(...),
	motion : UploadFile = File(...),
):
	# save audio to shared storage
	audio_content = await audio.read()
	audio_filename = str(uuid.uuid4()) + ".wav"
	audio_filepath = "/shared_storage/" + audio_filename
	with open(audio_filepath, "wb") as out_audio_file:
		out_audio_file.write(audio_content)

	# save motion to shared storage
	motion_content = await motion.read()
	motion_filename = str(uuid.uuid4()) + ".bvh"
	motion_filepath = "/shared_storage/" + motion_filename
	with open(motion_filepath, "wb") as out_motion_file:
		out_motion_file.write(motion_content)

	task_args = {
		"audio_filepath": audio_filepath,
		"motion_filepath": motion_filepath
	}
	task = celery_workers.send_task("visual.tasks.visualise", kwargs=task_args, queue="q_visual")
	return task.id

@app.post("/export_fbx/", status_code=202)
async def export_fbx(
	motion : UploadFile = File(...),
):
	# save motion to shared storage
	motion_content = await motion.read()
	motion_filename = str(uuid.uuid4()) + ".bvh"
	motion_filepath = "/shared_storage/" + motion_filename
	with open(motion_filepath, "wb") as out_motion_file:
		out_motion_file.write(motion_content)

	task_args = {
		"motion_filepath": motion_filepath
	}
	task = celery_workers.send_task("visual.tasks.export_fbx", kwargs=task_args, queue="q_visual")
	return task.id

@app.get("/job_id/{task_id}")
def check_job(task_id: str) -> str:
	res = celery_workers.AsyncResult(task_id)
	if res.state == states.PENDING:
		reserved_tasks = celery_workers.control.inspect().reserved()
		tasks = []
		if reserved_tasks:
			tasks_per_worker = reserved_tasks.values()
			tasks = [item for sublist in tasks_per_worker for item in sublist]
			found = False
			for task in tasks:
				if task["id"] == task_id:
					found = True
		result = {"jobs_in_queue": len(tasks)}
	elif res.state == states.FAILURE:
		result = str(res.result)
	elif res.state == states.SUCCESS:
		result = "Task completed successfully!"
	else:
		result = res.result
	return {"state": res.state, "result": result}

@app.get("/get_files/{task_id}")
def get_files(task_id: str):
	if os.environ["SERVER_MODE"] != "1":
		raise HTTPException(status_code = 405, detail=f"The app must be running in SERVER MODE to use this endpoint.")

	res = celery_workers.AsyncResult(task_id)
	if res.state != states.SUCCESS:
		raise HTTPException(status_code = 404, detail=f"Files are not available because the task has not finished.")

	location = res.result["download"]["location"]
	filename = res.result["download"]["filename"]
	mime_type = res.result["download"]["mime_type"]

	return FileResponse(
		path=location,
		headers={
			"Content-Disposition": f"attachment; filename=\"{filename}\"",
		},
		media_type=mime_type
	)
