import os
import bullet as b

VERSION = 'v1.0.0'

USER_DIR = '.sshs'


class SshSelectUI:
    def __init__(self, user_path):
        pass

    def menu(sell):
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
        print(result)


if __name__ == '__main__':
    # print(f'SSH Select {VERSION}')

    home_path = os.path.expanduser('~')
    print(home_path, USER_DIR)
    user_path = os.path.join(home_path, USER_DIR)

    if not os.path.exists(user_path):
        os.makedirs(user_path, mode=0o700)
        print(f'Initial setup:\n creating folder: {user_path}')
        print('All your hosts will be stored there.')

    SshSelectUI(user_path).menu()
