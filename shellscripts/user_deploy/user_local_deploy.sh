#!/bin/bash
username=$1

create_user(){
    useradd -m -s /bin/bash $username
    mkdir /home/$username/.ssh
}

add_to_sudoers(){
    echo $username 'ALL=(ALL)       NOPASSWD: ALL' >> /etc/sudoers
}

grant_ssh_key() {
cat >> /etc/ssh/sshd_config << EOF

Match User $username
    PasswordAuthentication no
    PubkeyAuthentication yes
EOF
}

create_user
add_to_sudoers
grant_ssh_key
systemctl restart sshd
