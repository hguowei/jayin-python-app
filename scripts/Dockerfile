FROM python:2.7
MAINTAINER Guowei Huang <hguowei@sina.com>

USER root

RUN mkdir -p /docker_app
WORKDIR /docker_app
ADD . /docker_app
RUN pip install -r src/requirements.txt

#CMD ["bash"]

RUN chmod +x scripts/docker-entrypoint.sh
#ENTRYPOINT ["scripts/docker-entrypoint.sh"]
CMD [""]