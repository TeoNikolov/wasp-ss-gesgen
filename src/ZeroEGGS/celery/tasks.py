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
def generate_bvh(self, style : str, audio_filepath : str, temperature : float):
    python_script = "/app/ZeroEGGS/ZEGGS/generate.py"
    output_path = "/app/output/bvh/"
    output_name = str(Path(audio_filepath).stem)
    script_args = [
        "-o", "/app/data/gesgen_options_v1.json",
        "-s", f"/app/data/styles/{style}.bvh",
        "-a", audio_filepath,
        "-p", output_path,
        "-r", "1234",
        "-fp", "/app/data/start_poses/037_Flirty_1_x_1_0.bvh",
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

    return [output_path + output_name + ".bvh", output_path + output_name + ".wav"]

@celery_app.task(name="tasks.test", bind=True, hard_time_limit=WORKER_TIMEOUT)
def test_task(self):
    for i in range(10):
        print("PRINT " + str(i))
        time.sleep(1)
    print(logger.info(self.request.id))
    print("DONE!")
    return 999