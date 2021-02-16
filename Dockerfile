FROM python:3.8-slim
LABEL maintainer="psymbio"

# COPY . /app
RUN apt-get update && apt-get install -y \
        build-essential \
        curl \
        libfreetype6-dev \
        libzmq3-dev \
        libgl1-mesa-glx \
        pkg-config \
        python \
        python-dev \
        rsync \
        software-properties-common \
        unzip \
        apt-transport-https \
        ca-certificates \
        gnupg \
        imagemagick \
        libpq-dev \
        libxml2-dev \
        libxslt1-dev \
        openssh-client \
        file \
        libtiff5-dev \
        libjpeg-dev \
        zlib1g-dev \
        libfreetype6-dev \
        liblcms2-dev \
        tcl8.6-dev \
        tk8.6-dev \
        python-tk \
        graphviz \
        libgraphviz-dev \
        python-pydot \
        python3-setuptools \
        python-setuptools \
        python3-pip \
        python-pip \
        nginx \
        nano \
        wget \
        dialog \
        net-tools \
        vim \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN pip3 install matplotlib pandas pillow h5py ipykernel jupyter numpy pandas scipy sklearn opencv-python django tensorflow keras gunicorn django-environ django-storages uwsgi openpyxl wfastcgi waitress
# Set the working directory of the docker image
# WORKDIR /app
RUN rm -v /etc/nginx/nginx.conf
ADD nginx.conf /etc/nginx/sites-available/
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
ADD . .
# COPY ./nginx.conf /etc/nginx/nginx.conf
# EXPOSE 8000

# CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "sudokusolver.wsgi:application"]
CMD service nginx start
CMD gunicorn sudokusolver.wsgi:application --bind 0.0.0.0:$PORT

# ENV PORT 8000

# CMD python3 manage.py runserver 0.0.0.0:$PORT