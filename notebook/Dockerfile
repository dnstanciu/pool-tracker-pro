FROM jupyter/scipy-notebook:latest

COPY requirements.txt /

RUN pip install -U pip

# Install dependencies.
RUN pip install -r /requirements.txt

# Set work directory.
#RUN mkdir /code
WORKDIR /work

# Make directory for data.
#RUN mkdir /data

# Set up our notebook config.
COPY jupyter_notebook_config.py /root/.jupyter/

# Copy notebooks.
COPY . /work/

# Copy data.
#COPY ../out/protoshape/interim /work/data/
