FROM python:3.7-buster

RUN apt-get update -y
RUN apt-get install ffmpeg lame libatlas-base-dev alsa-utils -y
RUN apt-get install pkg-config libhdf5-dev -y
RUN apt-get install nano -y

ENV PYTHONPATH=/app/micmon/

RUN pip install https://github.com/bitsy-ai/tensorflow-arm-bin/releases/download/v2.4.0-rc2/tensorflow-2.4.0rc2-cp37-none-linux_aarch64.whl
RUN pip install --upgrade numpy

WORKDIR /app

ARG user=appuser
ARG group=appuser
ARG uid=1000
ARG gid=1000
RUN groupadd -g ${gid} ${group}
RUN useradd -u ${uid} -g ${group} -s /bin/sh -m ${user} # 
RUN chown -R ${uid}:${gid} /app
RUN chmod 755 /app

# Switch to user
USER ${uid}:${gid}

#RUN pip install -r /app/requirements.txt

RUN git clone https://github.com:/BlackLight/micmon.git
RUN pip install -r /app/micmon/requirements.txt

USER root
RUN python /app/micmon/setup.py build install

USER appuser

COPY . /app/

CMD [ "python", "/app/test.py"]

