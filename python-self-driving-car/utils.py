import pygame as pg


def lerp(A: float, B: float, t: float):
  '''
  A - first number
  B - second number
  t - interpolation factor, a number between 0 and 1
  function to get an intermediate value between A and B
  '''
  return A + (B - A) * t

def get_interersection_point(
  line_1_start: pg.Vector2, 
  line_1_end: pg.Vector2, 
  line_2_start: pg.Vector2, 
  line_2_end: pg.Vector2
):
  '''
  find the intersection point of two lines
  each line is defined by two points, start and end
  see demo for more details
  '''
  a = line_1_start
  b = line_1_end
  c = line_2_start
  d = line_2_end

  tTop = (d.x - c.x) * (a.y - c.y) - (d.y - c.y) * (a.x - c.x)
  uTop = (c.y - a.y) * (a.x - b.x) - (c.x - a.x) * (a.y - b.y)

  bottom = (d.y - c.y) * (b.x - a.x) - (d.x - c.x) * (b.y - a.y)

  if bottom == 0:
    return None
  
  t = tTop / bottom;
  u = uTop / bottom;

  if t < 0 or t > 1 or u < 0 or u > 1:
    return None

  return {
    'point': pg.Vector2(
      lerp(a.x, b.x, t),
      lerp(a.y, b.y, t)
    ),
    'offset': t
  }

def has_intersection(polygon_points_1, polygon_points_2):
  '''
  polygon_points_1 - list of points of the first polygon
  polygon_points_2 - list of points of the second polygon
  function to check if two polygons intersect
  it iterates through all the lines formed by each poly and
  see if any of the lines intersects
  '''
  for i in range(len(polygon_points_1)):
    for j in range(len(polygon_points_2)):
      # mod the length so that the last point connects to the first at index 0
      p1 = polygon_points_1[i]
      p2 = polygon_points_1[(i + 1) % len(polygon_points_1)]
      p3 = polygon_points_2[j]
      p4 = polygon_points_2[(j + 1) % len(polygon_points_2)]

      # check if any of the edges intersects
      if get_interersection_point(p1, p2, p3, p4) is not None:
        return True
      
  return False