#!/usr/bin/python
import logging
import os
import traceback
from xml.etree import ElementTree

logger = logging.getLogger(__name__)

currentPath = os.path.dirname(os.path.abspath(__file__))


def getProviderFromFilenames():
    path = os.path.join(currentPath, 'xml')
    logger.info("Getting provider from '%s'" % path)
    provs = os.listdir(path)
    logger.debug(provs)
    return provs


class ProviderXMLHandler:
    fullFilePath = None
    domain = None
    dom = None
    services = []

    def __init__(self, xmlfile):
        self.fullFilePath = os.path.join(currentPath, os.path.join('xml', xmlfile))
        logger.debug("Getting " + self.fullFilePath)
        try:
            self.dom = ElementTree.parse(self.fullFilePath)
        except Exception as e:
            logger.debug(xmlfile)
            logger.error(traceback.format_exc())
            logger.info('Maybe try to fix with --update')
            raise e

        self.domain = xmlfile
        if not self.dom:
            logger.info("File loaded: " + str(self.dom))

        self.getDisplayName()
        self.get_incoming_servers()
        # self.getDomains()

    def getDomain(self):
        return self.domain

    def get_incoming_servers(self):
        server = []
        incoming_servers = self.dom.findall('emailProvider/incomingServer')
        logger.debug("incoming servers " + str(len(incoming_servers)))
        for s in incoming_servers:
            type = s.attrib['type']

            if type not in self.services:
                self.services.append(type)

            logger.debug("Hostname: " + str(s.find('hostname').text))
            logger.debug("Hostname: " + str(s.find('port').text))

            service = []
            service.append(type)
            service.append(s.find('hostname').text)
            service.append(int(s.find('port').text))

            if service not in server:
                server.append(service)

        return server

    def canProviderIMAP(self):
        if "imap" in self.services:
            return True
        return False

    def canProviderPOP3(self):
        if "pop3" in self.services:
            return True
        return False

    def getDisplayName(self):
        displayName = self.dom.findall('emailProvider/displayName')
        if len(displayName) > 0:
            displayName = displayName[0].text
            logger.debug("Display name: " + displayName)
            return displayName.encode('utf8')
        else:
            logger.debug("Display name: none")
        return "None";

    def getDomains(self):
        domains = self.dom.findall('emailProvider/domain')

        logger.debug("\nGetting Domains")
        for d in domains:
            logger.debug(d.text)

        return domains

    def getSMTPHost(self):
        port = self.dom.findall('emailProvider/outgoingServer')
        for p in port:
            if p.attrib['type'] == 'smtp':
                logger.debug("\nGot SMTPort: %s" % port)
                return p.find('hostname').text
        return None

    def getSMTPPort(self):
        port = self.dom.findall('emailProvider/outgoingServer')
        for p in port:
            if p.attrib['type'] == 'smtp':
                logger.debug("\nGot SMTPort: %s" % port)
                return p.find('port').text
        return None


def get_provider():
    providers = []
    names = getProviderFromFilenames()
    logger.info("Files found: " + str(len(names)))
    for p in names:
        providers.append(ProviderXMLHandler(p))

    return providers
