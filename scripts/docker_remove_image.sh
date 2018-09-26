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

if [ "$(docker image ls | awk '{print $1, $2}' | grep -w $APP_NAME | grep $APP_TAG)" ]; then
    echo "Removing image!"
    CMD="docker image ls | awk '{print \$1, \$2, \$3}' | grep -w $APP_NAME | grep -w $APP_TAG | awk '{print \$3}' | xargs docker rmi"
    echo $CMD
    eval $CMD
else
    echo "Image not exists!"
fi


