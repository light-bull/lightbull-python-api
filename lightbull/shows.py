from lightbull.error import LightbullError


class LightbullShows:
    def __init__(self, lightbull):
        self._lightbull = lightbull
    
    def get_shows(self):
        tmp = self._lightbull._send_get('shows')
        try:
            return tmp["shows"]
        except KeyError:
            return LightbullError("Unexpected data returned from /shows endpoint: {}".format(tmp))

    def get_show(self, show_id):
        return self._lightbull._send_get('shows', show_id)

    def new_show(self, name, favorite=False):
        r = self._lightbull._send_post('shows', data={'name': name, 'favorite': favorite})
        return r
    
    def update_show(self, show_id, name=None, favorite=None):
        show = self.get_show(show_id)

        data = {
            'name': name or show['name'],
            'favorite': favorite or show['favorite'],
        }
       
        self._lightbull._send_put('shows', show_id, data=data)
    
    def delete_show(self, show_id):
        self._lightbull._send_delete('shows', show_id)
    
    def get_visual(self, visual_id):
        return self._lightbull._send_get('visuals', visual_id)

    def new_visual(self, show_id, name):
        return self._lightbull._send_post('visuals', data={'showId': show_id, 'name': name})

    def update_visual(self, visual_id, name=None):
        visual = self.get_visual(visual_id)

        data = {
            'name': name or visual['name']
        }

        self._lightbull._send_put('visuals', visual_id, data=data)
    
    def delete_visual(self, visual_id):
        self._lightbull._send_delete('visuals', visual_id)
    
    def get_group(self, group_id):
        return self._lightbull._send_get('groups', group_id)

    def new_group(self, visual_id, parts, effect):
        return self._lightbull._send_post('groups', data={'visualId': visual_id, 'parts': parts, 'effectType': effect})

    def update_group(self, group_id, parts=None, effect=None):
        group = self.get_group(group_id)

        data = {
            'parts': parts or group['parts'],
            'effectType': effect or group['effect']['type'],
        }

        self._lightbull._send_put('groups', group_id, data=data)
    
    def delete_group(self, group_id):
        self._lightbull._send_delete('groups', group_id)
    
    def get_parameter(self, parameter_id):
        return self._lightbull._send_get('parameters', parameter_id)
    
    def update_parameter(self, parameter_id, current=None, default=None):
        data = {}
        if current:
            data['current'] = current
        if default:
            data['default'] = default
        
        self._lightbull._send_put('parameters', parameter_id, data=data)
    
    def get_current(self):
        return self._lightbull._send_get('current')
    
    def update_current(self, show_id=None, visual_id=None):
        data = {}
        if show_id:
            data['showId'] = show_id
        if visual_id:
            data['visualId'] = visual_id

        self._lightbull._send_put('current', data=data)

    def blank(self):
        return self._lightbull._send_put('current', data={'blank': True})
