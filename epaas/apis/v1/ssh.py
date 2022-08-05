from pexpect import pxssh
from flask import _app_ctx_stack
from flask import jsonify, request, current_app, g
from flask.views import MethodView
from epaas.apis.v1 import api_v1
from epaas.apis.v1.auth import auth_required, decrypt
import paramiko
from flask import current_app
from flask_sock import Sock
import time
from epaas.models import User, Server
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired


class SSH:
    def __init__(self, ip, user, password):
        self.ssh = None
        self.ip = ip
        self.user = user
        self.password = password

    def connect(self):
        self.ssh = pxssh.pxssh()
        try:
            self.ssh.login(self.ip, self.user, self.password)
            return True
        except Exception as e:
            import sys
            print(sys.exc_info())
            return False

    def get_ssh(self):
        top = _app_ctx_stack.top
        if not hasattr(top, 'ssh_conn'):
            top.ssh_conn = self.connect(self.ip, self.user, self.password)
        return top.ssh_conn

    def execute(self, command):
        CR = '\r\n'
        self.ssh.sendline(command)  # 执行命令
        self.ssh.prompt()  # 匹配command执行后的下一步操作的命令提示符
        # self.ssh.before 指的是两个命令提示符之间的内容
        data = self.ssh.before.split(CR.encode('utf-8'))[1:-1]
        for each in data:
            return(each.decode('utf-8'))


class SshAPI(MethodView):

    @auth_required
    def get(self):
        print(g.current_user.username)
        ip = request.args.get('ip', '', type=str)
        user = request.args.get('ip', '', type=str)
        password = request.args.get('ip', '', type=str)
        ssh = SSH(ip, user, password)
        cmdline = request.args.get('cmd', '', type=str)
        if ssh.connect():
            self.response = ssh.execute(cmdline)
            return jsonify(self.response)
        else:
            return None


class SSH_PARA(object):

    def __init__(self, host, port, user, password=None, keyfile=None, passphrase=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.keyfile = keyfile
        self._ssh = paramiko.SSHClient()
        self._ssh.load_system_host_keys()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if self.password:
            self._ssh.connect(host, port, user, password)
        elif self.keyfile:
            k = paramiko.RSAKey.from_private_key_file(keyfile)
            self._ssh.connect(hostname=host, port=port,
                              username=user, pkey=k)
        # 打开ssh通道，建立长连接
        # transport = self._ssh.get_transport()
        # self._chanel = transport.open_session()
        self._chanel = self._ssh.invoke_shell(term='xterm')
        # self._chanel.setblocking(0)
        # self._chanel.resize_pty(width=50, height=70)

    def resize(self, cols, rows):
        current_app.logger.info("重置窗口大小:{},{}".format(cols, rows))
        self._chanel.resize_pty(width=cols, height=rows)

    def send(self, msg):
        self._chanel.send(msg)

    def read(self):
        return self._chanel.recv(10000).decode('utf-8')

    def read_ready(self):
        return self._chanel.recv_ready()

    @staticmethod
    def get_permission(token, host):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except (BadSignature, SignatureExpired):
            return False
        user = User.query.get(data['id'])
        server = Server.query.filter_by(ip=host).first()
        if user is None or server is None:
            return False
        # compare role between user and server
        for user_role in user.roles.split(','):
            for server_role in server.roles.split(','):
                if user_role == server_role:
                    return server
        return False

api_v1.add_url_rule('/server/cmdline', view_func=SshAPI.as_view('cmdline'), methods=['GET'])
sockets = Sock()
sockets.init_app(api_v1)


@sockets.route('/server/socket/<string:token>/<string:ip>')
def echo(sockets, token, ip):
    server = SSH_PARA.get_permission(token, ip)
    if not server:
        sockets.send("you have no access permission")
        return False
    ssh = SSH_PARA(host=server.ip, port=22, user=server.ssh_user, password=decrypt(server.password))
    for i in range(2):
      recv = ssh.read()
      print(recv)
      sockets.send(recv)
    while True:
        message = sockets.receive()
        if message is not None:
            # ssh.send(bytes(message, encoding='utf-8'))
            ssh.send(message)
            while not ssh.read_ready():
                time.sleep(0.02)
            recv = ssh.read()
            sockets.send(recv)
