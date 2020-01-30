import argparse
import json
import os
import bullet as b

VERSION = 'v1.0.0'

USER_DIR = '.sshs'
HOSTS_FILE = 'hosts.json'
LAST_FILE = 'last'

EMPTY_HOSTS_FILE = {
    'aliases': [],
    'hosts': {},
    'users': {},
    'ports': {}
}

DEAFAULT_PORT = 22


class SshSelectUI:
    def __init__(self, user_path):
        self.hosts_path = os.path.join(user_path, HOSTS_FILE)
        self.last_path = os.path.join(user_path, LAST_FILE)
        self.hosts = {}

        with open(self.hosts_path) as hosts_file:
            self.hosts = json.load(hosts_file)

    @property
    def last_alias(self):
        if os.path.exists(self.last_path):
            return open(self.last_path, 'r').read()
        print('Connection not found.')

    def update(self):
        with open(self.hosts_path, 'w') as hosts_file:
            json.dump(self.hosts, hosts_file)

    def connect(self, alias):
        if alias not in self.hosts['aliases']:
            print(f'Host {alias} not found.')
            return

        user = self.hosts['users'][alias]
        host = self.hosts['hosts'][alias]
        port = self.hosts['ports'][alias]

        with open(self.last_path, 'w') as f:
            f.write(alias)

        print(f'ssh {user}@{host} -p {port}')
        os.system(f'ssh {user}@{host} -p {port}')

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

        if result == LAST and self.last_alias:
            self.connect(self.last_alias)
        elif result == NEW:
            self.add_host()
        elif result == LIST:
            self.show_list()
        elif result == EXIT:
            return

    def add_host(self):
        user = os.getlogin()

        cli = b.VerticalPrompt([
            b.Input('Alias: '),
            b.Input('Hostname/IP:PORT (default port:22) eg.: 192.168.1.1:3001 or mydomain.com '),
            b.Input(f'Username (default:{user}): ', pattern=r'.*')
        ])
        result = cli.launch()
        alias = result[0][1]
        host_n_port = result[1][1].split(':')
        host = host_n_port[0]
        if len(host_n_port) > 1:
            port = host_n_port[1]
        else:
            port = DEAFAULT_PORT
        username = result[2][1]

        if username == '':
            username = user

        if alias in self.hosts['aliases']:
            print('Host already exists')
            return self.add_host()

        self.hosts['aliases'].append(alias)
        self.hosts['hosts'][alias] = host
        self.hosts['ports'][alias] = port
        self.hosts['users'][alias] = username

        self.update()
        return self.menu()

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
            self.connect(alias)
        elif result == DEL_HOST:
            self.hosts['aliases'].remove(alias)
            del self.hosts['hosts'][alias]
            del self.hosts['users'][alias]
            self.update()
            return self.show_list()
        elif result == BACK:
            return self.menu()


def main():
    parser = argparse.ArgumentParser(
        description=f'SSH Select {VERSION}')
    parser.add_argument('host', type=str, nargs='?')
    args = parser.parse_args()

    home_path = os.path.expanduser('~')
    user_path = os.path.join(home_path, USER_DIR)

    if not os.path.exists(user_path):
        os.makedirs(user_path, mode=0o700)
        print(f'Initial setup:\n creating folder: {user_path}')

    hosts_path = os.path.join(user_path, HOSTS_FILE)
    if not os.path.exists(hosts_path):
        with open(hosts_path, 'w') as hosts_file:
            json.dump(EMPTY_HOSTS_FILE, hosts_file)
        print(f'All your hosts will be stored here: {hosts_path}')

    ui = SshSelectUI(user_path)

    if args.host:
        ui.connect(args.host)
    else:
        ui.menu()


if __name__ == '__main__':
    main()
