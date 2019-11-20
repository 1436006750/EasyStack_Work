# Copyright (c) 2018 SLIC personal studio.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import threading

import paste.deploy

if __name__ == "__main__":
    # TODO(neil): We should change to another way
    # import sys
    # reload(sys)
    # sys.setdefaultencoding('utf8')
    import argparse
    import socket
    import sys
    import wsgiref.simple_server as wss

    my_ip = socket.gethostbyname(socket.gethostname())
    parser = argparse.ArgumentParser(
        description='welcome to diveintoslic lessons.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        usage='%(prog)s [-h] [--port PORT] -- [passed options]')
    parser.add_argument('--port', '-p', type=int, default=5354,
                        help='TCP port to listen on')
    parser.add_argument('args',
                        nargs=argparse.REMAINDER,
                        metavar='-- [passed options]',
                        help="'--' is the separator of the arguments used "
                        "to start the WSGI server and the arguments passed "
                        "to the WSGI application.")
    args = parser.parse_args()
    if args.args:
        if args.args[0] == '--':
            args.args.pop(0)
        else:
            parser.error("unrecognized arguments: %s" % ' '.join(args.args))
    sys.argv[1:] = args.args
    server = wss.make_server('', args.port, paste.deploy.loadapp(
        'config:/root/zx/0.0_Internship_Work/diveintoslic/etc/paste.ini',
        name='main'))

    print("*" * 80)
    url = "http://%s:%d/" % (my_ip, server.server_port)
    print("Available at %s" % url)
    print("DANGER! For testing only, do not use in production")
    print("*" * 80)
    sys.stdout.flush()

    server.serve_forever()
else:
    application = None
    app_lock = threading.Lock()

    with app_lock:
        if application is None:
            application = paste.deploy.loadapp(
                'config:/root/zx/0.0_Internship_Work/diveintoslic/etc/paste.ini'
                'paste.ini',
                name='main')
