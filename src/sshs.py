import json
import os
import bullet as b

VERSION = 'v1.0.0'

USER_DIR = '.sshs'
HOSTS_FILE = 'hosts.json'

EMPTY_HOSTS_FILE = {
    'aliases': [],
    'hosts': {},
    'users': {}
}


class SshSelectUI:
    def __init__(self, hosts_path):
        self.hosts_path = hosts_path
        self.hosts = {}

        with open(hosts_path) as hosts_file:
            self.hosts = json.load(hosts_file)

    def update(self):
        with open(self.hosts_path, 'w') as hosts_file:
            json.dump(self.hosts, hosts_file)

    def menu(self):
        LAST = 'use last connection'
        LIST = 'list all hosts'
        NEW = 'add new host'
        EXIT = 'exit'

        cli = b.Bullet(
            prompt='*',
            choices=[
                LAST,
                LIST,
                NEW,
                EXIT
            ]
        )
        result = cli.launch()

        if result == NEW:
            self.add_host()
        elif result == LIST:
            self.show_list()
        elif result == EXIT:
            return

    def add_host(self):
        user = os.getlogin()

        cli = b.VerticalPrompt([
            b.Input('Alias: '),
            b.Input('Hostname/IP: '),
            b.Input(f'Username (default:{user}): ', pattern=r'.*')
        ])
        result = cli.launch()
        alias = result[0][1]
        host = result[1][1]
        username = result[2][1]

        if username == '':
            username = user

        if alias in self.hosts['aliases']:
            print('Host already exists')
            return self.add_host()

        self.hosts['aliases'].append(alias)
        self.hosts['hosts'][alias] = host
        self.hosts['users'][alias] = username

        self.update()

    def show_list(self):
        if len(self.hosts['aliases']) == 0:
            print('Hosts list is empty.')
            return self.menu()

        cli = b.Bullet(
            prompt='Available hosts:',
            choices=self.hosts['aliases']
        )
        alias = cli.launch()

        CON_HOST = 'connect'
        DEL_HOST = 'delete host'
        BACK = 'back'
        host_cli = b.Bullet(
            prompt=f'Host {alias} options:',
            choices=[CON_HOST, DEL_HOST, BACK]
        )
        result = host_cli.launch()

        if result == CON_HOST:
            user = self.hosts['users'][alias]
            host = self.hosts['hosts'][alias]
            os.system(f'ssh {user}@{host}')
        elif result == DEL_HOST:
            self.hosts['aliases'].remove(alias)
            del self.hosts['hosts'][alias]
            del self.hosts['users'][alias]
            self.update()
            return self.show_list()
        elif result == BACK:
            return self.menu()


if __name__ == '__main__':
    # print(f'SSH Select {VERSION}')

    home_path = os.path.expanduser('~')
    print(home_path, USER_DIR)
    user_path = os.path.join(home_path, USER_DIR)

    if not os.path.exists(user_path):
        os.makedirs(user_path, mode=0o700)
        print(f'Initial setup:\n creating folder: {user_path}')

    hosts_path = os.path.join(user_path, HOSTS_FILE)
    if not os.path.exists(hosts_path):
        with open(hosts_path, 'w') as hosts_file:
            json.dump(EMPTY_HOSTS_FILE, hosts_file)
        print(f'All your hosts will be stored here: {hosts_path}')

    SshSelectUI(hosts_path).menu()
