# Gesture Generation Tutorial
The gesture generation tutorial for the WASP summer school 2023 is composed of 3 tasks:
- Generating BVH motion from WAV audio
- Previewing the generated motion as a MP4 video
- Exporting the generated BVH motion as an FBX file format

A web-based system has been developed to enable the completion of these tasks. WASP currently hosts such a web server at *TODO* that you can acess in your browser; this saves you the effort of having to setup the system yourself on your machine. However, you might prefer to setup the system on your machine in some casee:
- There is an issue connecting to the WASP server.
- The WASP server has crashed.
- You want to dive deep into how the system works.
- You want to modify the functionality of the system (advanced, good in your free time).

Please refer to the "Setup" instructions in the gesture generation repository if you wish to setup the system yourself.

*Note: If the web server is buggy, you need to setup the Docker solution on your machine and use a command line interface (CLI) inside the corresponding Docker containers. For this purpose, make sure that you change the variable `SERVER_MODE` to `0` inside the `.env` file in the [repository root](https://github.com/TeoNikolov/wasp-ss2023-gesgen/).*

# Task 1. Generating BVH motion from audio
The first task is to use the ZeroEGGS AI model to generated gestures from audio. This audio may be either synthetic, your own voice, or any other audio you got from the internet. When completing the task, think about the following:
- How does changing one parameter affect the generated animation? Make sure to keep the seed fixed.
- Does changing the seed, while keeping the generation parameters fixed, lead to gestures that are clearly distinguishable from animations generated previously?
- Do the gestures look good? If not, can the visual quality be improved?
- Do the gestures match the speech temporally?

## Web-based
1. Open the web page at `localhost:5001`.
2. Click on the file input button after "Audio (WAV)" and pick a WAV audio file for which you want to generate an animation with gestures.
3. Choose a starting pose from the list after "Choose a starting pose". The corresponding pose will be used as the first frame of your generated animation.
4. Pick a style for your animation from the list after "Choose a style". This will act as a guide for the generated animations.
5. Pick a "temperature" value for gesture generation. A higher value will tell the ZeroEGGS model to generate gestures that are similar to the style you have selected. A lower value will have the opposite effect and the generated gestures will be influenced less by the selected style.
6. Changing the seed lets you generate a different animation even for the same input. Keeping the seed fixed lets you tweak the parameters without adding additional randomness.
7. Press "Download (BVH)" when you are satisfied with your choices. *Warning: There is a bug that may require you to press the button multiple times until the generation starts.*
8. Wait for generation to finish. You will be shown a "download file" dialog to save the generated BVH file when finished.

## Docker CLI
The `/data/` and `/output/` folders located in the gesture generation repository root are mounted inside Docker; you can add, remove, and access files directly from your file system. It is recommended to use these folders when completing this task, as it makes it easy to add your own files inside `/data/audio/` and to access the generated BVH files inside `/output/bvh/`.

1. Open your terminal of choice.
2. Run `docker ps` and find the "Container ID" of the `wasp-ss2023-gesgen` container.
3. Run `docker exec -it <container ID> bash` to attach to the container. If using Git Bash, you may need to add `winpty` at the start of the command.
4. Convert the audio data to be compatible with ZeroEGGS by running `sox "/app/data/audio/sentence01_3.wav" -r 16k -c 1 -b 32 "/app/output/converted_audio.wav"`.
    - `<first param>` : This is the input file we want to convert.
    - `-r` : The audio sampling rate. We need 16000 Hz.
    - `-c` : The number of audio channels. We need 1 for Mono audio.
    - `-b` : The bid depth of the data samples. ZeroEGGS uses a depth of 32 bits which is used to encode audio samples at a high precision.
    - `<last param>` : This is the output file that has been converted.
5. Generate gestures with ZeroEGGS by running `python3.8 "/app/ZeroEGGS/ZEGGS/generate.py" -o "/app/data/gesgen_options_v1.json" -s "/app/data/styles/Flirty.bvh" -a "/app/output/converted_audio.wav" -p "/app/output/bvh/" -r 1234 -fp "/app/data/start_poses/pose_1.bvh" -n "output_motion" -t 1.0`.
    - `-o` : Settings that ZeroEGGS will use for generation. Do not change this.
    - `-s` : The style to use when generating gestures. This acts as a guide for the gesture style that the model aims to generate.
    - `-a` : Input audio file.
    - `-p` : Folder in which the motion and a copy of the audio will be output to.
    - `-r` : The random seed to use for generation.
    - `-fp` : File containing a pose sample to use as the first pose of the generated animation.
    - `-n` : Name of the output BVH file.
    - `-t` : Temperature of the model, between `0.0` and `1.0`. A higher value causes the model to generate gesture that are similar to the chosen style; a lower value has the opposite effect.

When proceding to the next task, run `exit` in your terminal to detach from the Docker container.

# Task 2. Previewing the generated motion
Previewing the generated animations is much more straightforward than generating them. In fact, there is very litle you need to do, particularly with the web-based solution. Keep in mind that generating a video of the gestures is a relatively slow process, so please be patient.

## Web-based
1. Ensure you have opened the web page at `localhost:5001`.
2. Click on the file input button after "Motion (BVH)" and pick the generated BVH motion file.
3. Click on the file input button after "Audio (WAV)" and pick the WAV audio file that matches the generated BVH file you want to visualise.
4. Press "Download (MP4)" when you are satisfied with your choices. *Warning: There is a bug that may require you to press the button multiple times until the generation starts.*
5. Wait for generation to finish; this process can be rather slow. You will be shown a "download file" dialog to save the generated MP4 file when finished.

## Docker CLI
The `/output/` folder located in the gesture generation repository root is mounted inside Docker; you can add, remove, and access files directly from your file system. It is recommended to use this folder when completing this task, as it makes it easy to view the generated videos inside `/output/mp4/`.

1. Open your terminal of choice.
2. Run `docker ps` and find the "Container ID" of the `wasp-ss2023-visual` container.
3. Run `docker exec -it <container ID> xvfb-run -s ":99" -s '-screen 0 1024x700x24 -ac' bash` to attach to the container. If using Git Bash, you may need to add `winpty` at the start of the command. We use xvfb-run to create a virtual screen, which is required by Blender to render video files.
4. Run `/blender/blender-2.83.0-linux64/blender -b --python "/app/genea_visualizer/blender_render.py" -- --input "/app/output/bvh/output_motion.bvh" --duration 9999 --video --res_x 640 --res_y 480 -o "/app/output/mp4/output_video.mp4"`:
    - `-b` : This flag tells Blender to run in "headless" mode without the UI.
    - `--python` : A Python script which Blender will execute when it runs. This contains our custom rendering code.
    - `--input` : The BVH we want to render a video for. Only files generated by ZeroEGGS are compatible.
    - `--duration` : How many frames to render. To render the entire animation, we set this to `9999`.
    - `--video` : This indicates that we want to render a video. In principle, it is possible to render an image as well, but this will not be useful to us currently.
    - `--res_x` : The horizontal resolution to render the video at. A higher value will lead to slower rendering, but higher quality.
    - `--res_y` : The vertical resolution to render the video at. A higher value will lead to slower rendering, but higher quality.
    - `-o` : The directory in which the file will be output to. Currently, the output filename is the same as the input file with the extension set to `.mp4`.
5. Wait for the video to render - this can take a while depending on the animation duration.
6. The rendered video lacks audio (due to technical constraints). To add audio, run `ffmpeg -i "/app/output/mp4/output_video.mp4" -i "/app/output/bvh/output_motion.wav" -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 -shortest "/app/output/mp4/output_video_audio.mp4"`:
    - `<first -i>` : This is the video stream we want to combine with audio.
    - `<second -i>` : This is the audio stream we want to combine with video. Use the audio file that corresponds to the generated BVH that you rendered the first video for. In our case, ZeroEGGS makes a copy of the audio inside the `/output/bvh/` folder, so we can use that.
    - `<last param>` : This is the combine video and audio file that will be converted.
    - `<all other params>` : These params are needed for ffmpeg to correctly handle the data streams. These details are very low level and are not crucial for this tutorial. If you are interested in knowing more, you can read the [official ffmpeg documentation](https://ffmpeg.org/ffmpeg.html) and the one in this [ffmpeg Python wrapper](https://github.com/kkroening/ffmpeg-python).
7. Open the rendered video and preview the results!

You do not need to write `exit` in the terminal. The next task asks you to enter the same container.

# Task 3. Export the generated motion as FBX
## Web-based
*TODO*

## Docker CLI
The `/output/` folder located in the gesture generation repository root is mounted inside Docker; you can add, remove, and access files directly from your file system. It is recommended to use this folder when completing this task, as it makes it easy to access the generated FBX file inside `/output/fbx/`.

1. Open your terminal of choice.
2. Run `docker ps` and find the "Container ID" of the `wasp-ss2023-visual` container.
3. Run `docker exec -it <container ID> xvfb-run -s ":99" -s '-screen 0 1024x700x24 -ac' bash` to attach to the container. If using Git Bash, you may need to add `winpty` at the start of the command.
4. Export an FBX using `/blender/blender-2.83.0-linux64/blender -b --python "/app/genea_visualizer/export_fbx.py" -- -b "/app/output/bvh/output_motion.bvh" -m "/app/genea_visualizer/model/LaForgeMale.fbx" -o "/app/output/fbx/output_motion.fbx"`:
    - `-b (first occurrence)` : This flag tells Blender to run in "headless" mode without the UI.
    - `--python` : A Python script which Blender will execute when it runs. This contains our custom rendering code.
    - `-b (second occurrence)` : This is the BVH file we want to convert to FBX. Only files generated by ZeroEGGS are compatible.
    - `-m` : The model we want to apply the animation to. In our case, ZeroEGGS provide their own model for which animations are generated. Do not change this.
    - `-o` : The filename of the output FBX file.

# Final notes
If you finished the tutorial, you are free to continue experimenting or do something else! For inspiration, you could:
- Create new audio files and generate new animations
- Experiment with the gesture generation parameters
- Work on systems you used previously during the summer school
- Work on the student assignment for Thursday
- Setup the Docker solution locally, if you have not done so already
- Browse the code to learn more about how various tools were used to create a functioning web app: `FastAPI`, the `Celery` task queue, `Redis`, `Docker` (`Dockerfile`, `docker compose`), the `GENEA Visualiser`, `HTML`, `CSS`, `Javascript` . Feel free to ask questions!
- Help other teams out
- Have a relaxing discussion with ChatGPT about the essence of life and the universe

Hopefully you had fun and learned something new :)