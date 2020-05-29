#!/bin/bash
username=$1

# Related to https://teletype.in/@kiriharu/L-JrWt0Kq

check_service(){
if [ -f /etc/systemd/system/docker@.service ]; then
echo -e "\e[33m* Service exists, skipping\e[0m"
else
echo -e "\e[31m* Service not exists, creating file and service\e[0m"
touch /etc/systemd/system/docker@.service
cat >> /etc/systemd/system/docker@.service << EOF
[Unit]
Description=Docker Application Container Engine
Documentation=https://docs.docker.com
After=network-online.target firewalld.service containerd.service
Wants=network-online.target

[Service]
Type=notify
ExecStart=/usr/bin/dockerd -H unix:// --containerd=/run/containerd/containerd.sock \
                  --userns-remap %i \
                  --host unix:///var/run/docker-%i.sock \
                  --pidfile /var/run/docker-%i.pid
ExecReload=/bin/kill -s HUP $MAINPID
TimeoutSec=0
RestartSec=2
Restart=always
StartLimitBurst=3
StartLimitInterval=60s
LimitNOFILE=infinity
LimitNPROC=infinity
LimitCORE=infinity
TasksMax=infinity
Delegate=yes
KillMode=process
[Install]
WantedBy=multi-user.target
EOF
fi

systemctl daemon-reload
}

change_visudo(){
echo -e "\e[33m* Changing visudo... \e[0m"
cat >> /etc/sudoers << EOF
$username ALL=(root) NOPASSWD: /usr/bin/docker -H unix\:///var/run/docker-$username.sock *, ! /usr/bin/docker *--priviledged*, ! /usr/bin/docker *host*
EOF
}

change_uidguid(){
echo -e "\e[33m* Changing subuid and subguid... \e[0m"
uid=$(id -u $username)
sed -i.bak_$(date +%s) "/$username/d" /etc/subuid
sed -i.bak_$(date +%s) "/$username/d" /etc/subgid
multiplier=$(($uid - 1000))
cat >> /etc/subuid << EOF
$username:$uid:1
$username:$((100000 + 65536 * $multiplier)):65536
EOF
cat >> /etc/subgid << EOF
$username:$uid:1
$username:$((100000 + 65536 * $multiplier)):65536
EOF
}

systemd_operations(){
echo -e "\e[33m* Starting services... \e[0m"
systemctl start docker@$username.service
systemctl enable docker@$username.service
}

alias_add(){
if [ -f /etc/profile.d/00-dockeralias.sh ]; then
echo -e "\e[33m* /etc/profile.d/00-dockeralias.sh exist. Skipping... \e[0m"
else
echo -e "\e[31m* /etc/profile.d/00-dockeralias.sh, creating... \e[0m"
touch /etc/profile.d/00-dockeralias.sh
chmod 555 /etc/profile.d/00-dockeralias.sh
echo 'alias docker="sudo docker -H unix:///var/run/docker-$(whoami).sock"' >> /etc/profile.d/00-dockeralias.sh
fi
}

check_service
change_visudo
change_uidguid
systemd_operations
alias_add
echo -e "\e[33m* Done! \e[0m"

