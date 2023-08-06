"""
Mailer backend that sends email via oak-ridge.

oak-ridge is an open-source transactional mailer application developed by
Getme with a simple API for sending tran
"""

from contextlib import contextmanager
import io
import base64
import json
import sys
import requests
import threading

from manhattan.mail import EmailTemplate
from manhattan.mail.backends.base import BaseMailer

__all__ = ['Mailer']


class Mailer(BaseMailer):
    """
    Mailer that sends emails via oak-ridge.
    """

    def __init__(self,
        api_key='',
        api_endpoint='https://oak-ridge2.getme.co.uk',
        api_version='1.0',
        *args,
        **kwargs
        ):

        self.api_key = api_key
        self.api_endpoint = api_endpoint
        self.api_version = api_version
        super().__init__(*args, **kwargs)

        # A table for capturing Ids during a send
        self._capture_ids = None

    @contextmanager
    def capture_ids(self):
        """
        Capture a map of Ids generated when sending emails via oakridge.

        Note: Oakridge returns a single Id per send (even when there are
        multiple recipients), however, we combine this Id with each recipient
        (email address) to provide a unique Id for each email sent.
        """

        try:
            self._capture_ids = {}
            yield self._capture_ids

        finally:
            self._capture_ids = None

    def send(self, template):
        """Send the message template using oak-ridge"""

        # Validate the template is configured correctly for oak-ridge
        assert isinstance(template, EmailTemplate), \
                'oak-ridge supports sending `EmailTemplate` instances only'

        assert template.template_map, \
                '`template_map` must be used when sending through oak-ridge'

        # Build the URL to call
        url = '{endpoint}/{version}/send-email'.format(
            endpoint=self.api_endpoint,
            version=self.api_version
        )

        # Build the payload
        payload = {
            'api_key': self.api_key,
            'base_url': template.base_url,
            'bcc': [(r.addr, r.name) for r in template.bcc],
            'cc': [(r.addr, r.name) for r in template.cc],
            'css': template.css,
            'global_vars': template.global_vars,
            'recipient_vars': template.recipient_vars,
            'sender': (template.sender.addr, template.sender.name),
            'subject': template.subject,
            'template_path': template.template_path,
            'template_map': template.template_map,
            'to': [(r.addr, r.name) for r in template.to]
        }

        # Check for attachments
        if len(template.attachments) > 0:
            payload['attachments'] = []
            for attachment in template.attachments:

                # If the attachment content is not already in bytes then
                # covert it to bytes
                if isinstance(attachment.content, bytes):
                    content = attachment.content
                else:
                    content = io.BytesIO(
                        attachment.content.encode('utf-8')
                    ).getbuffer()

                payload['attachments'].append(
                    {
                        'filename': attachment.filename,
                        'file': base64.b64encode(
                            content
                        ).decode('utf8')
                    }
                )

        # Call the API
        response = requests.post(url, data={'payload': json.dumps(payload)})

        # Check for successful send to generate Ids
        try:
            response_json = response.json()

            if response_json['status'] == 'success':

                # Generate a table of recipients and oakridge Ids for the send
                id = response_json['payload']['send_request']

                if self._capture_ids is not None:
                    self._capture_ids.update({
                        r.addr: f'{id}:{r.addr.lower()}'
                        for r in template.to
                    })

        except ValueError:
            pass

        return response
