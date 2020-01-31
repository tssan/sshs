import os

import click


VERSION = 'v1.0.0'


DEAFAULT_PORT = 22

HOME_PATH = os.path.expanduser('~')
SSHS_PATH = os.path.join(HOME_PATH, '.sshs')
HOSTS_PATH = os.path.join(SSHS_PATH, 'hosts')
LAST_PATH = os.path.join(SSHS_PATH, 'last')


def load_hosts():
    if not os.path.exists(SSHS_PATH):
        os.makedirs(SSHS_PATH, mode=0x700)
        return []

    hosts = []

    if not os.path.exists(HOSTS_PATH):
        os.system(f'touch {HOSTS_PATH}')

    with open(HOSTS_PATH, 'r') as hosts_file:
        for l in hosts_file:
            hosts.append(l.replace('\n', ''))

    return hosts


def connect(alias, destination, port):
    click.echo(f'connecting to {alias}..')
    os.system(f'ssh {destination} -p {port}')


def validate_alias(s):
    # click.BadParameter('yy?', ctx=None, param='destination')
    pass


def parse(user_input):
    parts = user_input.split(':')

    if len(parts) == 3:
        alias, destination, port = parts
    elif len(parts) == 2:
        destination, port = parts
        alias = None
    elif len(parts) == 1:
        if '@' in parts[0]:
            destination = parts[0]
            alias = None
        else:
            destination = None
            alias = parts[0]
        port = None

    if alias is not None:
        validate_alias(alias)

    return {
        'alias': alias,
        'destination': destination,
        'port': port
    }


def find_in_hosts(h_dict, hosts):
    if h_dict['alias'] is not None:
        for h in hosts:
            parsed_h = parse(h)
            if parsed_h['alias'] == h_dict['alias']:
                return parsed_h

        if h_dict['port'] is None:
            h_dict['port'] = 22

        if h_dict['destination'] is not None:
            os.system(f"echo {h_dict['alias']}:{h_dict['destination']}:{h_dict['port']} >> {HOSTS_PATH}")
            return h_dict

    if h_dict['destination'] is not None:
        h_dict['alias'] = click.prompt(
            f"If you want to save {h_dict['destination']} enter new alias (empty value skips)",
            default='-not-set-',
            show_default=False
        )

        if h_dict['port'] is None:
            h_dict['port'] = 22

        if h_dict['alias'] is '-not-set-':
            return h_dict
        return find_in_hosts(h_dict, hosts)

    return False


@click.command()
@click.option('-ls', is_flag=True, help='List of hosts.')
@click.option('-rm', is_flag=True, help='Remove host.')
@click.argument('destination')
def cli(ls, rm, destination):
    h = parse(destination)
    hosts = load_hosts()
    found = find_in_hosts(h, hosts)

    if found:
        connect(**found)


if __name__ == '__main__':
    cli()
