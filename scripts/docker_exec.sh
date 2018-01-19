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

if [ "$(docker ps -f name=$CONTAINER_NAME | grep -w $CONTAINER_NAME$)" ]; then
    echo "Container exists, exec it."
    CMD="docker exec -it $(docker ps -a -f name=$CONTAINER_NAME | grep -w $CONTAINER_NAME$ | awk '{print $1}') bash"
    echo $CMD
    eval $CMD
else
    echo "Container is not running, please run it first by exec docker_run.sh!"
fi