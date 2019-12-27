---
layout: post
title: mysql脚本
slug: delete_big_tables
date: 2019-12-27 16:23
status: publish
author: 酒后的阿bill
categories:
  - devops
tags:
  - mysql
  - shell
excerpt: mysql相关shell脚本
---

- 删除大数据表

```bash
#!/bin/bash
#
dbname='dbname'
tabname='tablename'
step='10000'
sleeptime=1
start_index=30000001
end_index=39938589
MYSQL="mysql -u[user] -p[password] -t -e "

i_start=$start_index
i_end=$(expr "$start_index" + "$step")
i_end=$(expr "$i_end" - 1)
if [ $i_end -gt $end_index ]; then
  i_end=$end_index
fi
while [ $i_end -le $end_index ]; do
    echo "start delete from $i_start to $i_end"
    mysql delete delete from yitain where id >= $i_start and id <= $i_end
    #$MYSQL "delete from $dbname.$tabname where id >= $i_start and id <= $i_end;"
    i_start=$(expr "$i_end" + 1)
    i_end=$(expr "$i_end" + "$step")
    if [ $i_start -gt $end_index ]; then
        break
    fi
    if [ $i_end -gt $end_index ]; then
      i_end=$end_index
    fi
    sleep $sleeptime
done
```

- 统计最大的前十个表

```bash
#!/bin/bash
MYSQL="mysql -u[user] -t -e "
TMP_FILE=biggest_table.txt

echo "db 最大的十张表" >$TMP_FILE

$MYSQL "SELECT CONCAT(table_schema, '.', table_name), CONCAT(ROUND(table_rows / 1000000, 2), 'M') rows, CONCAT(ROUND(data_length / ( 1024 * 1024 * 1024 ), 2), 'G')                    DATA, CONCAT(ROUND(index_length / ( 1024 * 1024 * 1024 ), 2), 'G')                   idx,CONCAT(ROUND(( data_length + index_length ) / ( 1024 * 1024 * 1024 ), 2), 'G') total_size,ROUND(index_length / data_length, 2)                                           idxfrac FROM   information_schema.TABLES where table_schema = 'db' ORDER  BY data_length + index_length DESC LIMIT  10;" >>$TMP_FILE
```

- 检查Mariadb galera集群的健康状态

```bash
#/bin/bash

MYSQL_USERNAME="root"

if $1; then
    MYSQL_PASSWORD="{{ mysql_root_pass }}"
else
    MYSQL_PASSWORD=""
fi

ERR_FILE="/dev/null"
DEFAULTS_EXTRA_FILE="/etc/my.cnf"
TIMEOUT=10
EXTRA_ARGS=""

function service_status()
 {
    if [[ -n "$MYSQL_USERNAME" ]]; then
        EXTRA_ARGS="$EXTRA_ARGS --user=${MYSQL_USERNAME}"
    fi
    if [[ -n "$MYSQL_PASSWORD" ]]; then
        EXTRA_ARGS="$EXTRA_ARGS --password=${MYSQL_PASSWORD}"
    fi

    if [[ -r $DEFAULTS_EXTRA_FILE ]];then
        MYSQL_CMDLINE="/usr/local/mysql/bin/mysql --defaults-extra-file=$DEFAULTS_EXTRA_FILE -nNE --connect-timeout=$TIMEOUT \
                        --user=${MYSQL_USERNAME} --password=${MYSQL_PASSWORD}"
    else
        MYSQL_CMDLINE="/usr/local/mysql/bin/mysql -nNE --connect-timeot=$TIMEOUT --user=${MYSQL_USERNAME} --password=${MYSQL_PASSWORD}"
    fi

    wsrep_local_state=$($MYSQL_CMDLINE -e "SHOW STATUS LIKE 'wsrep_local_state';" 2>${ERR_FILE} | tail -1 2>>${ERR_FILE})
    wsrep_local_state_comment=$($MYSQL_CMDLINE -e "SHOW STATUS LIKE 'wsrep_local_state_comment';" 2>${ERR_FILE} | tail -1 2>>${ERR_FILE})
    wsrep_cluster_status=$($MYSQL_CMDLINE -e "SHOW STATUS LIKE 'wsrep_cluster_status';" 2>${ERR_FILE} | tail -1 2>>${ERR_FILE})

    if [[ "${wsrep_cluster_status}" == "Primary" ]] && [[ "${wsrep_local_state_comment}" == "Synced" && "${wsrep_local_state}" == "4" ]]
    then
        echo "true"
    else
        echo "false"
    fi
 }

function exec_next()
{
    taga="true"
    while $taga
    do
        if `service_status`; then
            taga="false"
        else
            sleep 5s
        fi
    done
}

`exec_next`#u
```
