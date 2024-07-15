################################################################################
# base system
################################################################################

FROM ubuntu:22.04                                                                              
                                                                                               
ENV DEBIAN_FRONTEND=noninteractive
                                               
RUN apt-get update \                                                                           
    # Tools                                                                                    
    && apt-get -y --no-install-recommends install \                                            
        curl \                                 
        ca-certificates \
        zip \                                  
        unzip \                                
        git \                                  
        vim \                                                                                  
        build-essential \                                                                      
        autoconf \                                                                             
        automake \                                                                             
        bison \        
        flex \         
        re2c \ 
        gdb \                                                                                  
        libtool \                                                                              
        make \                                                                                 
        pkgconf \ 
        valgrind \                                                                             
        git \                                  
        libxml2-dev \                          
        libsqlite3-dev \                                                                       
        nginx \  
        sudo \                                                                                 
    && apt-get -y --no-install-recommends install \              
        mariadb-client   

RUN apt-get -y --no-install-recommends install \
        php \
        php-cli \
        php-common \
        php-fpm \
        php-mysql \
        php-zip \
        php-gd \
        php-mbstring \
        php-curl \
        php-xml \
        php-bcmath \
        openssl \
        php-json \
        php-tokenizer

ARG HOME
ARG PROGPILOT_INTERFACE_DIR="${HOME}/sast/progpilot"

WORKDIR ${PROGPILOT_INTERFACE_DIR}

# copy necessary files for progpilot
COPY progpilot_v1_1_0 ${PROGPILOT_INTERFACE_DIR}/progpilot_v1_1_0/
COPY core ${PROGPILOT_INTERFACE_DIR}/core/
COPY progpilot-install.sh ${PROGPILOT_INTERFACE_DIR}
COPY progpilot-versions-list.yaml ${PROGPILOT_INTERFACE_DIR}

RUN apt-get update
RUN apt-get install wget

# dependencies for progpilot-install.sh
RUN apt-get install wget python3 python3-pip python-is-python3 -y
RUN pip3 install PyYAML

# progpilot installation
RUN ${PROGPILOT_INTERFACE_DIR}/progpilot-install.sh ${PROGPILOT_INTERFACE_DIR}/progpilot-versions-list.yaml