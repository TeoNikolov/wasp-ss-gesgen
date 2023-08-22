# Introduction
This repository contains various modules and code needed for completing the "Gesture Generation" tutorial for the WASP Summer School 2023. Later, the students will also use what they have learned here to generate gestures as part of a final student assignment; these gestures will be visualised in the [Norrköping Visualisation Center](https://visualiseringscenter.se/en).

The solution is composed of multiple modules, each of which has its own responsibilities.
- A *gesture generation* module generates gesture animations using an AI model. Currently, we are using the [ZeroEGGS](https://github.com/ubisoft/ubisoft-laforge-ZeroEGGS) AI model developed by Saeed Ghorbani and his colleagues at Ubisoft LaForge.
- A *visualisation* module which visualises gesture data in the form of a video. It also allows the export of gesture data to FBX.
- A *web app* module provides access to the two systems above via a web page you can access in your browser.

*TODO: A low-level description of the various modules such as libraries or variables is currently missing. This information will not be prioritized DURING the summer school; you can check if the repo is updated sometime in September. However, you can still see various commands actively used by the system in the [gesture generation tutorial](https://github.com/TeoNikolov/wasp-ss2023-gesgen/blob/main/tutorial.md).*

***Warning**: The server has not been tested on ARM-based CPU architectures (e.g. Mac with M1 chip). It may not run on those systems.*

***Warning**: The server has only been tested in Windows and Linux (Ubuntu). The system may not function correctnyl on other OSes like macOS.*

***Warning**: The web page has been tested only on Chrome and Firefox. It may not look properly / function correctly on other browsers like Opera or Safari.*

# Local setup
Below are instructions on how to set up the gesture generation system locally on your machine.
This is not required as WASP already hosts a web server that you can use.
However, a local setup may be useful to you if you wish to learn in-depth about how the system works and if you wish to modify or add any (source) files. This will also be useful in the potential scenario that the WASP server crashes or if there are networking-related issues between your machine and the WASP server.

## Prerequisites
- Make sure you have cloned this repository on your machine by running `git clone https://github.com/TeoNikolov/wasp-ss2023-gesgen/`.
- Make sure that `git` is installed on your machine. On Ubuntu, you can run `sudo apt-get install git-all` to download `git`. On Windows, you can download [Git for Windows](https://git-scm.com/downloads).
- Make sure to install Docker by refering to [these instructions](https://www.docker.com/products/docker-desktop/). You are encouraged to download the **latest version** to avoid potential issues with deploying the gesture generation system. Run `docker run hello-world` to test your installation; you should see *"Hello from Docker!"* in your terminal.
- Make sure Docker is running before continuing with the setup. You can test this by running `docker run hello-world`.
- If you wish to use the command line interface instead of the web app, set `SERVER_MODE` to `0` inside the `.env` file.

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

# How to use
You can either use the web server that is deployed OR you can use a command line interface (CLI) that attaches to the various Docker containers. A complete description of the workflow can be found [here](https://github.com/TeoNikolov/wasp-ss2023-gesgen/blob/main/tutorial.md).

# Folders and Files
*TODO*

This section provides information about the various folders and files in this repository. Note that only the most important folders and files are included to keep this section short.

Folders are *italicized*; files are not.
- *root*
    - .env - Contains environment variables set inside all Docker containers.
    - compose.yaml - 

# License
This repo is licensed under the *CC BY-NC-SA 4.0* license. You can find an overview of the license [here](https://creativecommons.org/licenses/by-nc-sa/4.0/).

**Disclaimer:** The license in this repo does not apply to the ZeroEGGS system; it has [its own license](https://github.com/ubisoft/ubisoft-laforge-ZeroEGGS/blob/main/License.md). Please contact its authors in case you have any questions.

# Attribution

When making use of this repository whether it is code or showing example output, please credit our work by including the **repo link** and our **names** in your document. We would greatly appreciate it!

**ZeroEGGS**

This repository utilizes Ubisoft La Forge's [ZeroEGGS](https://arxiv.org/abs/2209.07556) gesture generation AI model. We are very thankful that they let us use their model for the summer school! You are encouraged to browse the [ZeroEGGS repo](https://github.com/ubisoft/ubisoft-laforge-ZeroEGGS/) and to contact the authors if you have any questions about the model or using it for your own projects!

# Contact
If you have any questions, feel free to contact these folks via email:
- Teodor Nikolov - tnikolov@hotmail.com
- Mihail Tsakov - tsakovm@gmail.com
- Taras Kucherenko - tkucherenko@ea.com
