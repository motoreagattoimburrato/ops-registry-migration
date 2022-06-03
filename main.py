#!/usr/bin/env python
__author__ = "Luca Capanna"
__copyright__ = "Copyright 2022"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Luca Capanna"
__status__ = "Beta"

import json
import docker
import requests as rq

# TO DO:
# - if docker official registry is necessary email -> client.login(username=user, password=passwd, email=EMAIL, registry='https://index.docker.io/v1/')
# - if registry is v1 type
# - improve logging
# - improve GET registry images with token/tls_cert

### Configuration vars
# old registry name
old_registry = "localhost:5001"
# new registry name
new_registry = "localhost:5002"
# username old registry (optional)
#old_user = "changeme"
# password old registry (optional)
#old_passwd = "changeme"
# username new registry (optional)
# new_user = "changeme"
# password new registry (optional)
# new_passwd = "changeme"

# check if you docker CLI and status
def docker_health_check(client):
    print("Health check Docker CLI")
    print(json.dumps(client.info(), indent=4))
    print(json.dumps(client.version(), indent=4))

# login docker registry
def docker_login_registry(client, user, passwd, registry):
    print(f"Login registry -> {registry}")
    # change https if necessary
    url_registry = 'http://' + registry
    client.login(username=user, password=passwd, registry=url_registry)
    client.ping()

# listing docker images from remote registry (return array)
def docker_list_remote_images(registry):
    # change https if necessary
    docker_images_list = []
    images_list = rq.get(f"http://{registry}/v2/_catalog").json()['repositories']
    print(images_list)
    for image in images_list:
        print(image)
        tags_list = rq.get(f"http://{registry}/v2/{image}/tags/list").json()['tags']
        print(tags_list)
        for tag in tags_list:
            print(tag)
            image_name = old_registry + "/" + image + ":" + tag
            docker_images_list.append(image_name)
    return docker_images_list

# exec docker pull and docker push
def docker_pull_and_push(client, old_image, new_image):
    print(f"moving {old_image} TO--> {new_image} ... Pulling..")
    client.images.pull(old_image)
    client.images.get(old_image).tag(new_image)
    print(f"moving {old_image} TO--> {new_image} ... Pushing..")
    client.images.push(new_image)
    client.images.remove(old_image)
    client.images.remove(new_image)
    print("Image successfully migrated!")

def docker_migrator():
    client = docker.from_env()
    docker_health_check(client)

    if 'old_user' and 'old_passwd' in globals():
        docker_login_registry(client, old_user, old_passwd, old_registry)

    if 'new_user' and 'new_passwd' in globals():
        docker_login_registry(client, new_user, new_passwd, new_registry)

    docker_list_remote_images(old_registry)

    for image_name in docker_list_remote_images(old_registry):
        old_image = image_name.strip()
        new_image = old_image.replace(old_registry, new_registry)

    docker_images_list = docker_list_remote_images(old_registry)
    for image_name in docker_images_list:
        old_image = image_name.strip()
        new_image = old_image.replace(old_registry, new_registry)
        print(f"from {old_image} to {new_image}")
        docker_pull_and_push(client, old_image, new_image)

    print(f"Registry Migrated!")

if __name__ == '__main__':
    docker_migrator()
    print("Done")
