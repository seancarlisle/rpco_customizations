#!/bin/sh

#############################################################################
#                                                                           #
# Copyright 2019 Rackspace                                                  #
#                                                                           #
# Simple script to ensure that a target instance has its oom_score_adj      #
# score set to -1000 to prevent OOM killer from killing the instance.       #
#                                                                           #
# Meant to be used in conjunction with CRON                                 #
#                                                                           #
#############################################################################

if [ "$1" == "" ] || [ "$1" == "-h" ]
then
   echo "Usage: oom_score_adjuster.sh <instance id>"
fi

# Get the instance ID
INSTANCE="$1"
PID=$(ps -ef | grep 'libvirt+' | awk -v instance=$INSTANCE '$0 ~ instance {print $2}')

# Ensure oom_score_adj is -1000
if [ "$PID" == "" ]
then
   echo "Instance not found, exiting"
   exit 1
fi

if [ "$(cat /proc/$PID/oom_score_adj)" != "-1000" ]
then
   echo "Setting oom_score_adj"
   echo "-1000" > /proc/$PID/oom_score_adj
else
   echo "oom_score_adj for instance $INSTANCE already set to -1000. Nothing to do"
fi

exit 0
