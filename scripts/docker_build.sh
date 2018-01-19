#!/bin/bash

CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd )"
#echo $CURRENT_DIR

PARENT_DIR="$(dirname "$CURRENT_DIR")"
echo $PARENT_DIR

source $CURRENT_DIR/app_config.sh

CHECKING=APP_NAME
if [ -z ${!CHECKING+x} ]; then
  echo "$CHECKING is unset!";
  exit;
else
  echo "$CHECKING is set to '${!CHECKING}'!";
fi;

CMD="docker build -t $APP_NAME:$APP_TAG $PARENT_DIR --file $CURRENT_DIR/Dockerfile"
echo $CMD
$CMD
echo END="$CMD"
