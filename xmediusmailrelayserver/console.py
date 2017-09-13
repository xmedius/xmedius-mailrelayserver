import sys
import logging
from os.path import dirname
from xmediusmailrelayserver import server

def install_service(argv):
    new_argv = [dirname(__file__)]
    for arg in argv:
        new_argv.append(arg)
    from xmediusmailrelayserver.servicehelpers import handle_command_line
    handle_command_line(new_argv)

def main():
    stdout_handler = logging.StreamHandler(sys.stdout)
    logging.getLogger('').setLevel(logging.INFO)
    logging.getLogger('mail.log').addHandler(stdout_handler)
    logging.getLogger('XMediusMailRelayServer').addHandler(stdout_handler)

    server.start_server()

if __name__ == "__main__":
    main()
    input("Press Enter to quit")

