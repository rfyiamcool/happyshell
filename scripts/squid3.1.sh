#!/bin/bash 
#优化
echo "setenforce 0" >> /etc/rc.local
setenforce 0
cat >> /etc/sysctl.conf << EOF
net.ipv4.tcp_max_syn_backlog = 65536
net.core.netdev_max_backlog =  32768
net.core.somaxconn = 32768
net.core.wmem_default = 8388608
net.core.rmem_default = 8388608
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216

net.ipv4.tcp_timestamps = 0
net.ipv4.tcp_synack_retries = 2
net.ipv4.tcp_syn_retries = 2

net.ipv4.tcp_tw_recycle = 1
#net.ipv4.tcp_tw_len = 1
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_mem = 94500000 915000000 927000000
net.ipv4.tcp_max_orphans = 3276800
#net.ipv4.tcp_fin_timeout = 30
#net.ipv4.tcp_keepalive_time = 120
net.ipv4.ip_local_port_range = 1024  65535
EOF
sysctl -p

echo -ne "
* soft nofile 65535
* hard nofile 65535
" >>/etc/security/limits.conf

yum install -y ntp
ntpdate -d cn.pool.ntp.org
yum -y install path gcc gcc-c++ autoconf libjpeg libjpeg-devel libpng libpng-devel freetype freetype-devel libxml2 libxml2-devel zlib zlib-devel glibc glibc-devel glib2 glib2-devel bzip2 bzip2-devel ncurses ncurses-devel curl curl-devel e2fsprogs e2fsprogs-devel krb5 krb5-devel libidn libidn-devel openssl openssl-devel openldap openldap-devel nss_ldap openldap-clients openldap-servers

#install squid
#down install 
useradd squid
wget http://www.squid-cache.org/Versions/v3/3.1/squid-3.1.19.tar.gz 
tar zxf squid-3.1.19.tar.gz 
cd squid-3.1.19 
#install  
./configure --prefix=/usr/local/squid \
--enable-debug-cbdata \
--enable-async-io=100 \
--with-pthreads \
--enable-storeio="aufs,diskd,ufs" \
--enable-removal-policies="heap,lru" \
--enable-icmp \
--enable-delay-pools \
--enable-useragent-log \
--enable-referer-log \
--enable-kill-parent-hack \
--enable-arp-acl \
--enable-default-err-language=Simplify_Chinese \
--enable-err-languages="Simplify_Chinese English" \
--disable-poll \
--disable-wccp \
--disable-wccpv2 \
--disable-ident-lookups \
--disable-internal-dns \
--enable-basic-auth-helpers="NCSA" \
--enable-stacktrace \
--with-large-files \
--disable-mempools \
--with-filedescriptors=65535 \
--enable-ssl \
--enable-x-accelerator-var \
--enable-linux-tproxy  \
--enable-linux-netfilter \
--enable-poll
make
make install
cat >> /usr/local/squid/etc/squid.conf << EOF

visible_hostname squid.rui.com
cache_mgr rfyiamcool@163.com
max_filedescriptors 65535
http_port 80 vhost vport
 
cache_mem 512 MB
maximum_object_size 30000 KB
maximum_object_size_in_memory 4096 KB
memory_replacement_policy lru

cache_dir ufs /usr/local/squid/var/cache 1000 16 256
max_open_disk_fds 0
 
cache_swap_low 80
cache_swap_high 95
 
error_directory /usr/local/squid/share/errors/zh-cn
 
logformat squid %ts.%3tu %tr %>a %Ss /%03<Hs %<st %rm %ru %un %Sh/$<A %mt
access_log /usr/local/squid/var/logs/access.log squid
pid_filename /usr/local/squid/var/logs/squid.pid
cache_store_log none
 
cache_peer 192.168.209.128 parent 80 0 no-query originserver round-robin name=web1
cache_peer 192.168.209.254 parent 80 0 no-query originserver round-robin name=web2
cache_peer_domain web1 www.example.com
cache_peer_domain web2 www.example.com
cache_peer_access web1 allow all
cache_peer_access web2 allow all
 

 
cache_effective_user squid
cache_effective_group squid

acl QUERY urlpath_regex .php .jsp .asp .pl .cgi .aspx
acl QUERY urlpath_regex -i cgi-bin \?
acl denyssl urlpath_regex -i ^https:\\
no_cache deny denyssl
cache deny QUERY


ipcache_size 1024
ipcache_low 90
ipcache_high 95
fqdncache_size 1024

http_access allow all

#refresh_pattern ^ftp: 60 20% 10080
#refresh_pattern ^gopher: 60 0% 1440
#refresh_pattern ^gopher: 60 0% 1440
#refresh_pattern . 0 20% 1440
refresh_pattern -i \.css$       360     50%     2880     
refresh_pattern -i \.js$        1440    50%     2880     
refresh_pattern -i \.html$      720     50%     1440     
refresh_pattern -i \.jpg$       1440    90%     2880     
refresh_pattern -i \.gif$       1440    90%     2880     
refresh_pattern -i \.swf$       1440    90%     2880     
refresh_pattern -i \.jpg$       1440    50%     2880     
refresh_pattern -i \.png$       1440    50%     2880     
refresh_pattern -i \.bmp$       1440    50%     2880     
refresh_pattern -i \.doc$       1440    50%     2880      
refresh_pattern -i \.ppt$       1440    50%     2880      
refresh_pattern -i \.xls$       1440    50%     2880      
refresh_pattern -i \.pdf$       1440    50%     2880      
refresh_pattern -i \.rar$       1440    50%     2880      
refresh_pattern -i \.zip$       1440    50%     2880      
refresh_pattern -i \.txt$       1440    50%     2880 

EOF

#配置环境变量
cat >> /etc/profile << EOF
export PATH=$PATH:/usr/local/squid/sbin
EOF
source /etc/profile

#修改权限
chown -R squid:squid /usr/local/squid/var/cache
chown -R squid:squid /usr/local/squid/var/logs

mkdir /usr/local/squid/var/cache
mkdir /usr/local/squid/cache
/usr/local/squid/sbin/squid -z
/usr/local/squid/sbin/squid -s

#轮循日志
echo "0 0 * * * /usr/local/squid/sbin/squid -k rotate" >> /var/spool/cron/root
#生成squid启动脚本
cat >> /etc/init.d/squid <<EOF
#!/bin/bash
#chkconfig: 345 85 15
#description: squid test
#BY liyaoyi 2012-05-04
 
. /etc/rc.d/init.d/functions
squid="/usr/local/squid/sbin/squid"
prog="squid"
RETVAL=0
start() {
        echo -n $"Starting $prog: "
        daemon $squid -s
        RETVAL=$?
        echo
        return $RETVAL
        }
stop () {
        echo -n $"Stoping $prog: "
        daemon $squid -k shutdown
        echo
        return $RETVAL
        }
reload () {
        echo -n $"Reloading $prog: "
        daemon $squid -k reconfigure
        echo
        return $RETVAL
        }
 
case "$1" in
        start)
                start
                ;;
        stop)
                stop
                ;;
        reload)
                reload
                ;;
        restart)
                stop
                start
                ;;
        *) 
        echo $"Usage: $0 {start|stop|restart|reload}"
                RETVAL=1
esac
exit $RETVAL
EOF

chmod a+x /etc/init.d/squid
chkconfig --add squid
chkconfig squid on
/etc/init.d/squid start

echo ""
echo "squid install OK..."
echo ""
