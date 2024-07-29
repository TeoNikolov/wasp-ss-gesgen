# Introduction
This repository contains various modules and code needed for completing the "Gesture Generation" tutorial for the [WASP Summer School 2023 student assignment](https://github.com/Svito-zar/wasp-2023-summer-school/). Later, the students will also use what they have learned here to generate gestures as part of a final student assignment; these gestures will be visualised in the [Norrköping Visualisation Center](https://visualiseringscenter.se/en).

The solution is composed of multiple modules, each of which has its own responsibilities.
- A *gesture generation* module generates gesture animations using an AI model. We use the [ZeroEGGS](https://github.com/ubisoft/ubisoft-laforge-ZeroEGGS) AI model developed by Saeed Ghorbani and his colleagues at Ubisoft LaForge.
- A *visualisation* module which visualises gesture data in the form of a video. It also allows the export of gesture data to FBX. We use the [GENEA Challenge 2022 Visualizer](https://github.com/TeoNikolov/genea_visualizer/tree/archive_2022).
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
- Make sure that `git` is installed on your machine. On Ubuntu, you can run `sudo apt-get install git-all`. On Windows, you can download [Git for Windows](https://git-scm.com/downloads).
- Clone this repository to your machine with `git clone https://github.com/TeoNikolov/wasp-ss2023-gesgen/`.
- [Install](https://www.docker.com/products/docker-desktop/) the latest version of Docker. Verify your installation by running `docker run hello-world`; you should see *"Hello from Docker!"* in your terminal.
- Make sure Docker is running. You can test this by running `docker run hello-world`.
- If you wish to use the command line interface instead of the web app, set `SERVER_MODE` to `0` inside the `.env` file.

## Build the Docker images
Run `docker compose build` to build the following Docker images (this can take a while):

- `wasp-ss2023-gesgen` : This contains the [ZeroEGGS](https://github.com/ubisoft/ubisoft-laforge-ZeroEGGS) gesture generation AI model.

- `wasp-ss2023-visual` : This contains scripts for visualizing animations. It is based on the [GENEA Challenge 2022 Visualizer](https://github.com/TeoNikolov/genea_visualizer/tree/archive_2022) visualizer that renders `.bvh` motion and `.wav` audio data into a `.mp4` video. There are also Blender scripts to convert `.bvh` to `.fbx`.

- `wasp-ss2023-web` : This houses the web server and REST API. This makes it possible to interact with the other modules via the web browser or command line.

## Deploy the Docker images
Deploying containers from the images is done by running `docker compose up -d`.
The `-d` flag deploys the containers in *detached mode* so that the terminal remains usable. An image named `redis` will also be downloaded, as the other images depend on it.

You should be able to open a web page at `localhost:5001` if all containers started without errors. If the web page does not load, then most likely the `wasp-ss2023-web` container is not running or has crashed, or that your firewall is blocking port `5001`.

# VM Setup
Repo
- `cd ~/`
- `mkdir src
- `cd src`
- `git clone https://github.com/TeoNikolov/wasp-ss2023-gesgen.git`
- `git checkout 2024`

Docker
- [https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)
- `sudo docker compose build`
- `sudo docker compose up -d`

(If error)
- `sudo systemctl restart docker`
- `sudo docker compose build`
- `sudo systemctl restart docker`

(If still error)
- Check if cgroups are already mounted
	- `cat /proc/self/cgroup | grep devices`
	- E.g. `1:name=systemd:/user/docker/12345.devices`
- Mount cgroups manually
	- `sudo mkdir /sys/fs/cgroup/devices`
	- `sudo mount -t cgroup -o devices devices /sys/fs/cgroup/devices`
- Restart Docker
	- `sudo systemctl restart docker`

# Usage
You can either use the deployed web server OR a CLI that can attach to the Docker containers. The workflow is described [here](https://github.com/TeoNikolov/wasp-ss2023-gesgen/blob/main/tutorial.md).

# Folders and Files
*TODO*

Folders are *italicized*; files are not.
- *root*
    - .env - Contains environment variables set inside all Docker containers.
    - compose.yaml - 

# License
This repo is licensed under the *CC BY-NC-SA 4.0* license. You can find an overview of the license [here](https://creativecommons.org/licenses/by-nc-sa/4.0/).

**Disclaimer:** The license in this repo does not apply to the ZeroEGGS system; it has [its own license](https://github.com/ubisoft/ubisoft-laforge-ZeroEGGS/blob/main/License.md). Please contact its authors in case you have any questions.

# Attribution

When making use of this repository whether it is code or showing example output, please credit our work by including the **repo link** (https://github.com/TeoNikolov/wasp-ss2023-gesgen) and our **names** (Teodor Nikolov, Mihail Tsakov, Taras Kucherenko) in your documents. We would greatly appreciate it!

**ZeroEGGS**

This repository utilizes Ubisoft La Forge's [ZeroEGGS](https://arxiv.org/abs/2209.07556) gesture generation AI model. We are very thankful that they let us use their model for the summer school! You are encouraged to browse the [ZeroEGGS repo](https://github.com/ubisoft/ubisoft-laforge-ZeroEGGS/) and to contact the authors if you have any questions about the model or using it for your own projects!

# Contact
If you have any questions, feel free to contact these folks via email:
- Teodor Nikolov - tnikolov@hotmail.com
- Mihail Tsakov - tsakovm@gmail.com
- Taras Kucherenko - tkucherenko@ea.com
