import configparser
import asyncio
from aiosmtpd.controller import Controller
from aiosmtpd.handlers import Proxy
import logging
import aiosmtpd
from xmediusmailrelayserver.relayhandler import RelayHandler
from xmediusmailrelayserver.emailsender import EmailSender
from os.path import dirname, join
import yaml
import io

def start_server():
    log = logging.getLogger('XMediusMailRelayServer')
    loop = asyncio.get_event_loop()

    localpath = dirname(__file__)

    config = yaml.safe_load(io.open(join(localpath, 'config.yml')))
    hostname = config['Hostname']
    port = config['Port']
    default_server = config['DefaultRelayServer']
    from_address = config['FromAddress']

    retry_interval = config['MailRetryInterval']
    retry_timeout = config['MailRetryTimeout']

    email_sender = EmailSender(default_server, from_address)
    handler = RelayHandler(join(localpath, 'mail'), retry_interval, retry_timeout, email_sender, loop)

    for pattern_config in config['Patterns']:
        pattern = pattern_config
        servers = config['Patterns'][pattern]
        log.info("Added pattern '" + pattern + "' pointing to servers " + str(servers))
        handler.addPattern(pattern, servers)

    handler.handle_saved_messages()

    log.info("Listening on " + hostname + ":" + str(port))

    controller = Controller(handler, hostname=hostname, port=port, loop=loop)
    controller.start()

