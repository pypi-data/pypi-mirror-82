#!/usr/bin/env python3

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

"""ADO user API wrapper."""

import logging
from typing import cast

from simple_ado.base_client import ADOBaseClient
from simple_ado.exceptions import ADOException
from simple_ado.http_client import ADOHTTPClient
from simple_ado.types import TeamFoundationId


class ADOUserClient(ADOBaseClient):
    """Wrapper class around the ADO user APIs.

    :param http_client: The HTTP client to use for the client
    :param log: The logger to use
    """

    def __init__(self, http_client: ADOHTTPClient, log: logging.Logger) -> None:
        super().__init__(http_client, log.getChild("user"))

    def get_team_foundation_id(self, identity: str) -> TeamFoundationId:
        """Fetch the unique Team Foundation GUID for a given identity.

        :param str identity: The identity to fetch for (should be email for users and display name for groups)

        :returns: The team foundation ID

        :raises ADOException: If we can't get the identity from the response
        """

        request_url = self.http_client.api_endpoint(is_default_collection=False)
        request_url += "/IdentityPicker/Identities?api-version=5.1-preview.1"

        body = {
            "query": identity,
            "identityTypes": ["user", "group"],
            "operationScopes": ["ims"],
            "properties": ["DisplayName", "Mail"],
            "filterByAncestorEntityIds": [],
            "filterByEntityIds": [],
        }
        response = self.http_client.post(request_url, json_data=body)
        response_data = self.http_client.decode_response(response)

        try:
            result = response_data["results"][0]["identities"][0]
        except:
            raise ADOException("Could not resolve identity: " + identity)

        if result["entityType"] == "User" and identity.lower() == result["mail"].lower():
            return cast(TeamFoundationId, str(result["localId"]))

        if result["entityType"] == "Group" and identity.lower() == result["displayName"].lower():
            return cast(TeamFoundationId, str(result["localId"]))

        raise ADOException("Could not resolve identity: " + identity)
