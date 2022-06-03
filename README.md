# Registry Migration OPS script

This is a `python` script (python v3.8) that will migrate a registry to another registry (today onyl v2 to v2).

Comands to launch

```
git clone https://github.com/motoreagattoimburrato/ops-registry-migration.git
cd ops-registry-migration
# change vars -> see paragraphs below
chmod a+x main.py
python3 main.py
```

## Requirements

Before start, you need to install these python(3) [modules](./requirements.txt):

```
docker==5.0.2
requests==2.26.0
jsonref==0.2
jsonschema==3.2.0
simplejson==3.16.0
```

You can do it using the following comand:

```
pip3 install --requirement ./requirements.txt
```

## Before the run

Before run `main.py`, change the following variables with those most appropriate for you case.

```
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
```

## Testing the script

I made a [bash script](./scripts/create_registry_v2.sh) that can create two type v2 docker registry to test this script (needs SuperUser).

```
chmod a+x ./scripts/create_registry_v2.sh ; ./scripts/create_registry_v2.sh
```

## To Do list

- [ ] check if docker official registry (is necessary email in login) -> `client.login(username=user, password=passwd, email=EMAIL, registry='https://index.docker.io/v1/')`
- [ ] check if registry is v1 type and create functions
- [ ] improve logging
- [ ] check and use if registry images needs token/tls_cert/credentials (GET)
- [ ] create CI and QA check
