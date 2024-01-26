#  coding=utf-8
#  Copyright 2021-present, the Recognai S.L. team.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import os
from typing import TYPE_CHECKING, Optional
from uuid import uuid4

from argilla.server.pydantic_v1 import BaseSettings, PrivateAttr

if TYPE_CHECKING:
    from argilla.server.security.authentication.oauth2 import OAuth2Settings


class Settings(BaseSettings):

    """
    Attributes
    ----------

    secret_key:
        The secret key used for signed the token data

    algorithm:
        Encryption algorithm for token data

    token_expiration_in_minutes:
        The session token expiration in minutes. Default=30000

    """

    secret_key: str = uuid4().hex
    algorithm: str = "HS256"
    token_expiration_in_minutes: int = 15
    oauth_file: str = ".oauth.yaml"

    _oauth_settings: Optional["OAuth2Settings"] = PrivateAttr(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._oauth_settings = None

    @property
    def token_expire_time(self):
        """The token expiration time in seconds"""
        return self.token_expiration_in_minutes * 60

    @property
    def oauth2(self):
        from argilla.server.security.authentication.oauth2 import OAuth2Settings

        if self._oauth_settings:
            return self._oauth_settings

        if not self._oauth_settings and os.path.exists(self.oauth_file):
            self._oauth_settings = OAuth2Settings.from_yaml(self.oauth_file)
        else:
            self._oauth_settings = OAuth2Settings(enabled=False)

        return self._oauth_settings

    class Config:
        env_prefix = "ARGILLA_LOCAL_AUTH_"

        fields = {
            "secret_key": {"env": ["SECRET_KEY", f"{env_prefix}SECRET_KEY"]},
            "token_expiration_in_minutes": {
                "env": [
                    "TOKEN_EXPIRATION_IN_MINUTES",
                    f"{env_prefix}TOKEN_EXPIRATION_IN_MINUTES",
                ]
            },
        }


settings = Settings()
