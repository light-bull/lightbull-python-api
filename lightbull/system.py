class LightbullSystem:
    def __init__(self, lightbull):
        self._lightbull = lightbull

    def shutdown(self):
        return self._lightbull._send_post("shutdown")

    def get_ethernet(self):
        return self._lightbull._send_get("ethernet")

    def update_ethernet(self, mode, ip=None, gateway=None, dns=None):
        data = {
            "mode": mode,
            "ip": ip,
            "gateway": gateway,
            "dns": dns,
        }

        self._lightbull._send_put("ethernet", data=data)
