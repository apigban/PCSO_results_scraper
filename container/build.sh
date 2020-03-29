#!/usr/bin/env bash
#

set -xe

containerID=$(buildah from python:3.8.2)
newImageName="devtool"

buildah config --label maintainer="Alain Igban <apigban@gmail.com>" $containerID

buildah run $containerID groupadd pythonsvc
buildah run $containerID useradd -g pythonsvc -m pythonsvc
buildah config --user pythonsvc:pythonsvc $containerID 
buildah config --workingdir /home/pythonsvc $containerID  

# Install python dependencies
#buildah run $containerID pip3 install requests sqlalchemy lxml
buildah run $containerID pip install poetry


# Copy repo to container
# buildah copy --chown pythonsvc:pythonsvc $containerID ../

buildah copy --chown pythonsvc:pythonsvc $containerID entrypoint.sh

# Set entrypoint
buildah config --entrypoint /home/pythonsvc/container/entrypoint.sh $containerID

# Save the container as an image
buildah commit $containerID $newImageName