import requests

from .error import LightbullError
from .shows import LightbullShows
from .system import LightbullSystem


class Lightbull:
    def __init__(self, api_url, password):
        self._api_url = api_url
        self._jwt = self._auth(password)

        self.shows = LightbullShows(self)
        self.system = LightbullSystem(self)

    def config(self):
        return self._send_get("config")

    def simulator(self):
        return self._send_get("simulator")

    def _auth(self, password):
        r = requests.post(self._build_url("auth"), json={"password": password})
        if r.status_code != 200:
            raise LightbullError("Authentication failed")
        return r.json()["jwt"]

    def _send_get(self, *parts):
        r = requests.get(self._build_url(*parts), headers=self._get_headers())
        if not r.ok:
            raise LightbullError(f"API Error: HTTP {r.status_code} - {r.text}")

        try:
            return r.json()
        except:
            return None

    def _send_post(self, *parts, data={}):
        r = requests.post(self._build_url(*parts), headers=self._get_headers(), json=data)
        if not r.ok:
            raise LightbullError(f"API Error: HTTP {r.status_code} - {r.text}")

        try:
            return r.json()
        except:
            return None

    def _send_put(self, *parts, data={}):
        r = requests.put(self._build_url(*parts), headers=self._get_headers(), json=data)
        if not r.ok:
            raise LightbullError(f"API Error: HTTP {r.status_code} - {r.text}")

        try:
            return r.json()
        except:
            return None

    def _send_delete(self, *parts):
        r = requests.delete(self._build_url(*parts), headers=self._get_headers())
        if not r.ok:
            raise LightbullError(f"API Error: HTTP {r.status_code} - {r.text}")

    def _build_url(self, *parts):
        return "/".join([self._api_url, *parts])

    def _get_headers(self):
        return {"Authorization": f"Bearer {self._jwt}"}
