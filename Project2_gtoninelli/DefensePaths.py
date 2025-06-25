# GABRIEL F. TONINELLI - PROJECT2 - CSCI-1551

from panda3d.core import Vec3
from math import sin, cos, pi
import random

# CREATE A CIRCLE ON X-PLANE
def circular_x(center, radius, count):
    return [center + Vec3(0, radius * cos(2 * pi * i / count), radius * sin(2 * pi * i / count)) for i in range(count)]

# CREATE A CIRCLE ON Y-PLANE
def circular_y(center, radius, count):
    return [center + Vec3(radius * cos(2 * pi * i / count), 0, radius * sin(2 * pi * i / count)) for i in range(count)]

# CREATE A CIRCLE ON Z-PLANE
def circular_z(center, radius, count):
    return [center + Vec3(radius * cos(2 * pi * i / count), radius * sin(2 * pi * i / count), 0) for i in range(count)]

# RANDOM CLOUD FORMATION
def cloud(center, spread, count):
    return [center + Vec3(random.uniform(-spread, spread),
                          random.uniform(-spread, spread),
                          random.uniform(-spread, spread)) for _ in range(count)]

# BASEBALL SEAMS FORMATION (VISIBLE ARC)
def baseball_seams(center, radius, count):
    return [center + Vec3(
        radius * cos(2 * pi * i / count),
        radius * sin(2 * pi * i / count),
        radius * 0.6 * sin(2 * pi * i / count))  # More visible Z-arc
        for i in range(count)]

# GET ALL DEFENSE POSITIONS RELATIVE TO SHIP AND STATION
def get_all_defense_positions(ship_pos, station_pos):
    positions = []
    offset_distance = 1200  # Offset to space out formations

    positions += cloud(station_pos + Vec3(offset_distance, 0, 0), 250, 12)
    positions += baseball_seams(ship_pos + Vec3(-offset_distance, 0, 0), 300, 12)
    positions += circular_x(ship_pos + Vec3(0, offset_distance, 0), 200, 12)
    positions += circular_y(ship_pos + Vec3(0, -offset_distance, 0), 200, 12)
    positions += circular_z(ship_pos + Vec3(0, 0, offset_distance), 200, 12)

    return positions
