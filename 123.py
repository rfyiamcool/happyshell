#encoding:utf-8
from flask import Flask, session, redirect, url_for, escape, request
from flask import request
from flask import Flask
from flask import render_template
import re,time
import json
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
UPLOAD_FOLDER = '/file/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','tar.gz','gz'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


'''
http://10.96.60.61:9999/hello/netstat
   %20 空格     55 相当于 -
http://10.96.60.61:9999/hello/netstat%2055nl

netstat -an|grep 80|wc -l
http://10.96.60.61:9999/hello/netstat%2055nl%7Cgrep%2080%7Cwc%2055l

'''
from flask import Flask, session, redirect, url_for, escape, request

app = Flask(__name__)


@app.route('/')
def  index():
     return redirect('index.html')

@app.route('/index.html')
def  index():
     return render_template('index.html')

@app.route('/ssh.html')
def  sshssh():
     return render_template('ssh.html')


@app.route('/file.html')
def  file():
     cmd=os.popen('ls -lh /file').read()
     cmd = '\n%s' % cmd
     return render_template('file.html',cmd=cmd)
    
def  allowed_file(filename):
     return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
        
@app.route('/file', methods=['GET', 'POST'])
def  upload_file():
     if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
           filename = secure_filename(file.filename)
           file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
           return redirect(url_for('uploaded_file',filename=filename))

@app.route('/scp', methods=['GET', 'POST'])
def  scp_file():
     if request.method == 'POST':
        filename=request.form['filename']
        ip = request.form['ip']
        mulu = request.form['mulu']
#       cmd='scp %s root@%s:%s'% (filename,ip,mulu)
        cmd=os.popen('scp'+' '+'/file/'+filename+' '+'root@'+ip+':'+mulu).read()
#       cmd=os.popen('ssh root@'+ipaddr+' '+'ls '+'/'+mulu+'/'+filename).read()

        cmd = '\n%s' % cmd
#       return render_template('file.html',cmd=cmd)
        return redirect('file.html')


@app.route('/login.html')
def  login():
     return render_template('login.html')

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        passwd = request.form['password']
     #if  form.validate_on_submit():
        if  username == 'a' and passwd == '123':
        # login and validate the user...
        #    login_user(username)
        #    flash("Logged in successfully.")
            return "success"

@app.route('/service.html')
def  service():
     return render_template('service.html')

@app.route('/service',methods=['GET','POST'])
def  servicecmd():
     if request.method == 'POST':
        ipaddr=request.form['ip']
        linuxcmd   = request.form['cmd']
        print ipaddr
        print linuxcmd
        if linuxcmd=='nginx':
                cmd='pkill nginx;/usr/local/nginx/sbin/nginx'
        if linuxcmd=='mysql':
                cmd='/etc/init.d/mysql* restart'
        if linuxcmd=='fpm':
                cmd='/etc/init.d/php-fpm restart'
        if linuxcmd=='squid':
                cmd='/etc/init.d/squid restart'
        if linuxcmd=='varnish':
                cmd='/etc/init.d/varnishd restart'
        print cmd
        #执行命令
        os.popen('ssh root@'+ipaddr+' '+'\''+cmd+'\'').read()
        #返回执行后的结果
        info=os.popen('ssh root@'+ipaddr+' '+'\''+'ps aux|grep '+linuxcmd+'\'').read()
#        cmd = '\n 执行的语句 %s \n\n %s' % (cmd,info)
        cmd = '\n 执行的语句 %s' % cmd
        print cmd
#        cmd= ''.join(cmd)
     return render_template('service.html', cmd=cmd,info=info)



@app.route('/linux',methods=['GET','POST'])
def  linux():
     if request.method == 'POST':
        ipaddr=request.form['ip']
        num   = request.form['name']
        print ipaddr
        print num
        print 'ssh root@'+ipaddr+' '+num
#        cmd = os.popen(num).readlines()
        #cmd=os.popen('ssh root@'+ipaddr+' '+num).readlines()
        cmd=os.popen('ssh root@'+ipaddr+' '+num).read()
        cmd = '\n%s' % cmd
        print cmd
#        cmd= ''.join(cmd)
     return render_template('index.html', cmd=cmd)

@app.route('/ssh',methods=['GET','POST'])
def  ssh():
     if request.method == 'POST':
        ipaddr=request.form['ipaddr']
        username  = request.form['username']
        password  = request.form['password']
        cmd  = request.form['cmd']
        print ipaddr
        print username,password
        print 'python ssh.py'+' '+ipaddr+' '+username+' '+password
        cmd=os.popen('python ssh.py'+' '+ipaddr+' '+username+' '+password+' '+cmd).read()
        cmd = '\n%s' % cmd
        return render_template('ssh.html', cmd=cmd)


@app.route('/share.html')
def  kkk():
     return render_template('share.html')

