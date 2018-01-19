#!/bin/bash

CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd )"
#echo $CURRENT_DIR

PARENT_DIR="$(dirname "$CURRENT_DIR")"
echo $PARENT_DIR

source $CURRENT_DIR/app_config.sh

function check(){
    CHECKING=$1
    if [ -z ${!CHECKING+x} ]; then
      echo "$CHECKING is unset!";
      exit;
    else
      echo "$CHECKING is set to '${!CHECKING}'!";
    fi;
}
check APP_NAME

CONTAINER_NAME=$APP_NAME"_"$APP_TAG

if ! [ "$(docker ps -a -f name=$CONTAINER_NAME | grep -w $CONTAINER_NAME$)" ]; then
    echo "Container not exist, run it first."
    CMD="docker run --name=$CONTAINER_NAME $PORT_MAPPING $VOLUME_MAPPING -it $APP_NAME:$APP_TAG $DOCKER_CMD"
    echo $CMD
    eval $CMD
else
    if [ "$(docker ps -f name=$CONTAINER_NAME | grep -w $CONTAINER_NAME$)" ]; then
        echo "Container is already running!"
    else
        echo "Container exists, start it."
        CMD="docker ps -a -f name=$CONTAINER_NAME | grep -w $CONTAINER_NAME$ | awk '{print \$1}' | xargs docker start"
        echo $CMD
        eval $CMD
    fi
fi

