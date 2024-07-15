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
ARG SEMGREP_INTERFACE_DIR="${HOME}/sast/semgrep"

WORKDIR ${SEMGREP_INTERFACE_DIR}

# copy necessary files for semgrep
COPY semgrep_v1_79_0 ${SEMGREP_INTERFACE_DIR}/semgrep_v1_79_0/
COPY core ${SEMGREP_INTERFACE_DIR}/core/
COPY semgrep-install.sh ${SEMGREP_INTERFACE_DIR}
COPY semgrep-versions-list.yaml ${SEMGREP_INTERFACE_DIR}

RUN apt-get update
RUN apt-get install wget

# dependencies for semgrep-install.sh
RUN apt-get install wget python3 python3-pip python-is-python3 -y
RUN pip3 install PyYAML

# semgrep installation
RUN ${SEMGREP_INTERFACE_DIR}/semgrep-install.sh ${SEMGREP_INTERFACE_DIR}/semgrep-versions-list.yaml