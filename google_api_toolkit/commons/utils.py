import hashlib
import logging
import os
import tempfile

logger = logging.getLogger(__name__)

USAGE_LIMIT_STATUS = 429
ALREADY_EXISTS_STATUS = 409
SERVICE_UNAVAILABLE = 503


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


class EmptyResponse:
    pass


empty_response = EmptyResponse()
