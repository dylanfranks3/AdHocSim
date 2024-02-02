FROM ubuntu:22.04
ARG MYHOME=/root
ENV MYHOME ${MYHOME}
ARG PYTHONVER=3.10.5
ENV PYTHONVER ${PYTHONVER}
ARG PYTHONNAME=base
ENV PYTHONNAME ${PYTHONNAME}
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y locales wget git curl zip vim apt-transport-https tzdata language-pack-nb language-pack-nb-base manpages \
    build-essential libjpeg-dev libssl-dev xvfb zlib1g-dev libbz2-dev libreadline-dev libreadline6-dev libsqlite3-dev tk-dev libffi-dev libpng-dev libfreetype6-dev \
    libx11-dev libxtst-dev libfontconfig1 lzma lzma-dev liblzma-dev cmake sudo

RUN git clone https://github.com/pyenv/pyenv.git ${MYHOME}/.pyenv && \
    git clone https://github.com/yyuu/pyenv-virtualenv.git ${MYHOME}/.pyenv/plugins/pyenv-virtualenv && \
    git clone https://github.com/pyenv/pyenv-update.git ${MYHOME}/.pyenv/plugins/pyenv-update

SHELL ["/bin/bash", "-c", "-l"]
RUN ls
COPY ./.bash_profile  /tmp/
RUN cat /tmp/.bash_profile >> ${MYHOME}/.bashrc && \
    cat /tmp/.bash_profile >> ${MYHOME}/.bash_profile && \
    rm -f /tmp/.bash_profile && \
    source ${MYHOME}/.bash_profile && \
    pyenv install ${PYTHONVER} && \
    pyenv virtualenv ${PYTHONVER} ${PYTHONNAME} && \
    pyenv global ${PYTHONNAME}

#python related installs/builds for ns3
RUN pip install --verbose cppyy-cling
RUN pip install --verbose cppyy-backend==1.15.2
RUN pip install --verbose CPyCppyy==1.12.16
RUN pip install --verbose cppyy==2.4.2
RUN pip list


# ns3
RUN mkdir -p /usr/ns3
WORKDIR /usr 

RUN wget https://www.nsnam.org/release/ns-allinone-3.38.tar.bz2  && \
    tar -jxvf ns-allinone-3.38.tar.bz2

RUN cd /usr/ns-allinone-3.38 && ./build.py --enable-examples --enable-tests

RUN ln -s /usr/ns-allinone-3.38/ns-3.38/ /usr/ns3/

RUN apt-get clean && \
    rm -rf /var/lib/apt && \
    rm ns-allinone-3.38.tar.bz2


WORKDIR /usr/ns3/ns-3.38
RUN ./ns3 build
RUN ./ns3 configure --enable-python-bindings
#RUN ./ns3 run test.py

