import pygame as pg
from Car import Car
from Road import Road
from Visualizer import Visualizer


pg.init()

# initialize the pygame window with this size
width, height = 700, 900
screen = pg.display.set_mode((width, height))


# define a road, center is at the middle of width, width is 90% of the road width
road_width = 300
road = Road(road_width / 2, road_width * 0.9)

# layer that all things will be drawn on, it's size is the size of the road
road_render_layer = pg.transform.scale(screen, (road_width, road.lane_height))

# layer that the visualized neural network will use
network_render_layer = pg.Surface((width - road_width, height))

# changes ai controlled or manual "ai" or "man"
main_car_mode = "man"

# define a car and other cars, at a quarter of the road
car = Car(road.get_lane_center(1), road.lane_height / 4, 30, 50, max_speed=5, control_mode=main_car_mode)
other_cars = [
  Car(road.get_lane_center(1), road.lane_height / 4 - 300, 30, 50, control_mode="dum")
]

# this function is called every frame
def frame(dt):
  # clear the screen, background
  road_render_layer.fill("lightgray")
  network_render_layer.fill((79, 79, 79))

  # update the cars2
  for other_car in other_cars:
    other_car.update(road.borders)
  car.update(road.borders, other_cars)

  # draw the road first so it is under the cars  
  road.render(road_render_layer)
  
  # draw the cars
  for other_car in other_cars:
    other_car.render(road_render_layer, "red")
  car.render(road_render_layer, "blue")

  # draw the neural network
  Visualizer.draw_network(network_render_layer, car.brain)

  # put the road layer on the screen on the left side
  # move the render layer as the car moves so the car appears in place
  # the car will be at 70% of the window height
  screen.blit(road_render_layer, (0, -car.y_pos + height * 0.7))

  # put the network render layer on the right side of the screen
  screen.blit(network_render_layer, (road_width, 0))

# this function is called every time there is an event
def onEvent(event):
  car.controls.update(event)

# clock to limit the fps to 60
clock = pg.time.Clock()
running = True
dt = 0
while running:
  for event in pg.event.get():
    if event.type == pg.QUIT:
      running = False
    if event:
      onEvent(event)
  
  frame(dt)

  # update the screen so things show up
  pg.display.flip()
  dt = clock.tick(60)

# cleanup
pg.quit()