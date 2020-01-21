import os
# import bullet as b

VERSION = 'v1.0.0'

USER_DIR = '.sshs'


class SshSelectUI:
    def __init__(self):
        print(f'SSH Select {VERSION}')
        pass

    # def menu(sell):
    #     cli = b.

    # def choose_host(self):
    #     cli = b.Bullet(
    #         prompt="Select host:",
    #         choices=self.hosts
    #     )
    #     result = cli.launch()
    #     if self.use_ip:
    #         return [self.get_ip(result)]
    #     return [result]

    # def choose_group(self):
    #     cli = b.Bullet(
    #         prompt="Select group:",
    #         choices=self.groups
    #     )
    #     group = cli.launch()
    #     result = []

    #     for host in self._data[group]:
    #         if self.use_ip:
    #             result.append(self.get_ip(host))
    #         else:
    #             result.append(host)
    #     return result

    # def choose_env(self):
    #     cli = b.Bullet(
    #         prompt="Select env:",
    #         choices=self.envs
    #     )
    #     env = cli.launch()
    #     result = []

    #     for host in self._data['envs'][env]:
    #         if self.use_ip:
    #             result.append(self.get_ip(host))
    #         else:
    #             result.append(host)
    #     return result

    # def choose_where(self):
    #     ip_cli = b.YesNo('Hosts by IP?')
    #     self.use_ip = ip_cli.launch()

    #     H = 'host'
    #     G = 'group'
    #     E = 'env'
    #     cli = b.Bullet(
    #         prompt="Deploy by:",
    #         choices=[H, G, E]
    #     )
    #     result = cli.launch()
    #     if result == H:
    #         return self.choose_host()
    #     elif result == G:
    #         return self.choose_group()
    #     elif result == E:
    #         return self.choose_env()


if __name__ == '__main__':
    ui = SshSelectUI()
    home_path = os.path.expanduser('~')
    print(home_path, USER_DIR)
    user_path = os.path.join(home_path, USER_DIR)

    if not os.path.exists(user_path):
        os.makedirs(user_path, mode=0o700)
        print(f'Initial setup:\n creating folder: {user_path}')

    print(os.listdir(user_path))
