import os
import time
import subprocess
from pprint import pprint
from pathlib import Path

from pyvirtualdisplay import Display

from celery import Celery
from celery.utils.log import get_task_logger

# Start a display because Blender requires one for the rendering to work
Display().start()

WORKER_TIMEOUT = int(os.environ["CELERY_WORKER_TIMEOUT"])
logger = get_task_logger(__name__)

celery_app = Celery("tasks")
default_config = "celeryconfig"
celery_app.config_from_object(default_config)

class TaskFailure(Exception):
	pass

def call_blender_process(python_script, script_args):
    process = subprocess.Popen(
        [
            "/blender/blender-2.83.0-linux64/blender",
            "-b",
            "--python", python_script,
            "--"
        ] + script_args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return process

@celery_app.task(name="tasks.visualise", bind=True, hard_time_limit=WORKER_TIMEOUT)
def visualise(self,
              audio_filepath : str,
              motion_filepath : str
              ):

    if os.environ["SERVER_MODE"] == "1":
        output_path = "/shared_storage/"
    else:
        output_path = "/app/output/mp4/"
    output_name = str(Path(motion_filepath).stem)

    python_script = "/app/genea_visualizer/blender_render.py"
    script_args = [
         "--input", motion_filepath,
         "--duration", "9999",
         "--video",
         "--res_x", "640",
         "--res_y", "480",
         "-o", output_path + output_name
    ]
    print(f"Calling Blender + {python_script} with args:\n{script_args}", sep="\n")
    process = call_blender_process(python_script, script_args)

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
         "public": [output_name + ".mp4"],
         "internal": [output_path + output_name + ".mp4"]
    }
    return task_result
