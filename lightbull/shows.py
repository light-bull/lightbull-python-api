class LightbullShows:
    def __init__(self, lightbull):
        self._lightbull = lightbull
    
    def shows(self):
        return self._lightbull._send_get('shows')

    def show(self, show_id):
        return self._lightbull._send_get('shows', show_id)

    def new_show(self, name, favorite=False):
        r = self._lightbull._send_post('shows', data={'name': name, 'favorite': favorite})
        return r
    
    def update_show(self, show_id, name=None, favorite=None):
        show = self.show(show_id)

        data = {
            'name': name or show['name'],
            'favorite': favorite or show['favorite'],
        }
       
        self._lightbull._send_put('shows', show_id, data=data)
    
    def delete_show(self, show_id):
        self._lightbull._send_delete('shows', show_id)
    
    def visual(self, visual_id):
        return self._lightbull._send_get('visuals', visual_id)

    def new_visual(self, show_id, name):
        return self._lightbull._send_post('visuals', data={'show': show_id, 'name': name})

    def update_visual(self, visual_id, name=None):
        visual = self.visual(visual_id)

        data = {
            'name': name or visual['name']
        }

        self._lightbull._send_put('visuals', visual_id, data=data)
    
    def delete_visual(self, visual_id):
        self._lightbull._send_delete('visuals', visual_id)
    
    def group(self, group_id):
        return self._lightbull._send_get('groups', group_id)

    def new_group(self, visual_id, parts, effect):
        return self._lightbull._send_post('groups', data={'visual': visual_id, 'parts': parts, 'effect': effect})

    def update_group(self, group_id, parts=None, effect=None):
        group = self.group(group_id)

        data = {
            'parts': parts or group['parts'],
            'effect': effect or group['effect']['type'],
        }

        self._lightbull._send_put('groups', group_id, data=data)
    
    def delete_group(self, group_id):
        self._lightbull._send_delete('groups', group_id)
    
    def parameter(self, parameter_id):
        return self._lightbull._send_get('parameters', parameter_id)
    
    def update_parameter(self, parameter_id, current=None, default=None):
        data = {}
        if current:
            data['current'] = current
        if default:
            data['default'] = default
        
        self._lightbull._send_put('parameters', parameter_id, data=data)
    
    def current(self):
        return self._lightbull._send_get('current')
    
    def update_current(self, show_id=None, visual_id=None):
        data = {}
        if show_id:
            data['show'] = show_id
        if visual_id:
            data['visual'] = visual_id

        self._lightbull._send_put('current', data=data)

    def blank(self):
        return self._lightbull._send_put('current', data={'blank': True})