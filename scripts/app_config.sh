#!/bin/bash

SCRIPTS_DIR=$(cd "$(dirname "$0")";pwd)
echo SCRIPTS_DIR=$SCRIPTS_DIR

APP_DIR=$(dirname $SCRIPTS_DIR)
echo APP_DIR=$APP_DIR

APP_NAME=$(basename $APP_DIR)
echo APP_NAME=$APP_NAME

export APP_NAME=$APP_NAME

export APP_TAG=v0.1

export PORT_MAPPING="-p 8888:8888"

export VOLUME_MAPPING="-v $PARENT_DIR/src:/docker_app/src"

export DOCKER_CMD="bash"
#export DOCKER_CMD="ipython notebook --no-browser --port 8888 --ip=* --NotebookApp.password='$HASH' --allow-root"
