# Ansible experiment with docker targets

This is built from following "Mastering Ansible" course on Udemy.

Quite a lot of changes were applied because the course material was quite old and recent Ansible has had a lot of changes.
I also couldn't find the course resources so I hacked a flask app to follow along. That lead to a tangent to a lot more experimentations.
The result is that it does deviate from the course but thats apart of the play.

`docker-compose` is used to create the target hosts for ansible to configure. It is really nice to be able to spin up a lot of targets up and down as required to test.

I'm running OSX with docker-machine.

## 1. Setup Infrastructure

### 1.1. Setup Ansible vault password

This will be the password for the database user in the demo flask app. Its not a super secure method, but its fine for a locked down demo purpose on a local docker-machine.
It exercises the Ansible vault tool.

```sh
# Be in this repo folder
# ansible.cfg refers to this file for the password to access encrypted secrets
echo "(choose a vault password)" > vault_pass.txt

# This folder holds all the variables for this site
cd group_vars/all

# Create a new secret file. It will open up an editor to write secrets
ansible-vault create --vault-password-file ../../vault_pass.txt vault
```

In the editor add the following, save and exit:
```
vault_db_password: (choose a db password)
```

You'll find that `group_vars/all/vars.yml` refers to this variable for the db password



### 1.2. Build container image

I am using a generic container that ansible will configure into various types of servers. The image needs to have `ssh` and `python3` for ansible. It effectively just serves `sshd`

A local file `key.pub` will be baked into the image for access.

```sh
# Pick a ssh public key that will be added to the container's authorized_keys file
cp ~/.ssh/<pick a .pub key> key.pub

# Build container image
docker build -t local:ansibletarget .
```

### 1.3. Spin up infrastructure

```sh
# Spin up containers
docker-compose up -d
```
Each container will have a 1002x port mapped for `ssh` access on the docker-machine host. They will also have additional ports opened depending on their purpose

```sh
# Review containers
docker ps
```

**Special mentions**:

Container | Port | Comment |
--- | --- | --- |
lb01 | 9080 (80) | Static website on load balancer |
lb01 | 9081 (81) | Flask app on load balancer |
db01 | 13306 (3306) | Mysql port for debugging / dev/ test |
adminer | 8080 | adminer app to test/view database |

```sh
# Test ssh access

# Find the docker-machine ip
docker-machine ip
192.168.99.100

# ssh to first container
# add -i (key) as needed
ssh root@192.168.99.100 -p 10021
```

### 1.4. How to destroy when done

```sh
docker-compose down
```
You can also do a quick down/up to restart the whole experiment


## 2. Running Configuration Management

### 2.1. Run site.yml
Everything is in `site.yml`

```sh
ansible-playbook site.yml
```

Check out the contents of `site.yml` for the imported playbooks. You can also run the specific playbooks.

Other variants

```sh
# Check out the hosts and plays
ansible-playbook site.yml --list-hosts

# e.g. Run only against matches against webapp group
ansible-playbook site.yml --limit webapp

# Check out the tags that you can run against
ansible-playbook site.yml --list-tags

# e.g. Run only `packages` tasks
ansible-playbook site.yml --tags packages

# Check out the tasks to be executed
ansible-playbook site.yml --list-tasks

# Pretend run (no actions)
ansible-playbook site.yml --check
```

### 2.2. Other playbooks

playbook | What does it do |
--- | --- |
hostname.yml | Runs `hostname` on each inventory host. From the tutorial. |
stack_status.yml | A Utility playbook to check that each thing we care about is running properly through Ansible. |
stack_restart.yml | A Utility playbook that restarts the main service of each host. |


### 2.3. Little things

To nuke a container and start it again, you can do something like:

```sh
# Lets say we want to nuke lb01

# Kill it from docker process
docker stop lb01 && docker rm lb01

# Let docker-compose bring it back up
docker-compose up -d

# Run site, but only config lb01. You could also do just playbook/loadbalancer.yml
ansible-playbook site.yml --limit lb01
```


## 3. Seeing results

Check `docker-machine ip`. The following examples will be based on `192.168.99.100`

URL | What's there |
--- | --- |
http://192.168.99.100:9080 | The static website. Reload multiple times to see it switch between the backends |
http://192.168.99.100:9081 | The test flask app that talked to the db. Reload multiple times to see it switch between backends |
http://192.168.99.100:8080 | Adminer to see the contents of the database (this is a debug tool, and was not configured by Ansible) |