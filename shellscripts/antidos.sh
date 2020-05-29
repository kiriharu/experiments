#!/bin/sh

# Скрипт для бана различных досилок по IPTables.
# Находим все соединения на все порты и записываем их в файл iplist_raw
netstat -ntu | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -nr | grep -v "127.0.0.1" > iplist_raw
# Находим все соединения, которые больше 50 (цифру можна поменять) и записываем их в iplist
awk '{if ($1 > 50) { print $2 }}' iplist_raw > iplist
#Если какой-то ip из iplist есть в whitelist - пропускаем его, остальные добавляем в banlist
grep -vf whitelist iplist > banlist
#Создаем файл с правилами для iptables по бану данных IP
awk '{print "/sbin/iptables -A INPUT -s " $1 " -j DROP"; print "/sbin/iptables -A INPUT -d " $1 " -j DROP";}' banlist > iptables_ban.sh