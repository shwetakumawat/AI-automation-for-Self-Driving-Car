import math
import pygame as pg
from utils import lerp, get_interersection_point


class Sensor:
  '''
  a sensor that detects if its rays hit something
  this class' lifecycle is dependent on Car
  '''
  def __init__(self, on_car, count = 3, length = 100, spread = math.pi / 4) -> None:
    self.car = on_car
    self.ray_count = count
    self.ray_len = length
    self.ray_spread = spread
    
    # each ray corresponds to a reading
    # list of lines represented by a tuple (start, end)
    self.rays = []
    # list of numbers of how far the detected thing is
    self.readings = []

  def update(self, road_borders, other_cars):
    self._cast_rays()

    # clear the readings and fill it with new readings
    self.readings.clear()
    for ray in self.rays:
      self.readings.append(
        self._get_reading(ray, road_borders, other_cars)
      )
  
  def _get_reading(self, ray, borders, other_cars):
    touches = []

    # check for touching the road borders
    for border in borders:
      intersection = get_interersection_point(
        ray[0],
        ray[1],
        border[0],
        border[1]
      )
      if intersection:
        touches.append(intersection)
    
    # check for touching other cars by chevhing intersection with all edges
    for other_car in other_cars:
      for i in range(len(other_car.rect_points)):
        intersection = get_interersection_point(
          ray[0],
          ray[1],
          other_car.rect_points[i],
          other_car.rect_points[(i + 1) % len(other_car.rect_points)]
        )
        if intersection:
          touches.append(intersection)
    
    if len(touches) == 0:
      # no intersection with anything
      return None
    else:
      # closest intersection to the start of the ray (car center)
      min_offset = min(map(lambda t: t['offset'], touches))
      # only return the closest one
      for touch in touches:
        if touch['offset'] == min_offset:
          return touch

  def _cast_rays(self):
    self.rays = []

    for i in range(self.ray_count):
      # avoid dividing by 0  if there is only 1 ray
      angle_factor = i / (self.ray_count - 1) if self.ray_count > 1 else 0.5
      # get the angle that the ray should draw at
      # using the index as the ratio to it is spaced evenly
      angle = lerp(
        self.ray_spread / 2,
        -self.ray_spread / 2,
        angle_factor
      )
      # rotate the angle to the car's direction
      angle += self.car.direction
      # start from the car's center
      start_pos = pg.Vector2(self.car.x_pos, self.car.y_pos)
      # calculate the end position of the ray
      end_pos = pg.Vector2(
        self.car.x_pos - math.sin(angle) * self.ray_len, 
        self.car.y_pos - math.cos(angle) * self.ray_len
      )
      self.rays.append((start_pos, end_pos))
  
  def render(self, screen: pg.Surface):
    # draws the rays
    for i in range(self.ray_count):
      ray_start = self.rays[i][0]
      ray_end = self.rays[i][1]

      # if it detects something, draw the rays black from the hit point onward
      if self.readings[i]:
        point = self.readings[i]['point']
        pg.draw.line(screen, "yellow", ray_start, point, 2)
        pg.draw.line(screen, "black", point, ray_end, 2)
      else:
        pg.draw.line(screen, "yellow", ray_start, ray_end, 2)
  
  def get_offsets(self):
    '''
    return the offset value modified, now it represents the distance from ray end
    to the contact point
    '''
    return [
      1 - reading['offset'] if reading else 0
      for reading in self.readings
    ]