# wasp-ss2023-gesgen
Repository containing code for the gesture generation part of the WASP Summer School 2023 student assignment.

**Disclaimer** The repository is WIP and may not function fully. The README is currently unavailable.

# Introduction
This repository contains various modules and code needed for completing the "Gesture Generation" tutorial for the WASP Summer School 2023. Later, the students will also use what they have learned here to generate gestures as part of a final student assignment; these gestures will be visualised in the [Norrköping Visualisation Center](https://visualiseringscenter.se/en).

The solution is composed of multiple modules, each of which has its own responsibilities.
- A *gesture generation* module generates gesture animations using an AI model. Currently, we are using the [ZeroEGGS](https://github.com/ubisoft/ubisoft-laforge-ZeroEGGS) AI model developed by Saeed Ghorbani and his colleagues at Ubisoft LaForge.
- A *visualisation* module which visualises gesture data in the form of a video. It also allows the export of gesture data to FBX.
- A *web app* module provides access to the two systems above via a web page you can access in your browser.

More detailed information is given below.

## Gesture generation module
The gesture generation model lets you generate motion data in Biovision Hierarchy (BVH) format from raw audio in WAV format.

*TODO*

You can tweak the generated motion using various controls:
- motion style
- starting pose
- temperature
- seed

*END OF TODO*

## Visualisation module
The visualisation module lets you preview your generated BVH files as a MP4 video that includes WAV audio. For this, we have leveraged the [GENEA Visualiser](https://github.com/TeoNikolov/genea_visualizer) which was developed for the [GENEA Challenge](https://genea-workshop.github.io/2023/challenge/) that uses Blender.

*TODO* Below is incomplete

The visualisation module also lets you export the BVH motion data to FBX file format. This format is widely adopted by 3D software and is needed for use with Unreal Engine, which is needed by the WASP summer school to visualise...TODO

*TODO* Explain about blender? ffmpeg?

## Web app module
*TODO* Explain how it all works with celery and FASTAPI

A web server serves a web page that can be accessed from a browser. This is a convenient way to access the above-mentioned systems without having to tinker with the command line.

## Docker compose setup
*TODO* Too short? Maybe something more interesting to say here?

Docker is used to encapsulate the above-mentioned systems so that you do not have to setup their environments yourself (which can be quite cumbersome).

# Local setup
Below are instructions on how to set up the gesture generation system locally on your machine.
This is not required as WASP already hosts a web server that you can use.
However, a local setup may be useful to you if you wish to learn in-depth about how the system works and if you wish to modify or add any (source) files. This will also be useful in the potential scenario that the WASP server crashes or if there are networking-related issues between your machine and the WASP server.

**You can skip this section if you prefer to only use the WASP server.**

## Prerequisites
- Make sure you have cloned this repository on your machine by running `git clone https://github.com/TeoNikolov/wasp-ss2023-gesgen/`.
- Make sure that `git` is installed on your machine. On Ubuntu, you can run `sudo apt-get install git-all` to download `git`. On Windows, you can download [Git for Windows](https://git-scm.com/downloads).
- Make sure to install Docker by refering to [these instructions](https://www.docker.com/products/docker-desktop/). You are encouraged to download the **latest version** to avoid potential issues with deploying the gesture generation system. Run `docker run hello-world` to test your installation; you should see *"Hello from Docker!"* in your terminal.
- Make sure Docker is running before continuing with the setup. You can test this by running `docker run hello-world`.

## Build the Docker images
Build the Docker images by running `docker compose build`. This will build the following images:
- `wasp-ss2023-gesgen` - This contains the ZeroEGGS gesture generation AI model.
- `wasp-ss2023-visual` - This contains Blender and scripts that make it possible to render motion (BVH) and audio (WAV) data into a video (MP4). It is also possible to convert from BVH to FBX format.
- `wasp-ss2023-web` - This exposes the other systems via the web. Without this, you can only use the command line interface to interact with the other modules.

*Building the images can take a while.*

## Deploy the Docker images
Deploying containers from the images is done by running `docker compose up -d`.
The `-d` flag deploys the containers in *detached mode* so that the terminal remains usable. An image named `redis` will also be downloaded, as the other images depend on it.

You should be able to open a web page at `localhost:5001` if all containers started without errors. If the web page does not load, then most likely the `wasp-ss2023-web` container is not running or has crashed, or that your firewall is blocking port `5001`.

# Workflows
There are three major workflows when it comes to using the gesture generation system:
- Generating motion data from audio
- Visualising the generated motion data
- Exporting the motion data to FBX for use in other software

Steps are provided for the following use cases:
1. Using the WASP web server
2. Using a web server that you have hosted
3. Using the command line interface directly inside the Docker containers

## Generate motion data from audio
*TODO*

Using CLI.

Using the web server.

## Visualise motion data
*TODO*

Using CLI.

Using the web server.

## Export motion data to FBX
*TODO*

Using CLI.

Using the web server.

# Folders and Files
*TODO*

This section provides information about the various folders and files in this repository. Note that only the most important folders and files are included to keep this section short.

Folders are *italicized*; files are not.
- *root*
    - .env - Contains environment variables set inside all Docker containers.
    - compose.yaml - 

# License
*TODO*

# Attribution
This repository utilizes Ubisoft La Forge's [ZeroEGGS](https://arxiv.org/abs/2209.07556) gesture generation AI model. You are encouraged to browse around their [repository](https://github.com/ubisoft/ubisoft-laforge-ZeroEGGS/) and to contact the authors if you have any questions about it!

# Contact
If you have any questions, feel free to contact these folks via email:
- Teodor Nikolov - tnikolov@hotmail.com
- Mihail Tsakov - tsakovm@gmail.com
- Taras Kucherenko - tkucherenko@ea.com