# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  
  config.vm.define "master1", primary: true do |master|
    master.vm.box = "godfryd/lxc-ubuntu-18.04"
  end
  
  config.vm.define "k1" do |k1|
    k1.vm.box = "godfryd/lxc-ubuntu-18.04"
  end

  config.vm.define "k2" do |k2|
    k2.vm.box = "godfryd/lxc-ubuntu-18.04" 
  end

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "playbook.yml"
    ansible.compatibility_mode = "2.0"
    ansible.inventory_path = "./inventories/dev/lxd.py"
    ansible.groups = {
      "master" => ["master[0:4]"],
      "workers" => ["worker[0:8]"]
    }
  end
end
