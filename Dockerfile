FROM python:3.7-buster

RUN apt-get update -y
RUN apt-get install ffmpeg lame libatlas-base-dev alsa-utils -y
RUN apt-get install pkg-config libhdf5-dev -y
RUN apt-get install nano -y

ENV PYTHONPATH=/app/micmon/

WORKDIR /app

ARG user=appuser
ARG group=appuser
ARG uid=1000
ARG gid=1000
RUN groupadd -g ${gid} ${group}
RUN useradd -u ${uid} -g ${group} -s /bin/sh -m ${user} # 
RUN chown -R ${uid}:${gid} /app
RUN chmod 755 /app
RUN usermod -G audio appuser

# Switch to user
USER ${uid}:${gid}

RUN pip install https://github.com/bitsy-ai/tensorflow-arm-bin/releases/download/v2.4.0-rc2/tensorflow-2.4.0rc2-cp37-none-linux_aarch64.whl
RUN pip install numpy==1.21.6
RUN pip install matplotlib

RUN git clone https://github.com:/BlackLight/micmon.git

USER root
RUN python /app/micmon/setup.py build install

USER appuser

RUN micmon-datagen --low 250 --high 2500 --bins 100 --sample-duration 2 --channels 1  /app/datasets/sound-detect/audio  /app/datasets/sound-detect/data

COPY . /app/

CMD [ "python", "/app/test.py"]


