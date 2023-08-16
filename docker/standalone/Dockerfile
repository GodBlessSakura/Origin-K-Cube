FROM continuumio/anaconda3:2022.10
RUN apt-get -y update
RUN apt-get -y install git

RUN git clone https://github.com/jerryIsHere/K-Cube /repo
WORKDIR /repo
RUN conda env create -f /repo/environment.yml