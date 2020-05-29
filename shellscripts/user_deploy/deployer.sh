#!/bin/bash

# Usage: deployer.sh <hostname> <username> <deploy_user>
# Require sshpass

hostname=$1
username=$2
deploy_user=$3

script="user_local_deploy.sh"
no_fp="StrictHostKeyChecking=no"
key_path="/home/$(whoami)/.ssh/id_rsa"
pubkey_path="$key_path.pub"

echo -e "Input password for user $username:"
read password

function ssh_command(){
   sshpass -p $password ssh -o $no_fp ${username}@${hostname} $1
}

function scp_command(){
   sshpass -p $password scp -o $no_fp $1 ${username}@${hostname}:$2
}

function copy_script_to_server(){
    echo -e "\e[32m*** Copying  script to server...\e[0m"
    scp_command $script "/tmp/$script"
    ssh_command "chmod +x /tmp/$script"
}

function run_script_and_wait(){
    echo -e "\e[32m*** Running local script on server\e[0m"
    ssh_command "sh /tmp/$script $deploy_user"
    echo -e "\e[32m*** Sleeping 10 sec\e[0m"
    sleep 10
    echo -e "\e[42m*** Sleeping done!\e[0m"
}

function ssh_keygen(){
    echo -e "\e[32m*** Running ssh keygen \e[0m"
    if [ -f $pubkey_path ]; then
        echo -e "\e[33m*** $pubkey_path exist. Skipping... \e[0m"
    else 
       echo -e "\e[31m*** $pubkey_path does not exist, creating... \e[0m"
       ssh-keygen -t rsa -f $key_path -q -P ""
    fi
}

function move_pubkey(){
    echo -e "\e[32m *** Moving pubkey \e[0m"
    scp_command $pubkey_path "/tmp/id_rsa.pub"
    ssh_command "cat /tmp/id_rsa.pub >> /home/$deploy_user/.ssh/authorized_keys"
    ssh_command "chmod 600 /home/$deploy_user/.ssh/authorized_keys"
    ssh_command "chown -R $deploy_user:$deploy_user /home/$deploy_user"
}




echo -e "\e[31m#####  ###### #####  #       ####  #   # ###### #####  \e[0m"
echo -e "\e[32m#    # #      #    # #      #    #  # #  #      #    # \e[0m"
echo -e "\e[33m#    # #####  #    # #      #    #   #   #####  #    # \e[0m"
echo -e "\e[34m#    # #      #####  #      #    #   #   #      #####  \e[0m"
echo -e "\e[35m#    # #      #      #      #    #   #   #      #   #  \e[0m"
echo -e "\e[36m#####  ###### #      ######  ####    #   ###### #    # \e[0m"

copy_script_to_server
ssh_keygen
run_script_and_wait
move_pubkey

echo -e "\e[42m***SCRIPT DONE! CHECK SSH!***\e[0m"

