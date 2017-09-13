import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import logging
from logging import handlers
import threading
from xmediusmailrelayserver import server
from xmediusmailrelayserver.server import start_server
from os.path import dirname, join
from os import mkdir, stat
import yaml
import io

def handle_command_line(argv):
    return win32serviceutil.HandleCommandLine(XMRSServiceRunner, None, argv)

class XMRSServiceRunner (win32serviceutil.ServiceFramework):
    _svc_name_ = "xmediusmailrelayserver"
    _svc_display_name_ = "XMedius Mail Relay Server"
    _svc_description_ = "Relays emails to chosen server according to recipient patterns"
    IsStopping = False

    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self._WaitStop = threading.Event()
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.IsStopping = True
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        logger = logging.getLogger("XMediusMailRelayServer")
        logger.info('Service stopped.')

        self._WaitStop.set()

    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_,''))
        self.main()
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)

        self._WaitStop.wait()

    def main(self):
        logger = logging.getLogger('XMediusMailRelayServer')
        localpath = dirname(__file__)
        logfile = join(localpath, 'trace', 'server.log')

        logpath = dirname(logfile)
        try:
            stat(logpath)
        except:
            mkdir(logpath)

        file_hdlr = logging.handlers.RotatingFileHandler(logfile, maxBytes=100*1024*1024, backupCount=10)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_hdlr.setFormatter(formatter)
        logger.addHandler(file_hdlr)

        config = yaml.safe_load(io.open(join(localpath, 'config.yml')))

        if int(config['Debug']) == 1:
            logging.getLogger('').setLevel(logging.DEBUG)
            logging.getLogger('mail.log').addHandler(file_hdlr)
        else:
            logging.getLogger('').setLevel(logging.INFO)

        logger.info('Running in service mode')
        start_server()



