#!/bin/bash

export VAGRANT_HTTP_PROXY=${http_proxy}
export VAGRANT_YUM_HTTP_PROXY=${http_proxy}
export VAGRANT_HTTPS_PROXY=${http_proxy}
export VAGRANT_FTP_PROXY=${http_proxy}
export VAGRANT_NO_PROXY=${no_proxy},/var/run/docker.sock

echo "launch virtual cluster"

vagrant up --parallel
