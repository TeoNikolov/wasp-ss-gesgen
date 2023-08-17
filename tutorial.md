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

*Note: If the web server is buggy, your alternative way of completing the tasks is using a command line interface (CLI) inside the corresponding Docker containers. The tasks below provide an explanation for both the web-based and CLI use cases.*

# Task 1. Generating BVH motion from audio
## Web-based
*TODO*

## Docker CLI
*TODO*

# Task 2. Previewing the generated motion
## Web-based
*TODO*

## Docker CLI
*TODO*

# Task 3. Export the generated motion as FBX
## Web-based
*TODO*

## Docker CLI
*TODO*

# Final notes
If you finished the tutorial, you are free to do whatever you wish! For inspiration, you could:
- Continue messing around with the gesture generation system
- Work on systems you used previously during the summer school
- Work on the student assignment for Thursday
- Setup the Docker solution locally, if you have not done so already
- Browse the code to learn more about how various tools were used to create a functioning web app: `FastAPI`, the `Celery` task queue, `Redis`, `Docker` (`Dockerfile`, `docker compose`), the `GENEA Visualiser`, `HTML`, `CSS`, `Javascript` . Feel free to ask questions!
- Help other teams out
- Have a relaxing discussion with ChatGPT about the essence of life and the universe

Hope you had fun and learned something new :)