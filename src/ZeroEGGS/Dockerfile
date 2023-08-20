FROM ubuntu:20.04

# Install Python 3.8 + other dependencies (root)
RUN apt update 
RUN apt install -y wget software-properties-common 
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update
RUN apt install -y python3.8 python3-pip
RUN apt install -y sox ffmpeg

# install ZeroEGGS dependencies
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN python3.8 -m pip install --upgrade pip
RUN python3.8 -m pip install torch==1.12.1+cpu torchvision==0.13.1+cpu --index-url https://download.pytorch.org/whl/cpu
RUN python3.8 -m pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app/ZeroEGGS/

# install non-ZeroEGGS dependencies
RUN python3.8 -m pip install celery[redis]==5.3.1

###
# A non-root user is good practice, but it requires the host to setup the same
# user and give the mounted volume (directory) write permissions.
# Otherwise, files cannot be written by the user inside the container.
# To keep things "out-of-the-box" we use root for this simple application.
###
# create non-root user
#RUN groupadd -g 999 appuser && \
#	useradd -r -u 999 -g appuser appuser
#USER appuser

# run
WORKDIR /app/ZeroEGGS/celery/
ENTRYPOINT celery -A tasks worker --concurrency ${WORKER_COUNT_GESGEN} --loglevel=info -Q q_gesgen
