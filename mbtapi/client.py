"""
"""
import requests
import json


class MBTAClient(object):
    ENDPOINT = ''
    CACHE = {}
    
    def __init__(self, *args, **kwargs):
        self.data = dict(kwargs)

    def _fetch(self, path='/', **params):
        """need to update to fetch only object-specific link"""
        key = (self.ENDPOINT, path)
        
        try:
            return self.CACHE[key]
        
        except KeyError:
            resp = requests.get(self.ENDPOINT)
            if resp.ok:
                self.CACHE[key] = json.loads(resp.content.decode('UTF-8'))['data']
                return self.CACHE[key]
        return resp

    @classmethod
    def getAll(cls):
        c = cls()
        for obj in c._fetch():
            yield cls(**obj)
            
    def getAttr(self, key):
        return self.data['attributes'][key]
    
    @classmethod
    def getById(cls, search_id):
        c = cls()
        for obj in c._fetch():
            obj = cls(**obj)
            if obj.id == search_id:
                return obj
        return None
    
class Stop(MBTAClient):
    ENDPOINT = 'https://api-v3.mbta.com/stops'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            self.id = self.data['id']
            self.name = self.getAttr('name')
            self.parentStation = self.data['relationships']['parent_station']
        except KeyError:
            pass
        
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
        return str(self.routeId)[0].isdigit()
    
    def isCommuterRail(self):
        return self.routeId.startswith('CR-')

    def isSubway(self):
        subway_routes = ['Red', 'Blue', 'Orange', 'Green']
        return any([self.routeId.startswith(name) for name in subway_routes])
    
    def getPosition(self):
        return self.getAttr('latitude'), self.getAttr('longitude')

    def getPositionAndHeading(self):
        return self.getPosition() + (self.getAttr('bearing'))

    def getRouteColor(self):
        colors = {'Red': "\033[31m", 'Orange': "\033[33m",
                  'Green': "\033[92m", 'Green-A': "\033[92m", 'Green-B': "\033[92m",
                  'Green-C': "\033[92m", 'Green-D': "\033[92m", 'Green-E': "\033[92m",
                  'Blue': "\033[34m"}
        try:
            return colors[self.routeId]
        except KeyError:
            return ''

    def prettyRoute(self):
        color = self.getRouteColor()
        try:
            return "{}{}\033[0m".format(color, self.routeId)
        except KeyError:
            return "?? {}".format(self.routeId)

    def prettyStopName(self):
        return "{}{}\033[0m".format(
            self.getRouteColor(),
            Stop.getById(self.stopId).name
        )
        
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
        
