FROM malt33/php-cpg

ARG SAST_HOME="/SAST"
WORKDIR $SAST_HOME

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata

RUN apt-get update
RUN apt-get install python3 python3-pip python-is-python3 -y

COPY src ${SAST_HOME}/src

COPY config.py ${SAST_HOME}/
COPY config.py ${SAST_HOME}/
COPY pytest.ini ${SAST_HOME}/pytest.ini

ARG REQUIREMENTS_FILE
COPY ${REQUIREMENTS_FILE} ${SAST_HOME}/${REQUIREMENTS_FILE}
RUN pip install -r ${SAST_HOME}/${REQUIREMENTS_FILE}

ENV PYTHONPATH "${PYTHONPATH}:${SAST_HOME}/src"
ENTRYPOINT [ "bash" ]