import smtplib
from email import message
import logging

log = logging.getLogger('XMediusMailRelayServer')

class EmailSender:

    def __init__(self, default_server, from_address):
        self._default_server = default_server
        self._from_address = from_address
        self._smtp = smtplib.SMTP()


    def send(self, server, recipients, message):
        log.info("Sending to " + str(len(recipients)) + " recipients using server '" + server + "'")
        try:
            self._smtp.connect(server)
        except Exception as e:
            log.error("Error connecting to server")
            log.exception(e)
            return recipients

        try:
            refused = self._smtp.send_message(message, to_addrs=recipients)
        except (OSError, smtplib.SMTPException) as e:
            log.error("Error sending to server")
            log.exception(e)
            return recipients
        finally:
            self._smtp.quit()

        if refused:
            log.info("Recipients refused: " + str(refused))

        return refused

    def send_ndr(self, failed_message):
        m = message.Message()
        m.set_type("multipart/report")
        m.set_param('report-type', 'delivery-status')
        m.add_header('Subject', 'Returned mail: delivery failure')

        p1 = message.Message()
        p1.add_header('content-type', 'text/plain; charset=us-ascii')
        text = "Original message subject: " + failed_message['Subject'] + "\n\n"
        text += "The following addresses had delivery problems:\n"
        for recipient in failed_message['X-RcptTo'].split(", "):
            text += recipient
            text += "\n"

        p1.set_payload(text)
        
        p2 = message.Message()
        p2.add_header('content-type', 'message/delivery-status')
        s1 = message.Message()
        s1.add_header('Reporting-MTA', 'test.nic.lan')
        p2.attach(s1)

        for recipient in failed_message['X-RcptTo'].split(", "):
            s2 = message.Message()
            s2.add_header('Original-Recipient', recipient)
            s2.add_header('Final-Recipient', recipient)
            s2.add_header('Action', 'failed')
            s2.add_header('Status', '5.0.0 (permanent failure)')
            p2.attach(s2)

        m.attach(p1)
        m.attach(p2)

        log.info("Sending NDR using server " + self._default_server)

        try:
            self._smtp.connect(self._default_server)
        except Exception as e:
            log.error("Error connecting to server")
            log.exception(e)
            return

        try:
            self._smtp.send_message(m, to_addrs=failed_message.get('X-MailFrom'), from_addr=self._from_address)
        except (OSError, smtplib.SMTPException) as e:
            log.error("Error sending to server")
            log.exception(e)
        finally:
            self._smtp.quit()


