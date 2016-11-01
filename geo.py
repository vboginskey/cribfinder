import math

def distance(lat1, lon1, lat2, lon2):
    phi1, phi2 = map(math.radians, [lat1, lat2])
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return c * 6371 * 0.621371

def in_box(lat, lon, box):
    if box[0] < lat < box[2] and box[1] < lon < box[3]:
        return True

    return False
