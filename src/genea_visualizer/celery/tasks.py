import os
import time
import subprocess
from pprint import pprint
from pathlib import Path

import ffmpeg

from pyvirtualdisplay import Display

from celery import Celery
from celery.utils.log import get_task_logger

# Start a display because Blender requires one for the rendering to work
Display().start()

WORKER_TIMEOUT = int(os.environ["CELERY_WORKER_TIMEOUT"])
logger = get_task_logger(__name__)

celery_app = Celery("visual")
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

def call_ffmpeg_process(video_file, audio_file, output_file):
    if ".mp4" not in video_file:
        raise TaskFailure("Only MP4 video stream is currently supported!")
    if ".wav" not in audio_file:
        raise TaskFailure("Only WAV audio stream is currently supported!")

    # FFMPEG CMD ARGS --> ["ffmpeg", "-i", video_file, "-i", audio_file, "-c:v", "copy", "-c:a", "aac", "-map", "0:v:0", "-map", "1:a:0", "-shortest", output_file]
    v_stream = ffmpeg.input(video_file)['v']
    a_stream = ffmpeg.input(audio_file)['a']
    output_ffmpeg = ffmpeg.output(v_stream, a_stream, output_file, vcodec='copy', acodec='aac', **{'shortest': None, 'y': None})
    return ffmpeg.run(output_ffmpeg, capture_stdout=True, capture_stderr=True)

@celery_app.task(name="visual.tasks.visualise", bind=True, hard_time_limit=WORKER_TIMEOUT)
def visualise(self,
              audio_filepath : str,
              motion_filepath : str
              ):

    if os.environ["SERVER_MODE"] == "1":
        output_path = "/shared_storage/"
    else:
        output_path = "/app/output/mp4/"
    output_name_no_extension = str(Path(motion_filepath).stem)

    blender_output_filepath = output_path + output_name_no_extension + "_blender.mp4"
    python_script = "/app/genea_visualizer/blender_render.py"
    script_args = [
         "--input", motion_filepath,
         "--duration", "9999",
         "--video",
         "--res_x", "640",
         "--res_y", "480",
         "-o", blender_output_filepath
    ]
    print(f"Calling Blender + {python_script} with args:\n{script_args}", sep="\n")
    process = call_blender_process(python_script, script_args)

    # Without this, the Blender process will not exit properly
    while True:
         line = process.stdout.readline()
         if not line:
              break
        #  print(line)

    process.wait()
    print(f"Blender process finished with code {process.returncode}.")
    if process.returncode != 0:
        raise TaskFailure(process.stderr.read().decode("utf-8"))

    video_filepath = output_path + output_name_no_extension + ".mp4"
    ffmpeg_result = call_ffmpeg_process(blender_output_filepath, audio_filepath, video_filepath)
    print(f"FFMPEG process finished.")
    if ffmpeg_result[0] != b'':
            print("FFMPEG ERROR")
            raise TaskFailure(ffmpeg_result[0].decode("utf-8"))

    task_result = {
         "download": {
            "location": video_filepath,
            "filename": "video.mp4",
            "mime_type": "video/mp4"
         }
    }
    return task_result

@celery_app.task(name="visual.tasks.export_fbx", bind=True, hard_time_limit=WORKER_TIMEOUT)
def export_fbx(self,
              motion_filepath : str
              ):

    if os.environ["SERVER_MODE"] == "1":
        output_path = "/shared_storage/"
    else:
        output_path = "/app/output/fbx/"
    output_name = str(Path(motion_filepath).stem)
    output_file = output_path + output_name + ".fbx"

    python_script = "/app/genea_visualizer/export_fbx.py"
    script_args = [
         "-b", motion_filepath,
         "-m", "/app/genea_visualizer/model/LaForgeMale.fbx",
         "-o", output_file
    ]
    print(f"Calling Blender + {python_script} with args:\n{script_args}", sep="\n")
    process = call_blender_process(python_script, script_args)

    # Without this, the Blender process will not exit properly
    while True:
         line = process.stdout.readline()
         if not line:
              break
        #  print(line)

    process.wait()
    print(f"Blender process finished with code {process.returncode}.")
    if process.returncode != 0:
        raise TaskFailure(process.stderr.read().decode("utf-8"))

    task_result = {
         "download": {
            "location": output_file,
            "filename": "motion.fbx",
            "mime_type": "application/octet-stream"
         }
    }
    return task_result
