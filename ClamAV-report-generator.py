#!/usr/bin/python
__author__ = 'sizov'

from operator import itemgetter
import smtplib
from email.mime.text import MIMEText
import glob

class VirusParser:

    maillog_path = '/var/log/maillog*'
    report_email_address = 'it@test.com'
    mail_theme = 'ClamAV statistics'
    mail_from = 'clamav@akvnzm.ru'
    smtp_server = '127.0.0.1'

    result = []

    def parse(self):
        files = glob.glob(self.maillog_path)
        for f in files:
            with open(f) as file:
                for line in file:
                    curr_line = line.split()
                    if len(curr_line) == 9 and curr_line[4] == 'clamsmtpd:' and curr_line[8].startswith('status=VIRUS'):
                        self.result.append({
                            'date': curr_line[0] + ' ' + curr_line[1],
                            'time': curr_line[2],
                            'from': curr_line[6].split('from=')[1].replace(',', ''),
                            'to': curr_line[7].split('to=')[1].replace(',', ''),
                            'virus': curr_line[8].split('status=VIRUS:')[1]
                            })

    def top_list(self, direction):

        top = {}
        for line in self.result:

            if line[direction] in top:
                top[line[direction]] += 1
            else:
                top[line[direction]] = 1
        return sorted(top.items(), key=itemgetter(1), reverse=True)

    def prepare_report(self):
        report = ''
        sender_top = self.top_list('from')
        receiver_top = self.top_list('to')

        break_line = '\n\n===================================\n\n'
        report += 'Top Virus Senders:\n\n'
        for sender in sender_top:
            report += '  ' + sender[0] + ": " + str(sender[1]) + '\n'

        report += break_line
        report += 'Top Virus Receivers:\n\n'
        for receiver in receiver_top:
            report += '  ' + receiver[0] + ": " + str(receiver[1]) + '\n'

        report += break_line
        report += 'Main statistics\n\n'
        for line in self.result:
            report += line['date'] + ' ' + line['time'] + ' '
            report += line['from'] + ' ---> ' + line['to'] + ' '
            report += line['virus'] + '\n'

        return report

    def send_report(self):
        msg = MIMEText(parser.prepare_report())
        msg['Subject'] = self.mail_theme
        msg['From'] = self.mail_from
        msg['To'] = self.report_email_address

        s = smtplib.SMTP(self.smtp_server)
        s.sendmail(self.mail_from, self.report_email_address, msg.as_string())
        s.quit()

parser = VirusParser()
parser.parse()
parser.send_report()
