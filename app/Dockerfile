FROM centos:latest
MAINTAINER valerio.formato <valerio.formato@cern.ch>

RUN mkdir -p /opt/myproject
WORKDIR /opt/myproject
# ADD . /opt/myproject
ADD requirements.txt /opt/myproject

ARG version="6.09.02"
LABEL description="CERN ROOT framework"
LABEL version="${version}"

RUN yum -y install epel-release
RUN yum -y install nc gcc-c++ bzip2 git vim libpng libjpeg \
     postgresql postgresql-devel python-devel libSM libX11 libXext \
     libXpm libXft gsl-devel python-pip make cmake3\
     && yum -y clean all
RUN pip install --upgrade pip && pip install jupyter
RUN pip install -U 'Twisted[tls,http2]'
RUN ln -s /usr/bin/cmake3 /usr/bin/cmake

# Set ROOT environment
ENV ROOTSYS         "/opt/root"
ENV PATH            "$ROOTSYS/bin:$ROOTSYS/bin/bin:$PATH"
ENV LD_LIBRARY_PATH "$ROOTSYS/lib:$LD_LIBRARY_PATH"
ENV PYTHONPATH      "$ROOTSYS/lib:$PYTHONPATH"

ADD https://root.cern.ch/download/root_v${version}.Linux-centos7-x86_64-gcc4.8.tar.gz /var/tmp/root.tar.gz
RUN tar xzf /var/tmp/root.tar.gz -C /opt && rm /var/tmp/root.tar.gz

RUN pip install -r requirements.txt
# RUN /bin/bash -c "source setenv.sh; python manage.py migrate" # Can this be done during build? i.e. no link to the DB?

# VOLUME ["/opt/myproject/collected_static"]
