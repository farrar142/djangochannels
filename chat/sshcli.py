# Create your tests here.
from pprint import pprint
# from mysite.functions import auto_login
import paramiko
import time
import re
import asyncio


def ansi_decoder(context) -> str:
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', context)


class CliInterface:
    informs = {}

    def get_or_connect(self, params: dict):
        user = 'test'
        try:
            informs = CliInterface.informs.get(user)
            self = informs.get("self")
            self.cli = informs.get("cli")
            self.target = informs.get("target")
        except:
            hostname = params.get("hostname")
            username = params.get("username")
            password = params.get("password")
            self.cli = paramiko.SSHClient()
            self.cli.load_system_host_keys
            self.cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.cli.connect(**params)  # 여기까지 해줘야 invokeshell이열림
            self.target = self.cli.invoke_shell()
            self.target.settimeout(3)
            informs = {
                user: {
                    "self": self,
                    "cli": self.cli,
                    "target": self.target,
                    "params": params
                }
            }
            CliInterface.informs.update(informs)

    def close(self):
        self.target.close()

    def connect(self, info: dict):
        self.cli.connect(**info)

    def run(self):
        while True:
            cmd = input("입력) ")
            if cmd == "exit":
                return
            self.send(cmd)
            self.receive(True)

    def single_order(self, cmd):
        self.send(cmd)
        return self.receive(True)

    def send(self, cmd):
        self.target.send(cmd+"\n")

    def receive(self, bool=True):
        time.sleep(0.02)  # 기본대기시간
        while True:
            if self.target.recv_ready():
                time.sleep(0.02)  # 기본대기시간
                break
            else:
                time.sleep(0.5)
        result = self.target.recv(64435).decode('utf-8')
        result = ansi_decoder(result)
        if bool:
            print(result)
        return result
    #커스텀 로직들#

    def ls_al(self, *args):
        context = self.custom_order("ls -al")
        result = []
        for i in context:
            cur = i.split(" ")  # 나누기
            cur = ' '.join(cur).split()  # 공백지우기
            if len(cur) == 9:
                if cur[0].startswith('-'):
                    result.append(["file", cur[-1]])
                elif cur[0].startswith('d'):
                    result.append(["dir", cur[-1]])

        [print(i) for i in result]
        return result

    def cd(self, path):
        self.send("cd "+path)
        # self.receive()

    #커스텀 로직 끝#
    def custom_order(self, cmd):
        self.send(cmd)
        context = self.receive(False)
        context = context.splitlines()
        return context

    def custom_cmd(self, cmd, *args):
        return getattr(self, cmd)(*args)

    def show(self):
        pprint(CliInterface.informs)

    @classmethod
    def from_api(cls, hostname, username, password, directory, cmd=""):
        setting = {
            "hostname": hostname,
            "username": username,
            "password": password,
        }
        test = CliInterface()
        test.get_or_connect(setting)
        test.receive()
        test.custom_cmd("cd", directory)
        files = test.custom_cmd("ls_al")
        result = test.single_order(cmd)
        test.close()
        return {files: files, result: result}


# async def main():
#     setting = {
#         "hostname": "49.50.174.121",
#         "username": "root",
#         "password": "eowjsrhkddurtlehdrneowjsfh304qjsrlf28"
#     }
#     # test = CliInterface()
#     # test.get_or_connect(setting)
#     # test.receive()
#     # # test.run()
#     # test.custom_cmd("cd", "/home/test")
#     # test.custom_cmd("ls_al")
#     CliInterface().from_api("49.50.174.121", "root",
#                             "eowjsrhkddurtlehdrneowjsfh304qjsrlf28", "/home/test")
# asyncio.run(main())
