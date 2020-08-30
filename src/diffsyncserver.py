import os

import git
from flask import request, Response, Blueprint, Flask, logging
from urllib import parse


app = Flask("Git diff sync server")

api = Blueprint("git", "api", url_prefix='/git')
admin = Blueprint('admin', 'api', url_prefix='/admin')

logger = logging.create_logger(app)


@admin.route('/chdir', methods=['GET'])
def admin_chdir():
    dir = request.args.get('dir')
    dir = parse.unquote(dir)
    if dir and os.path.isdir(dir):
        os.chdir(dir)
        logger.info("chdir from '%s' to '%s'" % (os.getcwd(), dir))
        return Response(status=200)
    else:
        return Response(status=400)


@admin.route('/chdir/current', methods=['GET'])
def admin_get_chdir():
    return os.getcwd()


@api.route('/status', methods=['GET'])
def api_status():
    return git.status()


@api.route("/apply", methods=['POST'])
def api_apply():
    if request.headers.get('content-type') != 'text/plain':
        return Response(status=400)
    logger.info("apply change to '%s'" % (os.getcwd()))
    git.discard_changes()
    logger.info("discard changes done.")
    if git.apply(request.data):
        logger.info("apply changes done.")
        return "ok"
    return "fail"


@api.route('/diff')
def diff():
    return git.diff()


@api.route('/diff/stat')
def diff_stat():
    return git.diff('--stat')


@api.route('/show')
def show():
    result, code = git.show()
    return result


@api.route('/switch/<string:branch>')
def switch(branch):
    message, code = git.switch_branch_to(branch)

    return message


@api.route('/discard/changes')
def discard():
    message, code = git.discard_changes()

    return message


app.register_blueprint(api)
app.register_blueprint(admin)


def main():
    if 'GIT_WORKING_DIRECTORY' in os.environ:
        if os.path.isdir(os.environ.get('GIT_WORKING_DIRECTORY')):
            os.chdir(os.environ.get('GIT_WORKING_DIRECTORY'))
        else:
            raise Exception("No such directory: '%s'" % os.environ.get('GIT_WORKING_DIRECTORY'))

    app.run(port=5000)


if __name__ == '__main__':
    main()
