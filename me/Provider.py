class Provider:
    def __init__(self, displayName, domain):
        self.displayName = displayName
        self.domain = domain
        self.services = []

    def setService(self, service):
        self.services.append(service)

    def getServices(self):
        return self.services

    def getDomain(self):
        return self.domain


class Service:
    def __init__(self, type, host, port, smtp_host, smtp_port):
        self.type = type
        self.host = host
        self.port = port
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port

    def getType(self):
        return self.type

    def getHost(self):
        return self.host

    def getPort(self):
        return self.port
