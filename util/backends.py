from django.contrib.auth.backends import RemoteUserBackend

import os
import threading
import tempfile
import time

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from subprocess import Popen,PIPE,check_call

class TNQRemoteUserBackend(RemoteUserBackend):
    create_unknown_user = False

class SendmailBackend(BaseEmailBackend):
    """sendmail email backend class."""
    def __init__(self, fail_silently=False, sendmail_cmd=None, **kwargs):
        super(SendmailBackend, self).__init__(fail_silently=fail_silently)
        self.sendmail_cmd = sendmail_cmd
        if self.sendmail_cmd is None:
            try:
                self.sendmail_cmd = settings.SENDMAIL_CMD
            except:
                self.sendmail_cmd = "sendmail"
        if isinstance(self.sendmail_cmd, str):
            self.sendmail_cmd = self.sendmail_cmd.split()
        self._lock = threading.RLock()

    def open(self):
        return True

    def close(self):
        pass

    def send_messages(self, email_messages):
        """
        Sends one or more EmailMessage objects and returns the number of email
        messages sent.
        """
        if not email_messages:
            return
        self._lock.acquire()
        try:
            num_sent = 0
            for message in email_messages:
                sent = self._send(message)
                if sent:
                    num_sent += 1
        finally:
            self._lock.release()
        return num_sent

    def _get_environ(self):
        return os.environ

    def _send(self, email_message):
        """A helper method that does the actual sending."""
        if not email_message.recipients():
            return False
        try:
            ps = Popen(self.sendmail_cmd+list(email_message.recipients()), \
                       stdin=PIPE, env=self._get_environ())
            ps.stdin.write(email_message.message().as_string())
            ps.stdin.flush()
            ps.stdin.close()
            return not ps.wait()
        except:
            if not self.fail_silently:
                raise
            return False
        return True

class KerberizedSendmailBackend(SendmailBackend):
    def __init__(self, fail_silently=False, keytab_path=None, principal=None, **kwargs):
        super(KerberizedSendmailBackend, self).__init__(fail_silently=fail_silently, **kwargs)
        self.keytab_path = keytab_path or settings.KRB_KEYTAB
        self.principal = principal or settings.KRB_PRINCIPAL
        self.ccache_path = None
        self.ccache_time = 0

    def _get_environ(self):
        env = os.environ
        env["KRB5CCNAME"] = self.ccache_path
        return env

    def open(self):
        super(KerberizedSendmailBackend, self).open()
        if time.time() > self.ccache_time + 6*60*60:
            if not self.ccache_path:
                _, self.ccache_path = tempfile.mkstemp(prefix="krb5")
            check_call(["kinit", "-k", "-t", self.keytab_path, self.principal], env=self._get_environ())
            self.ccache_time = time.time()
        return True

    def send_messages(self, *args, **kwargs):
        self.open()
        return super(KerberizedSendmailBackend, self).send_messages(*args, **kwargs)

    def __del__(self):
        if self.ccache_path:
            os.unlink(self.ccache_path)
