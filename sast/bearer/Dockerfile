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
ARG BEARER_INTERFACE_DIR="${HOME}/sast/bearer"

WORKDIR ${BEARER_INTERFACE_DIR}

# copy necessary files for bearer
COPY bearer_v1_45_0 ${BEARER_INTERFACE_DIR}/bearer_v1_45_0/
COPY core ${BEARER_INTERFACE_DIR}/core/
COPY bearer-install.sh ${BEARER_INTERFACE_DIR}
COPY bearer-versions-list.yaml ${BEARER_INTERFACE_DIR}

RUN apt-get update
RUN apt-get install wget

# dependencies for bearer-install.sh
RUN apt-get install wget python3 python3-pip python-is-python3 -y
RUN pip3 install PyYAML

# bearer installation
RUN ${BEARER_INTERFACE_DIR}/bearer-install.sh ${BEARER_INTERFACE_DIR}/bearer-versions-list.yaml