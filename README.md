# masekube
Ansible implementation of a minimal Kubernates Cluster with Keycloak for development purposes.

* Currently uses the Vagrant LXD provider so I can spin up lots of nodes on modest hardware.

This is really only used as a playground for developing and testing kubernetes behaviour. I make no guarantees that I've done anything correctly and if you know I've messed up, a github issue is always welcome. 


```
## Requirements

* Ubuntu 18.04+ (currently only tested)
* LXD
* Vagrant
* Vagrant LXD plugin
* Ansible must be installed on the host
* Python 
* Git


## Fetch the role requirements

```
$ ansible-galaxy install -r requirements.yml
$ vagrant up
```

