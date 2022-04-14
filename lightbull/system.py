class LightbullSystem:
    def __init__(self, lightbull):
        self._lightbull = lightbull

    def shutdown(self):
        return self._lightbull._send_post("shutdown")

    # TODO: ethernet
