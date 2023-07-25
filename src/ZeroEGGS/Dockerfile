FROM ubuntu:20.04

# Install Python 3.8
RUN apt update 
RUN apt install -y wget software-properties-common 
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update
RUN apt install -y python3.8 python3-pip

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install dependencies and packages in the requirements file
RUN apt install -y sox ffmpeg
RUN python3.8 -m pip install --upgrade pip
RUN python3.8 -m pip install torch==1.12.1+cpu torchvision==0.13.1+cpu --index-url https://download.pytorch.org/whl/cpu
RUN python3.8 -m pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app/ZeroEGGS/

# switch working directory
WORKDIR /app/ZeroEGGS/ZEGGS/