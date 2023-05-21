import pygame as pg
from utils import lerp


class Road:
  '''
  the (infinite) road which cars will be drawn on
  also defines the boundaries in which the cars are contained
  '''
  def __init__(self, x_pos: float, width: float, lanes: int = 3) -> None:
    '''
    x_pos - the x position of the center of the road
    width - the width of the road
    lanes - the number of lanes in the road
    '''
    self.x_pos = x_pos
    self.width = width
    self.lanes = lanes

    self.lane_width = width / lanes
    # arbitrary large number to represent infinity, without it being too slow
    self.lane_height = 4e4

    self.left_edge = x_pos - width / 2
    self.right_edge = x_pos + width / 2
    self.top = -self.lane_height / 2
    self.bottom = self.lane_height / 2
    
    # find the x value of the left side of each lane from the second lane
    # spacing the lanes evenly
    self.lane_x_positions = [
      lerp(
        self.left_edge, 
        self.right_edge, 
        lane / self.lanes
      ) 
      for lane in range(lanes + 1)
    ]

    # color of the lines
    self.color = "white"

    # borders
    self.borders = [
      # (top left, bottom left)
      (pg.Vector2(self.left_edge, self.top), pg.Vector2(self.left_edge, self.bottom)),
      # (top right, bottom right)
      (pg.Vector2(self.right_edge, self.top), pg.Vector2(self.right_edge, self.bottom))
    ]
  
  def get_lane_center(self, lane_idx: int):
    '''
    lane_idx - the index of the lane, 0 is the leftmost lane
    function to get the center of a lane
    '''
    return self.lane_x_positions[lane_idx % self.lanes] + self.lane_width // 2

  def render(self, screen: pg.Surface):
    # drawing the dashed lines
    for i in range(1, len(self.lane_x_positions) - 1):
      line_x = self.lane_x_positions[i]
      # draw a dashed line with 50px spacing and 25px in length
      for j in range(int(self.top), int(self.bottom), 50):
        pg.draw.line(screen, self.color, (line_x, j), (line_x, j + 25), 5)
    
    # draw the borders on the side as solid lines
    for border in self.borders:
      pg.draw.line(screen, self.color, (border[0].x, border[0].y), (border[1].x, border[1].y), 5)