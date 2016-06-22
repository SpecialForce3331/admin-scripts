#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'sizov'

import getopt
import sys

class LogParser:
    
    maillog = '/var/log/maillog'

    months = ('jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec')

    result = []

    def parse(self, mail_from=None, mail_to=None, date=None):

        if not mail_from or not mail_to:
            exit('Необходимо указать адрес как отправителя так и получателя!')

        mail_from = mail_from.lower()
        mail_to = mail_to.lower()

        queue = self.__find_queue(mail_from, mail_to, date)

        if queue:
            message_id = self.__find_postfix_messages_by_queue(queue)
            if message_id:
                new_queue = self.__find_spamd_messages_by_id(message_id, queue, mail_to)
                if new_queue:
                    self.__find_postfix_messages_by_queue(new_queue)

            for line in self.result:
                print(line)

    def __find_queue(self, mail_from=None, mail_to=None, date=None):

        queue = 0

        with open(self.maillog, 'r') as f:
            for line in f:
                line = line.lower()

                month = line.split()[0]
                day = int(line.split()[1])
                service_type = line.split()[4]

                if date:
                    d, m = date.split('/')
                    if self.months[int(m) - 1] != month or int(d) != day:
                        continue

                if service_type == 'clamsmtpd:':
                    if line.find(mail_from) > -1 and line.find(mail_to) > -1:
                        self.result.append(line)
                elif not service_type.startswith('postfix'):
                    continue

                if line.split()[6] == 'to=<' + mail_to + '>,' and queue == line.split()[5]:
                    return queue

                if line.split()[6] == 'from=<' + mail_from + '>,':
                    queue = line.split()[5]
                    continue


    def __find_postfix_messages_by_queue(self, queue):

        message_id = 0

        with open(self.maillog, 'r') as f:
            for line in f:
                line = line.lower()

                if queue != 0:
                    if queue == line.split()[5]:
                        if message_id == 0 and line.split()[6].startswith('message-id'):
                            message_id = line.split()[6].split('message-id=')[1]
                        self.result.append(line)
                    continue
        return message_id

    def __find_spamd_messages_by_id(self, message_id, old_queue, mail_to):

        if message_id == 0:
            return

        queue = 0
        with open(self.maillog, 'r') as f:
            for line in f:
                line = line.lower()

                if line.split()[4].startswith('spamd'):
                    if line.find(message_id) > -1:
                        self.result.append(line)
                    continue
                elif line.split()[4].startswith('postfix'):
                    if line.find(message_id) > -1 and line.split()[5] != old_queue and line.find(mail_to) > -1:
                        queue = line.split()[5]
            return queue


parser = LogParser()

sender = None
receiver = None

argv = sys.argv[1:]

opts, args = getopt.getopt(argv, "s:r:")

for arg in opts:
    if arg[0] == '-s':
        sender = arg[1]
    elif arg[0] == '-r':
        receiver = arg[1]

if sender and receiver:
    parser.parse(sender, receiver)
else:
    print('parser.py -s <sender> -r <receiver>')
    exit(2)
