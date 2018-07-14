import os
import logging
logger = logging.getLogger(__name__)

class ProxyController:

    http_proxy_key = "http_proxy"
    https_proxy_key = "https_proxy"

    http_proxy = os.environ.get(http_proxy_key)
    https_proxy = os.environ.get(https_proxy_key)

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def env_proxy_off(self):
        logger.info("Turning off env proxy")
        self.http_proxy = os.environ.get(self.http_proxy_key)
        self.https_proxy = os.environ.get(self.https_proxy_key)
        os.environ[self.http_proxy_key] = ""
        os.environ[self.https_proxy_key] = ""

    def env_proxy_on(self):
        logger.info("Turning on env proxy")
        os.environ[self.http_proxy_key] = self.http_proxy
        os.environ[self.https_proxy_key] = self.https_proxy
