from random import random
import json


class NeuralNetwork:
  '''
  A neural network is a collection of levels
  '''
  def __init__(self, neuron_count_list) -> None:
    '''
    neuron_count_list - a list of the number of neurons in each level
    '''
    # initializes the levels so each level connects to the next
    self.levels = [
      Level(neuron_count_list[i], neuron_count_list[i + 1])
      for i in range(len(neuron_count_list) - 1)
    ]
  
  def feed_forward(self, given_inputs):
    '''
    given_inputs - a list of numbers to feed into the first level
    '''
    outputs = self.levels[0].feed_forward(given_inputs)

    # put the outputs of the first level into the next level and repeat
    for i in range(1, len(self.levels)):
      outputs = self.levels[i].feed_forward(outputs)
    
    # final outputs
    return outputs

  def print_formatted(self):
    net_levels = [
      level.__dict__ for level in self.levels
    ]
    for level in net_levels:
      for k,v in level.items():
        print(k, v)
      print()
    print('---')

  def serialize(self):
    net_levels = [
      level.__dict__ for level in self.levels
    ]
    return json.dumps(net_levels)


class Level:
  '''
  A level or layer is a collection of neurons (input) and 
  connects to another collection of neurons (output)
  '''
  def __init__(self, input_count, output_count) -> None:
    '''
    input_count - the number of nodes in the input layer
    output_count - number of nodes in the output layer
    '''

    # initialize the lists 
    # inputs are a list of numbers from some data
    # outputs are a list of 0 and 1 indicating whether the neuron fires or not
    self.inputs = [None for _ in range(input_count)]
    self.outputs = [None for _ in range(output_count)]

    # each output neuron has a bias, ie a value above which it will fire
    self.biases = [None for _ in range(output_count)]

    # there will be a connection between each input node and output node
    # each connection between neurons has a weight
    # weights are the strength of connection, controls how much it affects the output
    self.weights = [
      [None for _ in range(output_count)] 
      for _ in range(input_count)
    ]

    self.randomize()
  
  def randomize(self):
    '''
    randomize weights and biases
    sets each to a float between 1 and -1
    '''
    for i in range(len(self.inputs)):
      for j in range(len(self.outputs)):
        self.weights[i][j] = random() * 2 - 1
    
    for i in range(len(self.biases)):
      self.biases[i] = random() * 2 - 1
  
  def feed_forward(self, given_inputs):
    '''
    given_inputs - a list of numbers that will be fed into the input neurons
    '''
    # set the inputs from the raw inputs
    # the give_inputs are going to come from the sensors
    for i in range(len(self.inputs)):
      self.inputs[i] = given_inputs[i]
    
    # calculate the outputs
    # each output neuron has a value that is the input * weight of the connection
    for i in range(len(self.outputs)):
      output_sum = 0
      for j in range(len(self.inputs)):
        output_sum += self.inputs[j] * self.weights[j][i]

      # if the output sum is greater than the bias, it will fire
      if output_sum > self.biases[i]:
        self.outputs[i] = 1
      else:
        self.outputs[i] = 0
    
    return self.outputs