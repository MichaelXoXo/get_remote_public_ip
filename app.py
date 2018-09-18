import os
import subprocess

import paramiko
from apistar import App, Route, types, validators
from apistar.server.wsgi import WSGIEnviron


class RebootParams(types.Type):
    """
    https://discuss.apistar.org/t/how-to-describe-parameter-in-api-call/501/5
    """
    # content = validators.String(max_length=1024 * 1024 * 10, description='Text content to tag')
    # offset = validators.Integer(minimum=0, allow_null=True, description='Paging offset')
    # limit = validators.Integer(minimum=1, allow_null=True, description='Paging limit')
    ip = validators.String(description="输入待重启机器的IP")


def welcome(name=None):
    if name is None:
        return {'message': 'Welcome to Michae'}
    return {'message': 'Welcome to Michael Home, {}'.format(name)}


def get_ip(environ: WSGIEnviron):
    return {"ip_addr": environ["REMOTE_ADDR"]}


def reboot(ip):
    """
    ip: 要重启机器的ip

    # https://github.com/onyxfish/relay/issues/11
    # https://stackoverflow.com/questions/3586106/perform-commands-over-ssh-with-python
    # https://codereview.stackexchange.com/questions/171179/python-script-to-execute-a-command-using-paramiko-ssh
    """
    cmd_str = "mkdir -p /tmp/michaeltest"
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(ip, username='root', password="xxx")
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd_str)
    print(type(ssh_stdin))
    print(ssh_stdout.read().decode())
    print(ssh_stderr.read().decode())
    status = 'success' if not ssh_stderr.read().decode() else 'failure'
    ssh.close()
    return {'ip': ip,
            'cmd': cmd_str,
            'status': status
            }


routes = [
    Route('/', method='Get', handler=welcome),
    Route('/ip', method='Get', handler=get_ip),
    Route('/machine/{ip}', method='Get', handler=reboot)
]

app = App(routes=routes)
if __name__ == '__main__':
    app.serve('0.0.0.0', 5000, debug=True)
