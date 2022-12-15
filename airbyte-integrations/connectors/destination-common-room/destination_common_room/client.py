#
# Copyright (c) 2022 Airbyte, Inc., all rights reserved.
#

from typing import Any, Mapping
from requests.exceptions import HTTPError
import requests


class CommonRoomClient:
    base_url = "https://api.commonroom.io/community/v1/"

    def __init__(self, bearer_token: str):
        self.bearer_token = bearer_token

    def fields(self):
        """
        API docs: https://api.commonroom.io/docs/community.html#tag/Members/paths/~1members~1customFields/get
        """
        return self._request("GET", "members/customFields")

    def member(self, email: str, data: Mapping[str, Any]):
        """
        API docs: https://api.commonroom.io/docs/community.html#operation/createOrUpdateCommunityMember
        """
        return self._request("POST", "members", dict({
            "socials": [{"type": "email", "value": email}],
            "source": "Recurring import"},
            **data
        ))

    def memberField(self, email: str, field: Mapping[str, Any], value: Any):
        """
        API docs: https://api.commonroom.io/docs/community.html#operation/setMemberCustomFieldValue
        field comes from fields()
        """
        return self._request("POST", "members/customFields", {
            "socialType": "email",
            "value": email,
            "customFieldId": field["id"],
            "customFieldValue": {"type": field["type"], "value": value}
        })

    def _request_headers(self) -> Mapping[str, Any]:
        return {"Authorization": f"Bearer {self.bearer_token}"} if self.bearer_token else {}

    def _request(
        self, http_method: str, path: str, json: Mapping[str, Any] = None
    ) -> requests.Response:
        url = f"{self.base_url}/{path}"
        headers = {"Accept": "application/json", **self._request_headers()}

        response = requests.request(
            method=http_method, url=url, headers=headers, json=json)

        if not response.ok:
            raise HTTPError(response.text, response=response)

        return response.json()
