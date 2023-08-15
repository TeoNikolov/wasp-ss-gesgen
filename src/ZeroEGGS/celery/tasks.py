import os
import time
import subprocess
from pprint import pprint
from pathlib import Path

from celery import Celery
from celery.utils.log import get_task_logger

WORKER_TIMEOUT = int(os.environ["CELERY_WORKER_TIMEOUT"])
logger = get_task_logger(__name__)

celery_app = Celery("tasks")
default_config = "celeryconfig"
celery_app.config_from_object(default_config)

class TaskFailure(Exception):
	pass

def call_python_process(python_script, script_args):
    process = subprocess.Popen(
        [
            "python3.8",
            python_script,
        ] + script_args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return process

@celery_app.task(name="tasks.generate_bvh", bind=True, hard_time_limit=WORKER_TIMEOUT)
def generate_bvh(self,
                 style : str,
                 pose : str,
                 audio_filepath : str,
                 temperature : float,
                 seed: int
                 ):

    if os.environ["SERVER_MODE"] == "1":
        output_path = "/shared_storage/"
    else:
        output_path = "/app/output/bvh/"
    output_name = str(Path(audio_filepath).stem)

    python_script = "/app/ZeroEGGS/ZEGGS/generate.py"
    script_args = [
        "-o", "/app/data/gesgen_options_v1.json",
        "-s", f"/app/data/styles/{style}.bvh",
        "-a", audio_filepath,
        "-p", output_path,
        "-r", str(seed),
        "-fp", f"/app/data/start_poses/{pose}.bvh",
        "-n", output_name,
        "-t", str(temperature)
    ]
    print(f"Calling {python_script} with args:\n{script_args}", sep="\n")
    process = call_python_process(python_script, script_args)

    # Debug prints
    # while True:
    #      line = process.stdout.readline()
    #      if not line:
    #           break
    #      print(line)

    process.wait()
    print(f"Process finished with code {process.returncode}.")
    if process.returncode != 0:
        raise TaskFailure(process.stderr.read().decode("utf-8"))

    # These are useful ONLY in SERVER_MODE with "shared_storage"
    task_result = {
         "download": {
            "location": output_path + output_name + ".bvh",
            "filename": "motion.bvh",
            "mime_type": "application/octet-stream"
         }
    }
    return task_result
