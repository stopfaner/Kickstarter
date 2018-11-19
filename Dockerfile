FROM ubuntu:18.04

# Install required OS packages
RUN apt-get update -y
RUN apt-get install -y build-essential tar gcc libffi-dev libev4 libev-dev libpq-dev
RUN apt-get install -y python3-dev python3-pip cython3

EXPOSE 8000
RUN pip3 install --upgrade pip
RUN pip3 install virtualenv
# Make a workdir and virtualenv
WORKDIR /opt/service_api
RUN virtualenv kickstarter
RUN . kickstarter/bin/activate

ENV DATABASE_HOST="89.235.184.160"
ENV DATABASE_PORT=7432

# Install everything else
ADD . /opt/service_api
CMD @rm -rf *.egg-info
RUN pip3 install -e .
CMD gunicorn manage:app --config config/prod.py --worker-class sanic.worker.GunicornWorker
