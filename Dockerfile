FROM python:3.9-bullseye

RUN apt-get -y update 

#install necessary linux packages
RUN apt-get install -y ffmpeg lame libatlas-base-dev alsa-utils 
RUN apt-get install -y pkg-config libhdf5-dev 
RUN apt-get install -y nano 
RUN apt-get install -y libhdf5-dev libc-ares-dev libeigen3-dev gcc gfortran libgfortran5 libatlas3-base libatlas-base-dev libopenblas-dev libopenblas-base libblas-dev liblapack-dev cython3 libatlas-base-dev openmpi-bin libopenmpi-dev python3-dev

#set pythonpath for micmon
ENV PYTHONPATH="/app/micmon/:/home/appuser/.local/bin/"

WORKDIR /app
COPY README.md /app/

#set user appuser - and give rights to it
ARG user=appuser
ARG group=appuser
ARG uid=1000
ARG gid=1000
RUN groupadd -g ${gid} ${group}
RUN useradd -u ${uid} -g ${group} -s /bin/sh -m ${user} # 

#give rights to microphone
RUN usermod -G audio appuser

# Switch to user
USER ${uid}:${gid}

#raspi python3.9 version of tensorflow
#RUN pip install https://github.com/PINTO0309/Tensorflow-bin/releases/download/v2.8.0/tensorflow-2.8.0-cp39-none-linux_aarch64.whl
RUN pip install https://github.com/PINTO0309/Tensorflow-bin/releases/download/v2.9.0/tensorflow-2.9.0-cp39-none-linux_aarch64.whl
RUN pip install -U wheel mock six
RUN pip install protobuf==3.20.*

#x386 architecture tensorflow version
#RUN pip install tensorflow

#RUN pip install numpy==1.21.6
#RUN pip install numpy --upgrade
RUN pip install numpy

COPY requirements.txt /app/
RUN pip install -r requirements.txt
#RUN pip install matplotlib

# setup.py needs root rights
USER root
RUN chown -R ${uid}:${gid} /app
RUN chmod 755 /app
RUN git clone https://github.com/filserm/micmon

RUN python micmon/setup.py build install

COPY . /app/
RUN chown -R ${uid}:${gid} /app
RUN chmod 777 /app
USER appuser
RUN micmon-datagen --low 250 --high 2500 --bins 100 --sample-duration 2 --channels 1  datasets/sound-detect/audio  datasets/sound-detect/data

# build the model
#CMD [ "python", "model.py"]

# run the mic
#CMD [ "python", "run_ml_algo.py"]

CMD ["./entrypoint.sh"]