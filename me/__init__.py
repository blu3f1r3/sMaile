import email
import imaplib
import json
import logging
import traceback

from prettytable import PrettyTable

from me import xml_parser
from me.Provider import Provider, Service
from me.utils import is_online, get_email_domain_name, parse_mailbox

logger = logging.getLogger(__name__)


class MailExtractor:
    target_email = None
    target_password = None
    target_provider = None
    target_email_hosts = {}
    error = []

    def __init__(self, target_email, target_password, as_json=False, output_file_path="out.json",
                 output_print_max=None):
        self.as_json = as_json
        self.output_file_path = output_file_path
        self.output_print_max = output_print_max if isinstance(output_print_max, int) else None

        self.target_email = target_email
        self.target_password = target_password
        assert self.target_email, "No target given"
        assert self.target_password, "Missing target password"

        self.provider_list: [Provider] = self.get_provider()
        assert len(self.provider_list), "no providers found"

        self.target_provider = self.get_target_provider()

        self.run()

    def run(self):
        self.login()

        if len(self.target_email_hosts.keys()) < 1:
            logger.warning('-- no data received --')
        else:
            self.prepare_results()
            self.result_output()

        if len(self.error) > 0:
            logger.warning('Errors occured')

    def login(self):
        for service in self.target_provider.services:
            logger.info("Trying to login '%s' per '%s' (%s:%s)" % (
                self.target_email, service.type, service.host, service.port
            ))

            if service.type == "imap":
                if self.imap_routine(service):
                    break

            elif service.type == "pop3":
                # TODO: Implement POP3 Login
                logger.info('pop3 not implemented yet')
                pass

    def imap_routine(self, service):
        _imap = None
        try:
            _imap = imaplib.IMAP4_SSL(host=service.host, port=service.port)
            _imap.login(self.target_email, self.target_password)
            logger.info("Connection established")

        except imaplib.IMAP4.error as e:
            logger.error(e)
            return

        mailboxes = self.imap_get_mail_boxes(_imap)

        for mailbox in mailboxes:
            if _imap.state == "SELECTED":
                _imap.close()

            _imap.select(mailbox, readonly=True)
            return_code, _mail_ids = _imap.search(None, 'ALL')

            _mail_ids = _mail_ids[0].decode('utf-8')
            mail_ids = _mail_ids.split(' ')

            logger.info("Mailbox: %s\t Mails: %i" % (mailbox, len(mail_ids)))

            for mail_id in mail_ids:
                if not mail_id:
                    continue

                typ, msg_data = _imap.fetch(mail_id, b'(RFC822)')

                msg = email.message_from_bytes(msg_data[0][1])
                host = get_email_domain_name(msg.get('From'))

                if not host in self.target_email_hosts.keys():
                    self.target_email_hosts[host] = 1
                self.target_email_hosts[host] += 1

        _imap.close()
        _imap.logout()
        return True

    @staticmethod
    def get_provider():
        provider = []
        _xml = xml_parser.get_provider()

        for _provider in _xml:
            prov = Provider(_provider.getDisplayName(), _provider.getDomain())
            services_provider = _provider.get_incoming_servers()

            for service in services_provider:
                prov.setService(
                    Service(service[0], service[1], service[2], _provider.getSMTPHost(), _provider.getSMTPPort()))

            provider.append(prov)
        return provider

    def get_target_provider(self):
        domain = get_email_domain_name(self.target_email)
        logger.info("Searching for domain '%s'" % domain)

        for provider in self.provider_list:
            if domain in provider.domain:
                return provider

        logger.warning('No provider found')

    @staticmethod
    def imap_get_mail_boxes(_imap):
        """
        :param
        :type imaplib
        :return:
        """
        mailboxes = []
        typ, mailbox_data = _imap.list()
        for line in mailbox_data:
            mailboxes.append(parse_mailbox(bytes.decode(line)))
        return mailboxes

    def prepare_results(self):
        _sorted = {k: v for k, v in sorted(self.target_email_hosts.items(), key=lambda item: item[1], reverse=True)}
        self.target_email_hosts = _sorted

    def result_output(self):
        x = PrettyTable()
        x.field_names = ['Host', 'Count']

        if self.output_print_max:
            results = list(self.target_email_hosts.keys())[:self.output_print_max]
        else:
            results = self.target_email_hosts.keys()

        for key in results:
            x.add_row([key, self.target_email_hosts[key]])
        print(x)

        if self.as_json:
            try:
                with open(self.output_file_path, 'w') as f:
                    f.write(json.dumps(self.target_email_hosts))
                logger.info("Saved output to '%s'" % self.output_file_path)

            except:
                logger.error(traceback.format_exc())
