# How to prepare test machine

```
$ sudo apt-get install virtualbox
$ sudo dpkg -i vagrant_2.0.0_x86_64.deb
$ vagrant plugin install vagrant-vyos
```

# Lunch

```
$ eval $(ssh-agent)
$ ssh-add humidai/id_rsa
$ cd humidai
$ ssh-keygen -t rsa
$ vagrant up
```

# How to prepare nodes

```
$ vagrant ssh humidai
$ ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i inventory/hosts_vyos playbook_vyos.yml
$ ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i inventory/hosts_base playbook_base.yml
$ ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i inventory/hosts_admin playbook_admin.yml
$ ansible-playbook -i localhost, -c local playbook_admin2.yml
```

# Build Docker Image
```
$ vagrant ssh humidai
$ sudo sed -i -e "s%/usr/bin/dockerd -H fd://%/usr/bin/dockerd -H fd:// --insecure-registry=192.16833.10:5000%g" /lib/systemd/system/docker.service
$ systemctl daemon-reload
$ sudo service docker restart

$ docker build -t gluster .
$ docker tag gluster 192.168.33.10:5000/gluster
$ docker push 192.168.33.10:5000/gluster
```

# Deploy LoadBalancer and Application Server

```
$ ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i inventory/hosts_lb playbook_lb.yml
$ ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i inventory/hosts_app playbook_app.yml
```
