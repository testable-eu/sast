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
        curl \
        vim \
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
ARG SNYK_INTERFACE_DIR="${HOME}/sast/snyk"

WORKDIR ${SNYK_INTERFACE_DIR}

# copy necessary files for snyk
COPY snyk_v1_1291_1 ${SNYK_INTERFACE_DIR}/snyk_v1_1291_1/
COPY core ${SNYK_INTERFACE_DIR}/core/
COPY snyk-install.sh ${SNYK_INTERFACE_DIR}
COPY snyk-versions-list.yaml ${SNYK_INTERFACE_DIR}

RUN apt-get update
RUN apt-get install wget

# dependencies for snyk-install.sh
RUN apt-get install wget python3 python3-pip python-is-python3 -y
RUN pip3 install PyYAML

# snyk installation
RUN ${SNYK_INTERFACE_DIR}/snyk-install.sh ${SNYK_INTERFACE_DIR}/snyk-versions-list.yaml