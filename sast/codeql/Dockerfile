################################################################################
# base system
################################################################################

FROM adoptopenjdk/openjdk11

ARG TPF_HOME="/tp-framework"
ARG CODEQL_INTERFACE_DIR="${TPF_HOME}/SAST/codeql"

WORKDIR ${CODEQL_INTERFACE_DIR}

# copy necessary files for codeql
COPY codeql_v2_9_2 ${CODEQL_INTERFACE_DIR}/codeql_v2_9_2/
COPY codeql_v2_13_1 ${CODEQL_INTERFACE_DIR}/codeql_v2_13_1/
COPY core ${CODEQL_INTERFACE_DIR}/core/
COPY codeql-install.sh ${CODEQL_INTERFACE_DIR}
COPY codeql-versions-list.yaml ${CODEQL_INTERFACE_DIR}

RUN apt-get update
RUN apt-get install wget

# dependencies for codeql-install.sh
RUN apt-get install wget python3 python3-pip python-is-python3 -y
RUN pip3 install PyYAML

# codeql installation
RUN ${CODEQL_INTERFACE_DIR}/codeql-install.sh ${CODEQL_INTERFACE_DIR}/codeql-versions-list.yaml