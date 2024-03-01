FROM malt33/php-cpg

ARG HOME="/SAST"
WORKDIR $HOME

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata

RUN apt-get update
RUN apt-get install python3 python3-pip python-is-python3 -y

COPY sast/ ${HOME}/sast
COPY tests/ ${HOME}/tests

COPY config.py ${HOME}/
COPY pytest.ini ${HOME}/pytest.ini

ARG REQUIREMENTS_FILE
COPY ${REQUIREMENTS_FILE} ${HOME}/${REQUIREMENTS_FILE}
RUN pip install -r ${HOME}/${REQUIREMENTS_FILE}

ENTRYPOINT [ "bash" ]