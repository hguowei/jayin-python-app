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
echo $CONTAINER_NAME

if [ "$(docker ps -q -f name=$CONTAINER_NAME | grep -w $CONTAINER_NAME$)" ]; then
    echo "Container not exists!"
else
    if [ "$(docker ps -a -f status=exited -f name=$CONTAINER_NAME | grep -w $CONTAINER_NAME$)" ]; then
        echo "Removing container!"
        CMD="docker ps -a -f name=$CONTAINER_NAME | grep -w $CONTAINER_NAME$ | awk '{print \$1}' | xargs docker rm"
        echo $CMD
        eval $CMD
    else
        echo "Container is running, please rm 'docker_stop.sh' to stop it first."
    fi
fi


