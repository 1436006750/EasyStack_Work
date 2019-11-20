# Copyright (c) 2018 SLIC personal studio.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import oslo_i18n
from oslo_serialization import jsonutils
import routes.middleware
import six
from six.moves import http_client
import webob
import webob.dec
import webob.exc

from diveintoslic import exception
from diveintoslic.i18n import _


JSON_ENCODE_CONTENT_TYPES = set(['application/json',
                                 'application/json-home'])

PARAMS_ENV = 'diveintoslic.params'


class SmarterEncoder(jsonutils.json.JSONEncoder):
    """Help for JSON encoding dict-like objects."""

    def default(self, obj):
        if not isinstance(obj, dict) and hasattr(obj, 'iteritems'):
            return dict(obj.iteritems())
        return super(SmarterEncoder, self).default(obj)


class Application(object):

    @classmethod
    def factory(cls, global_config, **local_config):
        """Used for paste app factories in paste.deploy config files.

        Any local configuration (that is, values under the [app:APPNAME]
        section of the paste config) will be passed into the `__init__` method
        as kwargs.

        A hypothetical configuration would look like:

            [app:wadl]
            latest_version = 1.3
            paste.app_factory = storeanalysis.fancy_api:Wadl.factory

        which would result in a call to the `Wadl` class as

            import storeanalysis.fancy_api
            storeanalysis.fancy_api.Wadl(latest_version='1.3')

        You could of course re-implement the `factory` method in subclasses,
        but using the kwarg passing it shouldn't be necessary.

        """
        return cls(**local_config)

    @webob.dec.wsgify(RequestClass=webob.Request)
    def __call__(self, req):
        # request body
        params_json = req.body
        if params_json:
            params_parsed = {}
            try:
                params_parsed = jsonutils.loads(params_json)
            except ValueError:
                e = exception.ValidationError(attribute='valid JSON',
                                              target='request body')
                return render_exception(e, request=req)
            finally:
                if not params_parsed:
                    params_parsed = {}

            if not isinstance(params_parsed, dict):
                e = exception.ValidationError(attribute='valid JSON object',
                                              target='request body')
                return render_exception(e, request=req)

            params = {}
            for k, v in params_parsed.items():
                if k in ('self', 'context'):
                    continue
                if k.startswith('_'):
                    continue
                params[k] = v
            req.environ[PARAMS_ENV] = params

        arg_dict = req.environ['wsgiorg.routing_args'][1]
        action = arg_dict.pop('action')
        del arg_dict['controller']

        params = req.environ.get(PARAMS_ENV, {})
        params.update(arg_dict)

        # TODO(termie): do some basic normalization on methods
        method = getattr(self, action)

        try:
            # import pdb; pdb.set_trace()
            result = method(req, **params)
        except Exception as e:
            return render_exception(exception.UnexpectedError(exception=e),
                                    user_locale=None)

        response_code = self._get_response_code(req)
        return render_response(body=result,
                               status=response_code,
                               method=req.method)

    def _get_response_code(self, req):
        code = (http_client.CREATED,
                http_client.responses[http_client.CREATED])
        return code


class Router(object):
    def __init__(self, mapper):
        self.mapper = mapper
        self._router = routes.middleware.RoutesMiddleware(self._dispatch,
                                                          self.mapper)

    @webob.dec.wsgify(RequestClass=webob.Request)
    def __call__(self, req):
        """Route the incoming request to a controller based on self.map.

        If no match, return a 404.

        """
        return self._router

    @staticmethod
    @webob.dec.wsgify(RequestClass=webob.Request)
    def _dispatch(req):
        """Dispatch the request to the appropriate controller.

        Called by self._router after matching the incoming request to a route
        and putting the information into req.environ.  Either returns 404
        or the routed WSGI app's response.

        """
        match = req.environ['wsgiorg.routing_args'][1]
        if not match:
            msg = (_('(%(url)s): The resource could not be found.') %
                   {'url': req.url})
            return render_exception(exception.NotFound(msg),
                                    request=req,
                                    user_locale=None)
        app = match['controller']
        return app


def render_response(body=None, status=None, headers=None, method=None):
    """Form a WSGI response."""
    if headers is None:
        headers = []
    else:
        headers = list(headers)
    headers.append(('Vary', 'X-Auth-Token'))

    if body is None:
        body = b''
        status = status or (http_client.NO_CONTENT,
                            http_client.responses[http_client.NO_CONTENT])
    else:
        content_types = [v for h, v in headers if h == 'Content-Type']
        if content_types:
            content_type = content_types[0]
        else:
            content_type = None

        if content_type is None or content_type in JSON_ENCODE_CONTENT_TYPES:
            body = jsonutils.dump_as_bytes(body, cls=SmarterEncoder)
            if content_type is None:
                headers.append(('Content-Type', 'application/json'))
        status = status or (http_client.OK,
                            http_client.responses[http_client.OK])

    # NOTE(davechen): `mod_wsgi` follows the standards from pep-3333 and
    # requires the value in response header to be binary type(str) on python2,
    # unicode based string(str) on python3, or else storeanalysis will not work
    # under apache with `mod_wsgi`.
    # storeanalysis needs to check the data type of each header and convert the
    # type if needed.
    # see bug:
    # https://bugs.launchpad.net/storeanalysis/+bug/1528981
    # see pep-3333:
    # https://www.python.org/dev/peps/pep-3333/#a-note-on-string-types
    # see source from mod_wsgi:
    # https://github.com/GrahamDumpleton/mod_wsgi(methods:
    # wsgi_convert_headers_to_bytes(...), wsgi_convert_string_to_bytes(...)
    # and wsgi_validate_header_value(...)).
    def _convert_to_str(headers):
        str_headers = []
        for header in headers:
            str_header = []
            for value in header:
                if not isinstance(value, str):
                    str_header.append(str(value))
                else:
                    str_header.append(value)
            # convert the list to the immutable tuple to build the headers.
            # header's key/value will be guaranteed to be str type.
            str_headers.append(tuple(str_header))
        return str_headers

    headers = _convert_to_str(headers)

    resp = webob.Response(body=body,
                          status='%d %s' % status,
                          headerlist=headers,
                          charset='utf-8')

    if method and method.upper() == 'HEAD':
        # NOTE(morganfainberg): HEAD requests should return the same status
        # as a GET request and same headers (including content-type and
        # content-length). The webob.Response object automatically changes
        # content-length (and other headers) if the body is set to b''. Capture
        # all headers and reset them on the response object after clearing the
        # body. The body can only be set to a binary-type (not TextType or
        # NoneType), so b'' is used here and should be compatible with
        # both py2x and py3x.
        stored_headers = resp.headers.copy()
        resp.body = b''
        for header, value in stored_headers.items():
            resp.headers[header] = value

    return resp


def render_exception(error, context=None, request=None, user_locale=None):
    """Form a WSGI response based on the current error."""
    error_message = error.args[0]
    message = oslo_i18n.translate(error_message, desired_locale=user_locale)
    if message is error_message:
        # translate() didn't do anything because it wasn't a Message,
        # convert to a string.
        message = six.text_type(message)

    body = {'error': {
        'code': error.code,
        'title': error.title,
        'message': message,
    }}
    headers = []
    return render_response(status=(error.code, error.title),
                           body=body,
                           headers=headers)
