# Copyright 2012 OpenStack Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from oslo_log import log
from oslo_utils import encodeutils
import six
from six.moves import http_client

from diveintoslic.i18n import _


LOG = log.getLogger(__name__)

# Tests use this to make exception message format errors fatal
_FATAL_EXCEPTION_FORMAT_ERRORS = False


def _format_with_unicode_kwargs(msg_format, kwargs):
    try:
        return msg_format % kwargs
    except UnicodeDecodeError:
        try:
            kwargs = {k: encodeutils.safe_decode(v)
                      for k, v in kwargs.items()}
        except UnicodeDecodeError:
            # NOTE(jamielennox): This is the complete failure case
            # at least by showing the template we have some idea
            # of where the error is coming from
            return msg_format

        return msg_format % kwargs


class Error(Exception):
    """Base error class.

    Child classes should define an HTTP status code, title, and a
    message_format.

    """

    code = 500
    title = http_client.responses[http_client.BAD_REQUEST]
    message_format = None

    def __init__(self, message=None, **kwargs):
        try:
            message = self._build_message(message, **kwargs)
        except KeyError:
            # if you see this warning in your logs, please raise a bug report
            if _FATAL_EXCEPTION_FORMAT_ERRORS:
                raise
            else:
                LOG.warning('missing exception kwargs (programmer error)')
                message = self.message_format

        super(Error, self).__init__(message)

    def _build_message(self, message, **kwargs):
        """Build and returns an exception message.

        :raises KeyError: given insufficient kwargs

        """
        if message:
            return message
        return _format_with_unicode_kwargs(self.message_format, kwargs)


class ValidationError(Error):
    message_format = _("Expecting to find %(attribute)s in %(target)s."
                       " The server could not comply with the request"
                       " since it is either malformed or otherwise"
                       " incorrect. The client is assumed to be in error.")
    code = int(http_client.BAD_REQUEST)
    title = http_client.responses[http_client.BAD_REQUEST]


class NotFound(Error):
    message_format = _("Could not find: %(target)s.")
    code = int(http_client.NOT_FOUND)
    title = http_client.responses[http_client.NOT_FOUND]


class VersionNotFound(NotFound):
    message_format = _("Could not find version: %(version)s.")


class SecurityError(Error):
    """Security error exception.

    Avoids exposing details of security errors, unless in insecure_debug mode.

    """

    amendment = _('(Disable insecure_debug mode to suppress these details.)')

    def __deepcopy__(self):
        """Override the default deepcopy.

        Keystone :class:`storeanalysis.exception.Error` accepts an optional message
        that will be used when rendering the exception object as a string. If
        not provided the object's message_format attribute is used instead.
        :class:`storeanalysis.exception.SecurityError` is a little different in
        that it only uses the message provided to the initializer when
        storeanalysis is in `insecure_debug` mode. Instead it will use its
        `message_format`. This is to ensure that sensitive details are not
        leaked back to the caller in a production deployment.

        This dual mode for string rendering causes some odd behaviour when
        combined with oslo_i18n translation. Any object used as a value for
        formatting a translated string is deep copied.

        The copy causes an issue. The deep copy process actually creates a new
        exception instance with the rendered string. Then when that new
        instance is rendered as a string to use for substitution a warning is
        logged. This is because the code tries to use the `message_format` in
        secure mode, but the required kwargs are not in the deep copy.

        The end result is not an error because when the KeyError is caught the
        instance's ``message`` is used instead and this has the properly
        translated message. The only indication that something is wonky is a
        message in the warning log.
        """
        return self

    def _build_message(self, message, **kwargs):
        """Only returns detailed messages in insecure_debug mode."""
        if message:
            if isinstance(message, six.string_types):
                # Only do replacement if message is string. The message is
                # sometimes a different exception or bytes, which would raise
                # TypeError.
                message = _format_with_unicode_kwargs(message, kwargs)
            return _('%(message)s %(amendment)s') % {
                'message': message,
                'amendment': self.amendment}

        return _format_with_unicode_kwargs(self.message_format, kwargs)


class UnexpectedError(SecurityError):
    """Avoids exposing details of failures, unless in insecure_debug mode."""

    message_format = _("An unexpected error prevented the server "
                       "from fulfilling your request.")

    debug_message_format = _("An unexpected error prevented the server "
                             "from fulfilling your request: %(exception)s.")


class ConfigFileNotFound(UnexpectedError):
    debug_message_format = _("The Keystone configuration file %(config_file)s "
                             "could not be found.")


class ArgTypeError(Error):
    message_format = _("Argument type error, which is not excepted.")
