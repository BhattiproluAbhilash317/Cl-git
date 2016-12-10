import logging 
import smtplib
from email.mime.text import MIMEText

log = logging.getLogger(__name__)

class SimpleBulkMailer(object):
    """SimpleBulkMailer is intended to provide a simple interface to automate
    sending several messages to an email server.
    messages are configured with the create_message function
    a send operation sends all 
    """

    def __init__(self, serve, origin='SIMPLEMAILER', auth = None, timeout = 10):
        """ initialize this class with connection information to an email service
         
        """
        self.servername = serve 
        self.timeout = timeout
        self.auth = auth
        self.origin = origin
        self.messages = [] 
        log.debug('initialized {}'.format(self.servername))

    def create_message(self, subject, message, destination, origin = None):
        """ create a new message in the array of outgoing messages
        parameters:
        subject: string type to use for the subject of the email
        message: body part for the message
        destination: to email address
        origin: optionally can set messages with alternate From
        return:
        nothing, just sets up a new message in to be delivered in an internal array
        """
        msg = MIMEText(message)
        if origin is not None:
            msg['From'] = origin
        else:
            msg['From'] = self.origin
        msg['Subject'] = subject
        msg['To'] = destination
        self.messages.append(msg)

    def _connect_smtp(self):
        """ helper function to initiate connection to an SMTP server
            return
            smtplib.SMTP object
        """
        smtp = None
        try:
            smtp = smtplib.SMTP(self.servername, timeout = self.timeout)
        except smtplib.SMTPException as err:
            log.critical('smtp service at {} is not currently available'.format(self.servername))
            log.critical(err)
        except Exception as err:
            log.critical('smtp other error {} is not currently available'.format(self.servername))
            log.critical(err)
        
        if self.auth is not None:
            try:
                smtp.login(self.auth[0], self.auth[1])
            except smtplib.SMTPException as err:
                log.warn('smtp service login error for {}'.format(self.servername))
                log.warn(err)
        return smtp 

    def send(self):
        """
         perfoms a bulk send on all messages that have been set previously by
         create message. communication with email service is limited to this blocking
         function.
         parameters:
        """
        log.debug('send {} messages'.format(len(self.messages)))
        smtp = self._connect_smtp()
        if smtp is not None:
            for msg in self.messages:
                #TODO:  There could be any exception in here somewhere
                log.debug('message: \n\r{}'.format(msg.as_string()))
                try:
                    smtp.sendmail(msg['From'], msg['To'], msg.as_string())
                except smtplib.SMTPRecipientsRefused as err:
                    log.warn('Recipient refused for following message: \n\r{}'.format(msg.as_string()))
                    log.warn(err)
                except smtplib.SMTPException as err:
                    log.critical('something went wrong with sending message: \n\r{}'.format(msg.as_string()))
                    log.critical(err)
            smtp.quit()
        else:
            log.warning('emails did not get sent because of exception in connection')
