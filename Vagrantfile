# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "centos/7"
  config.vm.synced_folder ".", "/vagrant", disabled: true
  
  config.vm.provider "virtualbox" do |vb|
      vb.memory = 3256
      vb.cpus = 2
  end
  
  config.vm.define "mysqlserver" do |mysqlserver|
    mysqlserver.vm.hostname = "vmmysqlserver"
    mysqlserver.vm.network :forwarded_port, host: 33306, guest: 3306
    mysqlserver.vm.network :forwarded_port, host: 33307, guest: 3307
    mysqlserver.vm.network :forwarded_port, host: 33308, guest: 3308
    mysqlserver.vm.network :forwarded_port, host: 33309, guest: 3309
    mysqlserver.vm.network :forwarded_port, host: 28080, guest: 80

    #mysqlserver.vm.provision :shell, inline: "yum-config-manager --disable epel", privileged: true
    #mysqlserver.vm.provision :shell, path: "provision-mysql-yum-repo-el7.sh", privileged: true
    #mysqlserver.vm.provision :shell, path: "provision-mysql-community-57-el7-yum.sh", privileged: true

    mysqlserver.vm.provision :shell, path: "fabric-demo-install.sh", privileged: true
  end  
 
end
