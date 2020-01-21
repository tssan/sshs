import json
import os
import bullet as b

VERSION = 'v1.0.0'

USER_DIR = '.sshs'
HOSTS_FILE = 'hosts.json'

EMPTY_HOSTS_FILE = {
    'aliases': [],
    'hosts': {}
}


class SshSelectUI:
    def __init__(self, hosts_path):
        self.hosts_path = hosts_path
        self.hosts = {}

        with open(hosts_path) as hosts_file:
            self.hosts = json.load(hosts_file)

    def menu(self):
        LAST = 'use last connection'
        LIST = 'list all hosts'
        NEW = 'add new host'

        cli = b.Bullet(
            prompt='What you want to do?',
            choices=[
                LAST,
                LIST,
                NEW
            ]
        )
        result = cli.launch()

        if result == NEW:
            self.add_host()

    def add_host(self):
        cli = b.VerticalPrompt([
            b.Input('Alias: '),
            b.Input('Hostname/IP: ')
        ])
        result = cli.launch()
        alias = result[0][1]
        host = result[1][1]

        if alias in self.hosts['aliases']:
            print('Host already exists')
            return self.add_host()

        self.hosts['aliases'].append(alias)
        self.hosts['hosts'][alias] = host

        with open(hosts_path, 'w') as hosts_file:
            json.dump(self.hosts, hosts_file)


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
