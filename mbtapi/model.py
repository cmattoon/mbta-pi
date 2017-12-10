class Model(object):
    pass

class VehicleModel(Model):
    def __init__(self, **data):
        self.data = data
        
        self.id = data['id']
        
        self.lastUpdated = data['attributes']['last_updated']
        
        self.routeId = data['relationships']['route']['data']['id']
        self.stopId = data['relationships']['stop']['data']['id']
        self.directionId = data['attributes']['direction_id']

        self.bearing = data['attributes']['bearing']
        self.lat = data['attributes']['latitude']
        self.lon = data['attributes']['longitude']

    
