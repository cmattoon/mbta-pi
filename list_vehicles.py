#!/usr/bin/env python
from mbtapi.client import Vehicle, Stop
from mbtapi.model import VehicleModel
from mbtapi.util import ptable

stops = {stop.id: stop for stop in Stop.getAll()}

def print_vehicle_status():
    tbl_data = []
    for vehicle in Vehicle.getAll():
        if vehicle.isSubway():
            tbl_data.append([
                vehicle.id,
                vehicle.prettyRoute(),
                vehicle.prettyStatus(),
                vehicle.prettyStopName(),
                vehicle.stopId,
                vehicle.routeId,
                vehicle.tripId
            ])
    ptable(tbl_data, sort_by=1)
    
if __name__ == '__main__':
    print_vehicle_status()
