Based off:
http://www.middlewareinventory.com/blog/server-provisioning-with-vagrant-and-ansible-apache-server-setup-example/


To run debug playbook:

1. Make inventory:

Run `vagrant ssh-config` and turn the output to:
```
[test]
127.0.0.1

[test:vars]
ansible_user = vagrant
ansible_port = 2222
ansible_ssh_private_key_file = ...
```

2. Run playbook

ansible-playbook -i inventory.yml -v debug-playbook.yml
