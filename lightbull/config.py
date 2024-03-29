class LightbullConfig:
    def __init__(self, lightbull):
        self._lightbull = lightbull

    def get(self):
        return self._lightbull._send_get("config")

    def get_parts(self):
        return self._lightbull._send_get("config", "parts")
