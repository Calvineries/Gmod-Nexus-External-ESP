import hashlib, random, ctypes
from math import sqrt
from dataclasses import dataclass

@dataclass
class ScreenSize:
    x = ctypes.windll.user32.GetSystemMetrics(0) - 1
    y = ctypes.windll.user32.GetSystemMetrics(1) - 1

@dataclass
class Vector3:
    x: float
    y: float
    z: float

@dataclass
class Vector2:
    x: float
    y: float

def distance(start_point: Vector3, end_point: Vector3):
	distance = sqrt(
        (int(start_point.x) - int(end_point.x)) * (int(start_point.x) - int(end_point.x)) +
		(int(start_point.y) - int(end_point.y)) * (int(start_point.y) - int(end_point.y)) +
		(int(start_point.z) - int(end_point.z)) * (int(start_point.z) - int(end_point.z)))

	return int(abs(round(distance)))

def get_random_string() -> None:
    chars = ['A',
    'B', 'C', 'D', 'E', 'F','G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'U', 'P', 'R', 'S', 'T', 'W', 'Y', 'Z',
    'a', 'b', 'c', 'd', 'e', 'f','g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'u', 'p', 'r', 's', 't', 'w', 'y', 'z',
    '1','2', '3', '4', '5', '6', '7', '8', '9', '0', '!', '@', '#', '$', '%', '^', '&', '&', '(', ')', '-', '_', '=', '+']
    return ''.join(random.choice(chars) for _ in range(0, 15))