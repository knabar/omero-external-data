#!/bin/bash

# Copyright (c) 2013 Glencoe Software, Inc. All rights reserved.
#
# This software is distributed under the terms described by the LICENCE file
# you can find at the root of the distribution bundle.
# If the file is missing please request a copy by contacting
# support@glencoesoftware.com.

cd settings
for setting in *
do
    echo $setting ":"
    cat $setting
    omero config set --file $setting $setting
done