@app.route('/share',methods=['GET','POST'])
def  share():
     if request.method == 'POST':
        ipaddr=request.form['ip']
        mulu   = request.form['mulu']
        info=os.popen('ssh root@'+ipaddr+' '+'\''+'cd '+mulu+';python -m SimpleHTTPServer 7878'+'\'').read()
        cmd = '\n%s' % info
        print cmd
        print ipaddr
     return render_template('share.html', ipaddr=ipaddr)

@app.route('/cdn.html')
def  cdnhtml():
     return  render_template('cdn.html')

@app.route('/vi.html')
def  cdn():
     return  render_template('vi.html')

@app.route('/cdn',methods=['GET','POST'])
def  share():
     if request.method == 'POST':
        ipaddr=request.form['ip']
        cmd=os.popen('scp'+' '+'scripts/squid3.1.sh'+' '+'root@'+ipaddr+':/root').read()
        os.popen('ssh root@'+ipaddr+' '+'\''+'cd root;sh squid3.1.sh && exit'+'\'').read()
#        cmd = '\n%s' % info
        info=os.popen('ssh root@'+ipaddr+' '+'\''+'lsof -i :80|grep squid'+'\'').read()
        if info:
           info ='%s 已经成功的安装了 squid' % ipaddr
        else:
           info ='%s , 我草，没有安装成功~' % ipaddr
     return render_template('cdn.html', info=info)

@app.route('/cdnstatus',methods=['GET','POST'])
def  cndstatus():
     if request.method == 'POST':
         ipaddr=request.form['ip']
         info=os.popen('ssh root@'+ipaddr+' '+'\''+'/usr/local/squid/bin/squidclient -p 80 mgr:info'+'\'').read()
         if info:
             info ='\n 下面是 %s 的Squid 命中率 %s' % (ipaddr,info)
         else:
             info ='%s , 我草，查不到~' % ipaddr
         return render_template('cdn.html', info=info)

@app.route('/cdnqingli',methods=['GET','POST'])
def  cdnqingli():
     if request.method == 'POST':
         ipaddr=request.form['ip']
         name=request.form['name']
         cmd=os.popen('scp'+' '+'scripts/squidqingli.sh'+' '+'root@'+ipaddr+':/root').read()
         os.popen('ssh root@'+ipaddr+' '+'\''+'sh /root/squidqingli.sh '+name+'\'').read()
         info=os.popen('ssh root@'+ipaddr+' '+'\''+'cat cache.txt'+name+'\'').read()

         if info:
             info ='\n 节点  %s \n 清除了以下文件  %s' % (ipaddr,info)
         else:
             info ='%s , 我草，查不到~' % ipaddr
         return render_template('cdn.html', info=info)
#在线编辑文件     
namefile=''
@app.route('/cdnvi',methods=['GET','POST'])
def   cdnvi():
      if request.method == 'POST':
#             ipaddr=request.form['ip']
             name=request.form['name']
             namefile=name
             info=os.popen('cat '+name).read()
             info = '\n%s' %  info
             print namefile
             return render_template('vi.html', info=info)
@app.route('/cdnsave',methods=['GET','POST'])
def   cdnsave():
      if request.method == 'POST':
          print namefile
          name=request.form['name']
          info=name
          info = '\n%s' % info
          print namefile
          info=os.popen('echo '+'\''+name+'\''+'>'+'/root/1').read()
          print namefile
          return render_template('vi.html', info=info)



      



@app.route('/hello/<ccc>')
def hello_world(ccc=None):
    	cmd = ccc.replace('55','-')
	print cmd
	textlist = os.popen(cmd).readlines()
	textlist= '\r\n'.join(textlist)
        return textlist


@app.route('/info/<aaa>')
def info(aaa=None):
    	ipaddr = aaa
        print ipaddr
        cmd='sh net.sh;ifconfig;free -m;vmstat;iostat;df -hT'
	print cmd
	cmd = os.popen('ssh root@'+ipaddr+' '+'\''+cmd+'\'').read()
        cmd = '\n%s' % cmd
        print cmd
#        cmd= ''.join(cmd)
        return render_template('info.html', cmd=cmd)


@app.route('/aaa/<aaa>')
def hello(aaa=None):
     if aaa == 'net':
     	flow1 = open('/proc/net/dev')
     	lines = flow1.read()
     	flow1.close()
     	e =  re.compile('(eth\d)(?:\:)(\d+?)(?:\s+?)(\d+?)(?:\s+?\d+?\s+?\d+?\s+?\d+?\s+?\d+?\s+?\d+?\s+?\d+?\s+?)(\d+?)(?:\s+?)(\d+?)(?:\s)')
     	eth = e.findall(lines)
     	data = json.dumps(eth)
     if aaa == 'aaa':
        data='<h1>aaa </h1>'
     return data

@app.errorhandler(404)
def not_found(error):
    return render_template('index.html'), 404

if __name__ == '__main__':
#     app.run(debug=True)
     app.debug = True
     app.run(host="10.96.60.61",port=9999)
