# pull official base image
FROM continuumio/miniconda3

# set working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc postgresql \
  && apt-get clean

# create and activate Conda environment
COPY ./requirements.yml .
RUN conda env create --file requirements.yml \
&& echo "source activate earny-rest" > ~/.bashrc
RUN conda init
ENV PATH /opt/conda/envs/earny-rest/bin:$PATH

# add app
COPY . .