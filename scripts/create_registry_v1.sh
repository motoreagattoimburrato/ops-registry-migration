#!/usr/bin/env bash

docker_images=( "nginx:1.22"
                "nginx:1.21"
                "nginx:1.20"
                "haproxy:lts"
                "haproxy:2.5"
                "haproxy:1.8"
                "maven:latest"
                "maven:3.8.5-openjdk-11-slim"
                "maven:3.8.5-jdk-8-slim" )

SET_INSECURE_REGISTRY=no

echo "$(date --utc) - [INFO]: Run this script as superuser"
echo "$(date --utc) - [INFO]: This script will create on localhos one v1 and one v2 type docker registries (registry1 to 5001 and registry2 to 5002)"

if [[ $SET_INSECURE_REGISTRY == "yes" ]]
then
  echo "$(date --utc) - [INFO]: steup docker insecure registry"
  echo "{ \"insecure-registries\":[\"localhost:5001\", \"localhost:5002\"] }" > /etc/docker/daemon.json
  systemctl restart docker.service
else
  echo "$(date --utc) - [INFO]: make sure did you have set insecure registry in '/etc/docker/daemon.json' (insecure string: '{ \"insecure-registries\":[\"localhost:5001\", \"localhost:5002\"] }'')"
fi

echo "$(date --utc) - [INFO]: requirements (pull and volumes) registry docker"
docker pull registry:2
docker pull registry:0.8.1
docker volume create registry1
docker volume create registry2

echo "$(date --utc) - [INFO]: create registry1 (port 5001)"
docker run -d -p 5001:5000 --restart=always --name registry1 -v registry1:/var/lib/registry registry:0.8.1

echo "$(date --utc) - [INFO]: create registry1 (port 5002)"
docker run -d -p 5002:5000 --restart=always --name registry2 -v registry2:/var/lib/registry registry:2

echo "$(date --utc) - [INFO]: pull and import some images in registry1 (5001)"

for image in "${docker_images[@]}"
do
  echo "$(date --utc) - [INFO]: pulling $image from default registry"
  docker pull $image
  echo "$(date --utc) - [INFO]: tag $image for registry1"
  docker tag $image localhost:5001/$image
  echo "$(date --utc) - [INFO]: pushing $image to registry1"
  docker push localhost:5001/$image
done

echo "$(date --utc) - [INFO]: at the end of tests, you can run this comand to cleanup: \n 'docker stop registry1 registry2 ; docker system prune -a -f'"
