# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

  config.vm.define "humidai" do |machine|
    machine.vm.box = "bento/ubuntu-16.04"
    machine.vm.hostname = "humidai.atomichost"
    machine.ssh.forward_agent = true
    machine.vm.provider "virtualbox" do |vb|
      vb.memory = "512"
      #vb.customize ["modifyvm", :id, "--nic2","natnetwork"]
      #vb.customize ["modifyvm", :id, "--nictype2","82540EM"]
      #vb.customize ["modifyvm", :id, "--nicpromisc2","allow-all"]   
    end
    machine.vm.network "private_network", ip: "192.168.33.5", virtualbox__intnet: "intnet"
    machine.vm.synced_folder "./humidai", "/home/vagrant/humidai", create: true, owner: "vagrant", group: "vagrant"
    machine.vm.provision "shell", inline: <<-SHELL
      sudo apt-get update
      sudo apt-get install -y libffi-dev python-dev libssl-dev python-pip htop tmux
      LC_ALL=C sudo pip install pip --upgrade
      LC_ALL=C sudo pip install ansible
      curl -fsSL get.docker.com | bash
      sudo usermod -aG docker vagrant
    SHELL
  end

  # Admin
  config.vm.define "admin" do |machine|
    machine.vm.box = "bento/ubuntu-16.04"
    machine.vm.hostname = "admin.atomichost"
    machine.vm.network "private_network", ip: "192.168.33.10" , virtualbox__intnet: "intnet"
    machine.vm.network "private_network", ip: "192.168.34.10"
    machine.vm.network "forwarded_port", guest: 162, host: 162, protocol: "udp"
    machine.vm.provider "virtualbox" do |vb|
      vb.memory = "512"
    end
    machine.vm.provision "shell" do |s|
      ssh_pub_key = File.open('humidai/id_rsa.pub') { |f| f.read }
      s.inline = <<-SHELL
        echo "#{ssh_pub_key}" >> /home/vagrant/.ssh/authorized_keys
      SHELL
    end
  end

  # Virtual Router
  2.times do |i|
    config.vm.define "vyos%#02d" % (i+1) do |machine|
      machine.vm.box = "higebu/vyos"
      machine.vm.hostname = "vyos%#02d.atomichost" % (i+1)
      machine.vm.network "private_network", ip: "192.168.33.%#02d" % (21+i), virtualbox__intnet: "intnet"
      machine.vm.network "private_network", ip: "192.168.34.%#02d" % (21+i)
      machine.vm.provider "virtualbox" do |vb|
        vb.memory = "256"
      end
    end
  end

  # Load Balancer
  2.times do |i|
    config.vm.define "lb%#02d" % (i+1) do |machine|
      machine.vm.box = "bento/ubuntu-16.04"
      machine.vm.hostname = "lb%#02d.atomichost" % (i+1)
      machine.vm.network "private_network", ip: "192.168.33.%#02d" % (30+i), virtualbox__intnet: "intnet"
      machine.vm.provider "virtualbox" do |vb|
        vb.memory = "256"
      end
      machine.vm.provision "shell" do |s|
        ssh_pub_key = File.open('humidai/id_rsa.pub') { |f| f.read }
        s.inline = <<-SHELL
          echo "#{ssh_pub_key}" >> /home/vagrant/.ssh/authorized_keys
        SHELL
      end
    end
  end

  # Application
  2.times do |i|
    config.vm.define "app%#02d" % (i+1) do |machine|
      machine.vm.box = "bento/ubuntu-16.04"
      machine.vm.hostname = "app%#02d.atomichost" % (i+1)
      machine.vm.network "private_network", ip: "192.168.33.%#02d" % (40+i), virtualbox__intnet: "intnet"
      machine.vm.provider "virtualbox" do |vb|
        vb.memory = "256"
      end
      machine.vm.provision "shell" do |s|
        ssh_pub_key = File.open('humidai/id_rsa.pub') { |f| f.read }
        s.inline = <<-SHELL
          echo "#{ssh_pub_key}" >> /home/vagrant/.ssh/authorized_keys
        SHELL
      end
    end
  end
end
