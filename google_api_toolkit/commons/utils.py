import hashlib
import logging
import os
import tempfile
from pathlib import Path
from typing import Any, MutableMapping, Sequence, Union

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import HttpRequest

logger = logging.getLogger(__name__)

USAGE_LIMIT_STATUS = 429
ALREADY_EXISTS_STATUS = 409
SERVICE_UNAVAILABLE = 503


def default_response_handler(
    request: HttpRequest, *, http=None, num_retries: int = 5
) -> MutableMapping[str, Any]:
    """
    The default response handler for a googleapiclient.http.HttpRequest.
    By default, will retry a failed request up to 5 times.

    Handled error responses:
        * 429 (usage limit): When quota is exceeded, will wait 2 sec
          before repeating the request.
        * 503 (service unavailable): The google end-point is not
          available, will wait 5 sec before repeating the request.

    Args:
        request: The request object to be executed.
        http: httplib2.Http, an http object to be used in place of the
            one the HttpRequest request object was constructed with.
        num_retries: Integer, number of times to retry with randomized
            exponential backoff. If all retries fail, the raised HttpError
            represents the last request. If zero (default), we attempt the
            request only once.

    Returns:
        The request's response.
    """

    return request.execute(http, num_retries)


class DiscoveryCache:
    """
    Fix some issues with the default caching method of
    discovery.build().

    https://github.com/googleapis/google-api-python-client/issues/325
    """

    def filename(self, url):
        return os.path.join(
            tempfile.gettempdir(),
            "google_api_discovery_" + hashlib.md5(url.encode()).hexdigest(),
        )

    def get(self, url):
        try:
            with open(self.filename(url), "rb") as f:
                return f.read().decode()
        except FileNotFoundError:
            return None

    def set(self, url, content):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(content.encode())
            f.flush()
            os.fsync(f)
        os.rename(f.name, self.filename(url))


def get_credentials(
    scopes: Sequence[str], path: Union[str, Path], *, local_server: bool = True
) -> Credentials:
    """
    Quick retrieval of a credentials object using ``InstalledAppFlow``.

    Args:
        scopes: Scope of access requested (see `oauth2.scopes`_).
        path: Path to file with your application's credentials (see
            `oauth2`_ to generate it).
            
    .. _oauth2: https://developers.google.com/identity/protocols/oauth2
    .. _oauth2.scopes: https://developers.google.com/identity/protocols/oauth2/scopes
    """  # noqa
    flow = InstalledAppFlow.from_client_secrets_file(path, scopes)
    if local_server:
        credentials = flow.run_local_server(port=0, open_browser=False)
    else:
        credentials = flow.run_console()

    return credentials


class EmptyResponse:
    pass


empty_response = EmptyResponse()
