import re
import logging
from aiosmtpd import handlers
import asyncio
import time
from xmediusmailrelayserver.forwarddict import ForwardDict

log = logging.getLogger('XMediusMailRelayServer')

class RelayHandler(handlers.Mailbox):
    _patterns = {}

    def __init__(self, mail_dir, retry_interval, retry_timeout, email_sender, loop=None):
        super().__init__(mail_dir)
        self._loop = loop if loop else asyncio.get_event_loop()
        self.retry_interval = retry_interval
        self.retry_timeout = retry_timeout
        self._email_sender = email_sender

    def addPattern(self, pattern, servers):
        self._patterns[re.compile(pattern)] = servers

    def handle_saved_messages(self):
        for id in self.mailbox.keys():
            self._loop.call_soon(self.relay_message, id)
    
    def handle_message(self, message):
        message['X-Message-Received'] = str(time.time())
        id = self.mailbox.add(message)
        self._loop.call_soon(self.relay_message, id)
        
    def relay_message(self, id):
        log.info("Relaying message with id " + id)
        message = self.mailbox.get(id)

        forward_dict = ForwardDict(self._patterns)
        remaining_rcpts = set(message['X-RcptTo'].split(", "))
        for rcpt in remaining_rcpts:
            log.debug("Found recipient '" + rcpt + "'")
            forward_dict.add(rcpt)

        for server, rcpts in forward_dict.get().items():
            recipients = rcpts & remaining_rcpts
            if recipients:
                refused = self._email_sender.send(server, recipients, message)

                accepted = set(recipients) - set(refused)
                remaining_rcpts = remaining_rcpts - accepted

        if remaining_rcpts:
            log.debug("Recipients remaining: " + str(remaining_rcpts))
            message.replace_header('X-RcptTo', ", ".join(remaining_rcpts))

            if message['X-Message-Received'] and float(message['X-Message-Received']) + self.retry_timeout > time.time():
                self.mailbox.__setitem__(id, message)
                log.debug("Will retry in " + str(self.retry_interval) + " seconds")
                self._loop.call_later(self.retry_interval, self.relay_message, id)
            else:
                log.info("Giving up on remaining recipients.")
                self._email_sender.send_ndr(message)
                self.mailbox.discard(id)
        else:
            self.mailbox.discard(id)

