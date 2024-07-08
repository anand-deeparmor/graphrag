# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License
"""Errors for the default configuration."""


class ApiKeyMissingError(ValueError):
    """LLM Key missing error."""

    def __init__(self, embedding: bool = False) -> None:
        """Init method definition."""
        api_type = "Embedding" if embedding else "Completion"
        api_key = "GRAPHRAG_EMBEDDING_API_KEY" if embedding else "GRAPHRAG_LLM_API_KEY"
        msg = f"API Key is required for {api_type} API. Please set either the OPENAI_API_KEY, GRAPHRAG_API_KEY or {api_key} environment variable."
        super().__init__(msg)


class AzureApiBaseMissingError(ValueError):
    """Azure API Base missing error."""

    def __init__(self, embedding: bool = False) -> None:
        """Init method definition."""
        api_type = "Embedding" if embedding else "Completion"
        api_base = "GRAPHRAG_EMBEDDING_API_BASE" if embedding else "GRAPHRAG_API_BASE"
        msg = f"API Base is required for {api_type} API. Please set either the OPENAI_API_BASE, GRAPHRAG_API_BASE or {api_base} environment variable."
        super().__init__(msg)


class AzureDeploymentNameMissingError(ValueError):
    """Azure Deployment Name missing error."""

    def __init__(self, embedding: bool = False) -> None:
        """Init method definition."""
        api_type = "Embedding" if embedding else "Completion"
        api_base = (
            "GRAPHRAG_EMBEDDING_DEPLOYMENT_NAME"
            if embedding
            else "GRAPHRAG_LLM_DEPLOYMENT_NAME"
        )
        msg = f"Deployment Name is required for {api_type} API. Please set either the OPENAI_DEPLOYMENT_NAME, GRAPHRAG_LLM_DEPLOYMENT_NAME or {api_base} environment variable."
        super().__init__(msg)

from google.cloud import api_keys_v2
from google.cloud.api_keys_v2 import Key


def restrict_api_key_http(project_id: str, key_id: str) -> Key:
    """
    Restricts an API key. To restrict the websites that can use your API key,
    you add one or more HTTP referrer restrictions.

    TODO(Developer): Replace the variables before running this sample.

    Args:
        project_id: Google Cloud project id.
        key_id: ID of the key to restrict. This ID is auto-created during key creation.
            This is different from the key string. To obtain the key_id,
            you can also use the lookup api: client.lookup_key()

    Returns:
        response: Returns the updated API Key.
    """

    # Create the API Keys client.
    client = api_keys_v2.ApiKeysClient()

    # Restrict the API key usage to specific websites by adding them to the list of allowed_referrers.
    browser_key_restrictions = api_keys_v2.BrowserKeyRestrictions()
    browser_key_restrictions.allowed_referrers = ["www.example.com/*"]

    # Set the API restriction.
    # For more information on API key restriction, see:
    # https://cloud.google.com/docs/authentication/api-keys
    restrictions = api_keys_v2.Restrictions()
    restrictions.browser_key_restrictions = browser_key_restrictions

    key = api_keys_v2.Key()
    key.name = f"projects/{project_id}/locations/global/keys/"+"123456789012345-abcdefghijklmnopqrstuv12345"
    key.restrictions = restrictions

    # Initialize request and set arguments.
    request = api_keys_v2.UpdateKeyRequest()
    request.key = key
    request.update_mask = "restrictions"

    # Make the request and wait for the operation to complete.
    response = client.update_key(request=request).result()

    print(f"Successfully updated the API key: {response.name}")
    # Use response.key_string to authenticate.
    return response

