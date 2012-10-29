#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

from __future__ import unicode_literals, absolute_import, division, print_function

from twisted.internet.protocol import Factory, Protocol
from twisted.names import client, server, dns

from twisted.internet.selectreactor import SelectReactor



class DNSecureResolver(client.Resolver):
    def _query(self, *args):
        """
        Get a new L{DNSDatagramProtocol} instance from L{_connectedProtocol},
        issue a query to it using C{*args}, and arrange for it to be
        disconnected from its transport after the query completes.

        @param *args: Positional arguments to be passed to
            L{DNSDatagramProtocol.query}.

        @return: A L{Deferred} which will be called back with the result of the
            query.
        """
        print("args=%s" % (args, ))
        protocol = self._connectedProtocol()
        print(protocol)
        d = protocol.query(*args)
        def cbQueried(result):
            print(result.toStr())
            print(result.opCode)
            result.encode(open("output","w+"))
            #protocol.transport.stopListening()
            return result
        d.addBoth(cbQueried)
        return d

class DNSecureServerFactory(server.DNSServerFactory):
    def __init__(self, *args, **kwargs):
        return server.DNSServerFactory.__init__(self, *args, **kwargs)

    def gotResolverResponse(self, *args, **kwargs):
        return server.DNSServerFactory.gotResolverResponse(self, *args, **kwargs)

class DNSecureSelectReactor(SelectReactor):
    def listenUDP(self, *args, **kwargs):
        return SelectReactor.listenUDP(self, *args, **kwargs)


if __name__ == '__main__':
    reactor = DNSecureSelectReactor()
    verbosity = 0
    resolver = DNSecureResolver(servers=[('61.177.7.1', 53)], reactor=reactor)
    f = DNSecureServerFactory(clients=[resolver], verbose=verbosity)

    p = dns.DNSDatagramProtocol(f)
    f.noisy = p.noisy = verbosity

    reactor.listenUDP(53, p)
    reactor.listenTCP(53, f)
    reactor.run()
