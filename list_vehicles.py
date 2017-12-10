#!/usr/bin/env python
from mbtapi.client import Vehicle
from mbtapi.model import VehicleModel
from mbtapi.util import ptable


def print_vehicle_status():
    tbl_data = []
    for vehicle in Vehicle.getAll():
        if vehicle.isSubway():
            tbl_data.append([
                vehicle.id,
                vehicle.prettyRoute(),
                vehicle.prettyStatus(),
                vehicle.stopId,
                vehicle.directionId
            ])
    ptable(tbl_data)
    
if __name__ == '__main__':
    print_vehicle_status()
