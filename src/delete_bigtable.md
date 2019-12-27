---
layout: post
title: 删除大表shell脚本
slug: delete_big_tables
date: 2019-12-27 16:23
status: publish
author: 酒后的阿bill
categories:
  - devops
tags:
  - mysql
  - shell
excerpt: 删除大表shell脚本
---

####为了删除一些特别大的表

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
