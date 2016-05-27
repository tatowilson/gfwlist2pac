# gfwlist2pac -- python3 ONLY

fork from clowwindy's gfwlist2pac

##Automatically update the PAC for ShadowsocksX

Thanks to VincentSit's [bash script](https://gist.github.com/VincentSit/b5b112d273513f153caf23a9da112b3a)  
I modified it a little, and It's also ONLY tested on OS X.  

Before executing, make sure it has the permission, or you can execute the following code first:  

```
chmod +x update_gfwlist.sh
```

and then:

```
./update_gfwlist.sh
```

##The basic usage:

If you don't wanna use the automatically update bash script or it doesn't work for some reason, you can run the python script `main.py` manually.

Example & Usage:

```
python3 main.py -i gfwlist.txt -f gfwlist.js -p "SOCKS5 127.0.0.1:1080; DIRECT;" --user-rule myrule --precise

optional arguments:
     -h, --help            show this help message and exit
     -i GFWLIST, --input GFWLIST
                           path to gfwlist
     -f PAC, --file PAC    path to output pac
     -p PROXY, --proxy PROXY
                           the proxy parameter in the pac file, for example,
                           "SOCKS5 127.0.0.1:1080;"
     --user-rule USER_RULE
                           user rule file, which will be appended to gfwlist
     --precise             use adblock plus algorithm instead of O(1) lookup

```

## 规则

[http://codelife.me/blog/2013/04/06/convert-gfwlist-to-pac/](http://codelife.me/blog/2013/04/06/convert-gfwlist-to-pac/)

```
简单说明如下：

 通配符支持，如 *.example.com/* 实际书写时可省略* 如.example.com/ 意即*.example.com/* 
 正则表达式支持，以\开始和结束， 如 \[\w]+:\/\/example.com\
 例外规则 @@，如 @@*.example.com/* 满足@@后规则的地址不使用代理
 匹配地址开始和结尾 |，如 |http://example.com、example.com|分别表示以http://example.com开始和以example.com结束的地址
 || 标记，如 ||example.com 则http://example.com、https://example.com、ftp://example.com等地址均满足条件
 注释 ! 如 ! Comment

```
更详细说明 请访问 [http://adblockplus.org/en/filters](http://adblockplus.org/en/filters)
