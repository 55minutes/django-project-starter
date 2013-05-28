# -*- mode: ruby -*-
# vi: set ft=ruby :

$script = <<EOD
#!/bin/bash

sudo aptitude update
sudo aptitude -y safe-upgrade
sudo add-apt-repository -y ppa:pitti/postgresql
sudo aptitude -y install curl git-core libpq-dev nginx postgresql python-software-properties ufw virtualenvwrapper
EOD

Vagrant.configure("2") do |config|
  config.vm.box = "digital_ocean"
  config.vm.box_url = "https://github.com/smdahlen/vagrant-digitalocean/raw/master/box/digital_ocean.box"
  config.vm.synced_folder '.', '/vagrant', disabled: true
  config.vm.provision :shell, inline: $script

  config.vm.define :preview do |preview|
    preview.vm.hostname = "preview"
  end

  config.vm.define :staging do |staging|
    staging.vm.hostname = "staging"
  end

  config.vm.define :production do |production|
    staging.vm.hostname = "production"
  end

  config.ssh.private_key_path = "#{Dir.home}/.ssh/id_rsa"
  config.ssh.username = "deployer"

  config.vm.provider :digital_ocean do |provider|
    provider.client_id = "TeSncJROljOJH4aPUrpJA"
    provider.api_key = "UyCLlH6UdZ8f980I5n2bwlvt46pHsEGFEctSHcyJa"
    provider.image = "Ubuntu 12.04 x32 Server"
    provider.ca_path = "/usr/local/opt/curl-ca-bundle/share/ca-bundle.crt"
  end
end
