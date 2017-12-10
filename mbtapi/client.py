"""
"""
import requests
import json


class MBTAClient(object):
    ENDPOINT = ''

    def __init__(self, *args, **kwargs):
        self.data = dict(kwargs)

    def _fetch(self):
        """need to update to fetch only object-specific link"""
        resp = requests.get(self.ENDPOINT)
        if resp.ok:
            return json.loads(resp.content.decode('UTF-8'))['data']
        return resp

    @classmethod
    def getAll(cls):
        c = cls()
        for obj in c._fetch():
            yield cls(**obj)

class Stop(MBTAClient):
    ENDPOINT = 'https://api-v3.mbta.com/stops'

class Route(MBTAClient):
    ENDPOINT = 'https://api-v3.mbta.com/routes'

class Vehicle(MBTAClient):
    ENDPOINT = 'https://api-v3.mbta.com/vehicles'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            self.id = self.data['id']
            self.stopId = self.data['relationships']['stop']['data']['id']
            self.routeId = self.data['relationships']['route']['data']['id']
            self.directionId = self.getAttr('direction_id')
            self.lastUpdated = self.getAttr('last_updated')
            self.status = self.getAttr('current_status')
            
        except KeyError as e:
            print("\033[31m{}\033[0m".format(e))
            print(self.data)
            print("------")
            
    def isBusRoute(self):
        return self.routeId.isdigit()
    
    def getAttr(self, key):
        return self.data['attributes'][key]

    def getPosition(self):
        return self.getAttr('latitude'), self.getAttr('longitude')

    def getPositionAndHeading(self):
        return self.getPosition() + (self.getAttr('bearing'))

    def prettyStatus(self):
        colors = {
            'STOPPED_AT': "\033[31m",
            'IN_TRANSIT_TO': "\033[33m",
            'INCOMING_AT': "\033[32m",
        }
        try:
            return "{}{}\033[0m".format(colors[self.status], self.status)
        except KeyError:
            return "?? {}".format(self.status)
