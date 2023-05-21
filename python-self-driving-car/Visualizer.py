import pygame as pg
from utils import lerp
from Network import NeuralNetwork, Level


class Visualizer:
  '''
  A class to visualize a neural network
  shows the connections between the nodes and layers
  '''
  surface: pg.Surface
  
  @staticmethod
  def draw_network(surface: pg.Surface, network: NeuralNetwork):
    # find the bounds
    margin = 50
    left, top = margin, margin
    width = surface.get_width() - margin * 2
    height = surface.get_height() - margin * 2
    right = left + width

    # define a context to draw on
    Visualizer.surface = surface

    # each level has a height
    level_height = height / len(network.levels)
    
    # draw from back to front so the biases circles show on top of lines
    for i in range(len(network.levels) - 1, -1, -1):
      level_top = top + level_height * (len(network.levels))
      Visualizer.draw_level(
        network.levels[i],
        left, right, level_top, level_top + level_height
      )
  
  @staticmethod
  def draw_level(level: Level, left_bound, right_bound, top_bound, bottom_bound):
    # destructure for easier reference
    inputs = level.inputs
    outputs = level.outputs
    weights = level.weights
    biases = level.biases

    # helper functions to get the x evenly spaced
    # len - 1 because there are len - 1 spaces between the nodes, and idx begins at 0
    def get_input_x(idx):
      return lerp(left_bound, right_bound, idx / (len(inputs) - 1))
    def get_output_x(idx):
      return lerp(left_bound, right_bound, idx / (len(outputs) - 1))
    
    # draw the lines first so they are under the nodes
    # each input connects to each output
    for i in range(len(inputs)):
      input_x_pos = get_input_x(i)
      for j in range(len(outputs)):
        output_x_pos = get_output_x(j)
        Visualizer.draw_connection(
          input_x_pos, bottom_bound, output_x_pos, top_bound, weights[i][j]
        )

    # draw the input and output nodes
    for i in range(len(inputs)):
      x_pos = get_input_x(i)
      Visualizer.draw_node(x_pos, bottom_bound, inputs[i])
    
    for i in range(len(outputs)):
      x_pos = get_output_x(i)
      Visualizer.draw_node(x_pos, top_bound, outputs[i], bias=biases[i])
    

  @staticmethod
  def draw_node(x, y, node_value, bias = None):
    '''
    x - x position of the node
    y - y position of the node
    each node will be colored with its value
    output nodes have an optional bias ring
    '''
    radius = 18
    color = Visualizer.get_color(node_value)
    pg.draw.circle(Visualizer.surface, color, (x, y), radius)

    if bias is not None:
      bias_color = Visualizer.get_color(bias)
      # draw the bias offset times larger than the node
      offset = 1.5
      start_x = x - radius * offset
      start_y = y - radius * offset
      width = radius * (offset * 2)
      height = width
      pg.draw.arc(
        Visualizer.surface, 
        bias_color,
        (start_x, start_y, width, height), 
        0, 6.28, 3
      )
  
  @staticmethod
  def draw_connection(from_x, from_y, to_x, to_y, weight):
    '''
    from_x, from_y - position of the node to connect from
    to_x, to_y - position of the node to connect to
    weight - the weight of the connection
    '''
    width = 3
    color = Visualizer.get_color(weight)
    pg.draw.line(Visualizer.surface, color, (from_x, from_y), (to_x, to_y), width)
  
  @staticmethod
  def get_color(value):
    '''
    value - a number between -1 and 1
    gets the color that represents this value
    '''
    r, g, b = 0,0,0

    # since weights are from -1 to 1, take the magnitude of it
    color_number = abs(value) * 255

    # case negative: blue
    #   more negative, more blue --> closer to 0, more white
    # case positive: green
    #   more positive, more green --> closer to 0, more white
    if value < 0:
      r, g, b = 255 - color_number, 255 - color_number, 255
    else:
      r, g, b = 255 - color_number, 255, 255 - color_number
    
    return (r, g, b)