from utils import get_interersection_point
import pygame as pg

lines = [
  ((1, 2), (0, 0), (0, 2), (1, 1)), # expects (0.667, 1.333)
  ((1, 2), (0, 0), (0, 1), (1, 1)), # expects (0.5, 1)
  ((1, 2), (0, 0), (0.7, 1), (1, 1)), # expects None
  ((1, 2), (0, 0), (0.5, 1), (1, 1)), # expects None
  ((1, 2), (1, 1.5), (0.5, 1), (1, 1)), # expects None
  ((1, 2), (1, 0.5), (0.5, 1), (1.5, 1)), # expects (1, 1)
  ((1, 2), (1, 0.5), (0.5, 1), (0.5, 0.5)), # expects None
]

for line in lines:
  print(get_interersection_point(
    pg.Vector2(line[0][0], line[0][1]), 
    pg.Vector2(line[1][0], line[1][1]), 
    pg.Vector2(line[2][0], line[2][1]), 
    pg.Vector2(line[3][0], line[3][1])
  ))