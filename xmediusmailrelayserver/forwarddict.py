from collections import defaultdict
import logging

log = logging.getLogger('XMediusMailRelayServer')

class ForwardDict:

    def __init__(self, patterns):
        self._patterns = patterns
        self._dict = defaultdict(set)
        
    def add(self, recipient):
        for pattern, servers in self._patterns.items():
            if pattern.match(recipient):
                log.debug("Matched pattern for servers " + str(servers))
                for server in servers:
                    self._dict[server].add(recipient)
                break

    def get(self):
        return self._dict


