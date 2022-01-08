"""Holds the workflow service that supports client workflow submissions"""
from typing import Tuple

from argo_workflows.apis import WorkflowServiceApi
from argo_workflows.models import (
    IoArgoprojWorkflowV1alpha1Workflow,
    IoArgoprojWorkflowV1alpha1WorkflowCreateRequest,
)

from hera.v1.client import Client
from hera.v1.config import Config


class WorkflowService:
    """Argo workflow service for performing actions against workflows - submissions, deletions, etc.

    Parameters
    ----------
    domain: str
        The Argo deployment domain to submit workflows to.
    token: str
        The token to use for authentication purposes. Note that this assumes the Argo deployment is fronted with a
        deployment/service that can intercept a request and check the Bearer token.
    namespace: str = 'default'
        The K8S namespace the workflow service submits workflows to. This defaults to the `default` namespace.
    """

    def __init__(self, domain: str, token: str, namespace: str = 'default'):
        self._domain = domain
        self._namespace = namespace
        api_client = Client(Config(domain), token).api_client
        self.service = WorkflowServiceApi(api_client=api_client)

    def submit(
        self, workflow: IoArgoprojWorkflowV1alpha1Workflow, namespace: str = 'default'
    ) -> IoArgoprojWorkflowV1alpha1Workflow:
        """Submits the given workflow to the given namespace.

        Parameters
        ----------
        workflow: IoArgoprojWorkflowV1alpha1Workflow
            The workflow to submit.
        namespace: str
            The K8S namespace of the Argo server to submit the workflow to.

        Raises
        ------
        argo_workflows.exceptions.ApiException: Raised upon any HTTP-related errors.
        """
        return self.service.create_workflow(
            namespace,
            IoArgoprojWorkflowV1alpha1WorkflowCreateRequest(workflow=workflow, namespace=namespace),
            _check_return_type=False,
        )

    def delete(self, name: str) -> Tuple[object, int, dict]:
        """Deletes a workflow from the given namespace based on the specified name.

        Parameters
        ----------
        name: str
            The name of the workflow to delete.

        Returns
        -------
            Tuple(object, status_code(int), headers(HTTPHeaderDict))

        Raises
        ------
        argo_workflows.exceptions.ApiException: Raised upon any HTTP-related errors.
        """
        return self.service.delete_workflow(self._namespace, name, _check_return_type=False)

    def get_workflow_link(self, name: str) -> str:
        """Assembles a workflow link for the given workflow name. Note that the returned path works only for Argo.

        Parameters
        ----------
        name: str
            The name of the workflow to assemble a link for.

        Returns
        -------
        str
            The workflow link.
        """
        return f'https://{self._domain}/workflows/{self._namespace}/{name}?tab=workflow'
