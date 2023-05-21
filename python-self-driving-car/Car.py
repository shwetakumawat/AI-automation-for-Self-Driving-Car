import pygame as pg
from Controller import Controller
import math
from Sensor import Sensor
from utils import has_intersection
from Network import NeuralNetwork


class Car:
  def __init__(self, x_pos, y_pos, width, height, control_mode="man", max_speed = 3) -> None:
    # define the initial position and size of the car
    self.x_pos = x_pos
    self.y_pos = y_pos
    self.width = width
    self.height = height

    # define a list to store the corners of the rect for collisions
    self.rect_points = []

    # define the initial physical properites
    self.speed = 0
    self.acceleration = 0.2
    self.friction = 0.05
    self.max_speed = max_speed
    self.direction = 0
    self.damaged = False

    # link the controller class
    self.controls = Controller(control_mode)

    # link the sensor that will be used to detect the road borders
    # only add a sensor if the car is the not a dummy
    if control_mode != "dum":
      self.sensor = Sensor(self, count=5, spread=math.pi / 2, length=300)
      
      # give the car a network
      # it will have the amount of sensors number of nodes, then 6 nodes on a hidden layer
      # then 4 output nodes for each direction control
      self.brain = NeuralNetwork([self.sensor.ray_count, 6, 4])

    # only use the brain if it an ai
    if control_mode == "ai":
      self.use_brain = True
  
  def update(self, road_borders, other_cars = []):
    # stop moving if damaged
    if not self.damaged:
      self._move()
      self._update_corners()
      self._assess_damage(road_borders, other_cars)
    
    # not a dummy car, update the sensor
    if hasattr(self, "sensor"):
      self.sensor.update(road_borders, other_cars)

      # feed the sensor data to the first layer
      offsets = self.sensor.get_offsets()
      # outputs 4 values correcponding to each direction
      outputs = self.brain.feed_forward(offsets)

      # if I wanted this car to be self controlled, then control it with the outputs
      if hasattr(self, "use_brain") and self.use_brain:
        self.controls.forward = outputs[0]
        self.controls.back = outputs[1]
        self.controls.left = outputs[2]
        self.controls.right = outputs[3]
      # self.brain.print_formatted()

  def _move(self):
    # increase the speed by bit by bit so that it feels smoother
    if self.controls.forward:
      self.speed += self.acceleration
    elif self.controls.back:
      self.speed -= self.acceleration
    
    # set the speed to the max so that is cannot exceed max_speed
    if self.speed > self.max_speed:
      self.speed = self.max_speed
    
    # the reversing speed is slowed down by a factor
    reverse_factor = 2
    if self.speed < -self.max_speed / reverse_factor:
      self.speed = -self.max_speed / reverse_factor
    
    # decrease the speed by bit by bit when forward or back 
    # are not pressed so it slows down smoothly
    if self.speed > 0:
      self.speed -= self.friction
    if self.speed < 0:
      self.speed += self.friction

    # if speed is somehow between friction and -friction, it will vibrate in place
    # fix for that
    if abs(self.speed) < self.friction:
      self.speed = 0

    # only turn if the car is in motion
    if self.speed != 0:
      # flip the left-right controls if the car is reversing
      flip_factor = 1 if self.speed > 0 else -1

      # turn the car to a direction, the car's unit circle is rotation by 90 deg
      if self.controls.left:
        self.direction += 0.03 * flip_factor
      elif self.controls.right:
        self.direction -= 0.03 * flip_factor

    # 0 deg is facing up, so x and y (sin and cos) are switched
    self.x_pos -= math.sin(self.direction) * self.speed
    self.y_pos -= math.cos(self.direction) * self.speed
  
  def _update_corners(self):
    # construct the points for the 4 corners of the car
    # using the x and y pos as the center
    center_x = self.x_pos
    center_y = self.y_pos
    offset_x = self.width // 2
    offset_y = self.height // 2
    self.rect_points = [
      pg.Vector2(center_x - offset_x, center_y - offset_y),
      pg.Vector2(center_x + offset_x, center_y - offset_y),
      pg.Vector2(center_x + offset_x, center_y + offset_y),
      pg.Vector2(center_x - offset_x, center_y + offset_y)
    ]

    # need to use negative dir because the Y axis points down
    sin = math.sin(-self.direction)
    cos = math.cos(-self.direction)
    
    for i in range(len(self.rect_points)):
      point = self.rect_points[i]
      # point is translated so that the center is at the origin
      # ie, it is at the same location relative to 0,0 as it is relative to the center
      point.x -= self.x_pos
      point.y -= self.y_pos
      # perform rotation with the rotation matrix
      new_x = point.x * cos - point.y * sin
      new_y = point.x * sin + point.y * cos
      # translate back to original position
      point.x = new_x + self.x_pos
      point.y = new_y + self.y_pos
  
  def _assess_damage(self, road_borders, other_cars):
    # self.damaged = False
    # the car touches the borders
    for border in road_borders:
      if has_intersection(self.rect_points, border):
        self.damaged = True
        break
    # the car touches other cars
    for other_car in other_cars:
      if has_intersection(self.rect_points, other_car.rect_points):
        self.damaged = True
        break
  
  def render(self, screen: pg.Surface, color = "black"):
    if self.damaged:
      color = "gray"

    pg.draw.polygon(screen, color, self.rect_points)

    if hasattr(self, "sensor"):
      self.sensor.render(screen)
    