import subprocess


def _exec_git_command(*args, input=None):
    """exec an git command, return an tuple (stdout|stderr, exitcode)
    :param args: str
    :param input: bytes
    :return: Tuple(str, int)
    """
    git_args = ['git']
    git_args.extend(args)
    print(git_args)
    git = subprocess.Popen(git_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    stdout, stderr = git.communicate(input=input)

    if stderr:
        return stderr, git.returncode

    return stdout, git.returncode


def current_branch():
    """get current branch
    :return: str
    """
    message, code = _exec_git_command('symbolic-ref', '--short', 'HEAD')
    if code == 0:
        return message.strip().decode('utf8')

    print(message)
    return ""


def switch_branch_to(target_branch):
    return _exec_git_command('checkout', target_branch)


def discard_changes():
    return _exec_git_command('checkout', '--', '.')


def pull(*args):
    message, code = _exec_git_command('pull', *args)
    return code == 0


def fetch(*args):
    msg, code = _exec_git_command('fetch', *args)
    if code != 0:
        print(msg)
    return code == 0


def apply(change):
    message, code = _exec_git_command('apply', input=change)
    if code != 0:
        print(message)

    return code == 0


def status(*args):
    message, code = _exec_git_command('status', *args)
    return message


def diff(*args):
    message, code = _exec_git_command('diff', *args)
    return message


def show(*args):
    return _exec_git_command('show', *args)
