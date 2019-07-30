FROM jjanzic/docker-python3-opencv:latest

#contrib-opencv-4.1.0

COPY requirements.txt /

RUN pip install -U pip

# Install dependencies.
RUN pip install -r /requirements.txt

# Set work directory.
RUN mkdir /code
WORKDIR /code

# Copy project.
COPY . /code/
