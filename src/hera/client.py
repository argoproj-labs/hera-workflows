"""Holds client configurations for communicating with Argo APIs"""
from argo_workflows.api_client import ApiClient as _ArgoApiClient

from hera.config import Config


class Client:
    """A client representation for the Argo SDK.

    This client takes in a configuration that specifies the Argo HTTP
    endpoint. This client representation layer is a Bearer authorization protocol on top of the config and creates an
    Argo client that is used to perform requests to an authentication Argo endpoint.

    Parameters
    ----------
    config: Config
        The assembled Argo configuration.
    token: str
        The Bearer token to pass along in the header of each request. This has to be generated by the client in order
        to pass the client's auth configuration that may sit in front of the Argo server.

    Notes
    -----
    This is typically used to initialize a WorkflowServiceApi.
    """

    def __init__(self, config: Config, token: str):
        self._client = _ArgoApiClient(
            configuration=config.config,
            header_name='Authorization',
            header_value=f'Bearer {token}',
        )

    @property
    def api_client(self) -> _ArgoApiClient:
        """Returns the Argo API client that was configured with the class token"""
        return self._client
