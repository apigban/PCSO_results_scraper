#!/usr/bin/env bash
#

set -x

container=$(buildah from python:3.8.2)

buildah config --label maintainer="Alain Igban <apigban@gmail.com>" $container

buildah run $newcontainer groupadd python
buildah run $newcontainer useradd -g python -m python
buildah config --user python $container
buildah config --workingdir /home/python $newcontainer
