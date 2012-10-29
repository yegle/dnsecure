#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

from __future__ import unicode_literals, absolute_import, division, print_function

from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
from twisted.names import client, server, dns


class DNSecureResolver(client.Resolver):
    pass


if __name__ == '__main__':
    verbosity = 0
    resolver = DNSecureResolver(servers=[('4.2.2.2', 53)])
    f = server.DNSServerFactory(clients=[resolver], verbose=verbosity)
    p = dns.DNSDatagramProtocol(f)
    f.noisy = p.noisy = verbosity

    reactor.listenUDP(53, p)
    reactor.listenTCP(53, f)
    reactor.run()
