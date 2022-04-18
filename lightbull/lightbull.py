import base64
import datetime
import json
import requests

from .error import LightbullError
from .shows import LightbullShows
from .system import LightbullSystem


class Lightbull:
    def __init__(self, api_url, password):
        self._api_url = api_url
        self._password = password
        self._jwt = None

        self._auth()

        self.shows = LightbullShows(self)
        self.system = LightbullSystem(self)

    def config(self):
        return self._send_get("config")

    def simulator(self):
        return self._send_get("simulator")

    def _auth(self):
        # get jwt
        r = requests.post(self._build_url("auth"), json={"password": self._password})
        if r.status_code != 200:
            raise LightbullError("Authentication failed")

        # store expiry date and JWT
        jwt = r.json()["jwt"]
        jwt_data = json.loads(base64.b64decode(jwt.split(".")[1]))
        self._jwt_expiry = datetime.datetime.fromtimestamp(jwt_data["exp"])
        self._jwt = jwt

    def _reauth_if_required(self):
        if datetime.datetime.now() > self._jwt_expiry - datetime.timedelta(minutes=5):
            self._auth()

    def _send_get(self, *parts):
        self._reauth_if_required()
        r = requests.get(self._build_url(*parts), headers=self._get_headers())
        if not r.ok:
            raise LightbullError(f"API Error: HTTP {r.status_code} - {r.text}")

        try:
            return r.json()
        except:
            return None

    def _send_post(self, *parts, data={}):
        self._reauth_if_required()
        r = requests.post(self._build_url(*parts), headers=self._get_headers(), json=data)
        if not r.ok:
            raise LightbullError(f"API Error: HTTP {r.status_code} - {r.text}")

        try:
            return r.json()
        except:
            return None

    def _send_put(self, *parts, data={}):
        self._reauth_if_required()
        r = requests.put(self._build_url(*parts), headers=self._get_headers(), json=data)
        if not r.ok:
            raise LightbullError(f"API Error: HTTP {r.status_code} - {r.text}")

        try:
            return r.json()
        except:
            return None

    def _send_delete(self, *parts):
        self._reauth_if_required()
        r = requests.delete(self._build_url(*parts), headers=self._get_headers())
        if not r.ok:
            raise LightbullError(f"API Error: HTTP {r.status_code} - {r.text}")

    def _build_url(self, *parts):
        return "/".join([self._api_url, *parts])

    def _get_headers(self):
        return {"Authorization": f"Bearer {self._jwt}"}
