# -*- coding: utf-8 -*-
"""博客构建配置文件
"""

# For Maverick
site_prefix = "/"
source_dir = "../src/"
build_dir = "../dist/"
index_page_size = 10
archives_page_size = 20
enable_jsdelivr = {
    "enabled": True,
    "repo": "libiao163/libiao163.github.io@master"
}

# 站点设置
site_name = "悄悄生长"
site_logo = "${static_prefix}logo.png"
site_build_date = "2019-12-25T18:27+08:00"
author = "酒后的阿bill"
email = "libiao163@gmail.com"
author_homepage = "https://libiao163.github.io/"
description = "认真是我们参与这个社会的方式，认真是我们改变这个社会的方式"
key_words = ['Maverick', 'Galileo', 'blog']
language = 'zh-CN'
external_links = [
    {
        "name": "coolshell",
        "url": "https://coolshell.cn/",
        "brief": "陈皓"
    }
]
nav = [
    {
        "name": "首页",
        "url": "${site_prefix}",
        "target": "_self"
    },
    {
        "name": "归档",
        "url": "${site_prefix}archives/",
        "target": "_self"
    },
    {
        "name": "关于",
        "url": "${site_prefix}about/",
        "target": "_self"
    }
]

social_links = [
    {
        "name": "Twitter",
        "url": "https://twitter.com/",
        "icon": "gi gi-twitter"
    },
    {
        "name": "GitHub",
        "url": "https://github.com/libiao163",
        "icon": "gi gi-github"
    },
    {
        "name": "Weibo",
        "url": "https://weibo.com/6462830524/",
        "icon": "gi gi-weibo"
    }
]

head_addon = r'''
<meta http-equiv="x-dns-prefetch-control" content="on">
<link rel="dns-prefetch" href="//cdn.jsdelivr.net" />
'''

footer_addon = ''

body_addon = ''
