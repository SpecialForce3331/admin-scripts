import sys

IS_DEBUG = True

if IS_DEBUG:
    vip_users_file = '/tmp/vip_users.acl'
    deny_users_file = '/tmp/deny_users.acl'
    deny_sites_file = '/tmp/deny_regex_dstdomain.acl'
else:
    vip_users_file = '/etc/squid/vip_users.acl'
    deny_users_file = '/etc/squid/deny_users.acl'
    deny_sites_file = '/etc/squid/deny_regex_dstdomain.acl'


def help_text():
    return '-----------------------------------------------------------------------------\n' \
           'You can use on of commands:\n' \
           'vip "username or ip" - for add vip user\n' \
           'unvip "username or ip" - for remove user from vip list\n' \
           'block {user or site} "username or ip or url" - for block user or some url\n' \
           'unblock {user or site} "username or ip or url" - for unblock user or some url\n' \
           '-----------------------------------------------------------------------------'


def is_data_exists_in_file(filename, data):
    try:
        with open(filename, encoding='utf-8') as f:
            for line in f:
                if line.strip() == data:
                    return True
            return False
    except FileNotFoundError:
        print('File {} is incorrect! Please contact to sys.admin!'.format(filename))


def write_to_file(filename, data):
    try:
        with open(filename, 'a') as f:
            f.write(data + '\n')
        print('Success!')
    except FileNotFoundError:
        print('File {} is incorrect! Please contact to sys.admin!'.format(filename))


def remove_from_file(filename, data):
    try:
        with open(filename, encoding='utf-8') as f:
            file_content = f.readlines()
        with open(filename, 'w', encoding='utf-8') as f:
            for line in file_content:
                if line.strip() == data:
                    continue
                f.write(line)
        print('Success!')

    except FileNotFoundError:
        print('File {} is incorrect! Please contact to sys.admin!'.format(filename))


def add_vip(user):
    if is_data_exists_in_file(vip_users_file, user):
        print('User already exists in file ', vip_users_file)
    else:
        write_to_file(vip_users_file, user)


def remove_vip(user):
    if is_data_exists_in_file(vip_users_file, user):
        remove_from_file(vip_users_file, user)
    else:
        print('User not exists in file', vip_users_file)


def add_deny_site(url):
    if is_data_exists_in_file(deny_sites_file, url):
        print('Site already exists in file ', deny_sites_file)
    else:
        write_to_file(deny_sites_file, url)


def block_user(user):
    if is_data_exists_in_file(vip_users_file, user):
        write_to_file(deny_users_file, user)
    else:
        print('User not exists in file', deny_users_file)


actions = {
    'vip': add_vip,
    'unvip': remove_vip,
    'block': {
        'user': block_user,
        'site': add_deny_site
    }
}

try:
    commands = sys.argv[1:]
except IndexError:
    print(help_text())

if commands and len(commands) > 1:
    current_func = None

    for cmd in commands:
        if cmd == commands[-1]:
            try:
                current_func(cmd)
            except TypeError:
                print(help_text())
        elif current_func and current_func.get(cmd):
            current_func = current_func.get(cmd)
        elif actions.get(cmd):
            current_func = actions[cmd]
        else:
            print(help_text())
else:
    print(help_text())
