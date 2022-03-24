from requests import Session, Response
from requests.sessions import SessionRedirectMixin

from exceptions import BigRedirectException, CycleRedirectException


class SessionRedirectCheckerMixin(SessionRedirectMixin):

    TOO_LONG_RESPONSE = 1000
    READ_CHUNK = 100

    def __init__(self):
        super(SessionRedirectCheckerMixin, self).__init__()
        self.history = []

    def resolve_redirects(self, resp: Response, req, stream=False, timeout=None,
                          verify=True, cert=None, proxies=None, yield_requests=False, **adapter_kwargs):
        """Receives a Response. Returns a generator of Responses or Requests."""

        if resp.url in self.history:
            raise CycleRedirectException('redirecting to one of previous url', resp.url)
        new_url = self.get_redirect_target(resp)
        if new_url:
            if int(resp.headers.get('content-length', 0)) > self.TOO_LONG_RESPONSE:
                resp.close()
                raise BigRedirectException('redirecting with big content-length', resp.url)
            response_size = 0
            for data in resp.iter_content(self.READ_CHUNK):
                response_size += len(data)
                if response_size > self.TOO_LONG_RESPONSE:
                    resp.close()
                    raise BigRedirectException('redirecting with big response', resp.url)

            self.history.append(resp.url)
            req = resp.request.copy()
            req.url = new_url
            if yield_requests:
                yield req
            else:
                resp = self.send(
                    req,
                    stream=stream,
                    timeout=timeout,
                    verify=verify,
                    cert=cert,
                    proxies=proxies,
                    allow_redirects=True,
                    **adapter_kwargs
                )
        yield resp


class SessionChecker(SessionRedirectCheckerMixin, Session):
    pass
