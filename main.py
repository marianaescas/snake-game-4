import pygame, sys, random
from pygame.math import Vector2

pygame.init()

tittle_font = pygame.font.Font(None, 60)
score_font = pygame.font.Font(None, 40)

BG_COLOR = (148, 226, 247)
SNAKE_COLOR = (229, 143, 255)

cell_size = 30
number_of_cells = 25

OFFSET = 75

class food:
  def __init__(self, snake_body):
    self.position = self.generate_random_pos(snake_body)

  def draw(self):
    food_rect = pygame.Rect(OFFSET + self.position.x * cell_size, OFFSET + self.position.y * cell_size, cell_size, cell_size )
    screen.blit(food_surface, food_rect)

  def generate_random_cell(self):
    x = random.randint(0, number_of_cells - 1) 
    y = random.randint(0, number_of_cells - 1) 
    return Vector2(x, y)

    
  def generate_random_pos(self, snake_body):
    
    position = self.generate_random_cell()

    while position in snake_body:
      position = self.generate_random_cell()

    return position

    
class snake:
  def __init__(self):
    self.body = [Vector2(6, 9), Vector2(5,9), Vector2(4,9)]
    self.direction = Vector2(1,0)
    self.next_direction = Vector2(1,0)
    self.add_segment = False
    self.eat_sound = pygame.mixer.Sound("sounds/eat.mp3")
    self.wall_sound = pygame.mixer.Sound("sounds/wall.mp3")
    
  def draw (self):
    for segment in self.body:
      segment_rect = pygame.Rect( OFFSET + segment.x * cell_size, + OFFSET + segment.y * cell_size, cell_size, cell_size)
      pygame.draw.rect(screen, SNAKE_COLOR, segment_rect,0,7)

  def update(self):
    self.direction = self.next_direction
    self.body.insert(0, self.body[0] + self.direction)
    if not self.add_segment:
     self.body.pop()
    else:
      self.add_segment = False
      
  def reset(self):
    self.body = [Vector2(6, 9), Vector2(5,9), Vector2(4,9)]
    self.direction = Vector2(1,0)

class Game:
  def __init__(self):
    self.snake = snake()
    self.food = food(self.snake.body)
    self.state = "RUNNING"
    self.score = 0
    

  def draw(self):
    self.snake.draw()
    self.food.draw()

  def update(self):
    if self.state == "RUNNING":
  
      self.snake.update()
      self.check_collision_with_food()
      self.chek_collision_whith_eddges()
      self.check_collision_with_tail()
    
    
  def check_collision_with_food(self):
    if self.snake.body[0] == self.food.position:
      self.food.position = self.food.generate_random_pos(self.snake.body)
      self.snake.add_segment = True
      self.score += 1
      
  def chek_collision_whith_eddges(self):
    if self.snake.body[0].x == number_of_cells or self.snake.body[0].x == -1:
      self.game_over()
    elif self.snake.body[0].y == number_of_cells or self.snake.body[0].y == -1:
      self.game_over()
      
  def game_over(self):
      self.snake.reset()
      self.food.position = self.food.generate_random_pos(self.snake.body)
      self.state = "STOPPED"
      self.score = 0
      self.snake.wall_sound.play()
      
  def check_collision_with_tail(self):
      headless_snake = self.snake.body[1:]
      if self.snake.body[0] in headless_snake:
        self.game_over()

screen = pygame.display.set_mode((2*OFFSET + cell_size * number_of_cells, 2*OFFSET + cell_size * number_of_cells))

food_surface = pygame.image.load("Graphics/pixil-frame-0.png")

pygame.display.set_caption("Retro Snake")

clock = pygame.time.Clock()

game = Game()

SNAKE_UPDATE = pygame.USEREVENT

pygame.time.set_timer(SNAKE_UPDATE, 150)

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
    if event.type == SNAKE_UPDATE:
      game.update()

    if event.type == pygame.KEYDOWN:
     if game.state == "STOPPED":
       game.state = "RUNNING"  
     if event.key == pygame.K_UP and game.snake.direction!= Vector2(0, 1):
       game.snake.next_direction = Vector2(0, -1)
     if event.key == pygame.K_DOWN and game.snake.direction!= Vector2(0, -1):
       game.snake.next_direction = Vector2(0, 1)
     if event.key == pygame.K_RIGHT and game.snake.direction!= Vector2(-1, 0):
       game.snake.next_direction = Vector2(1, 0)
     if event.key == pygame.K_LEFT and game.snake.direction!= Vector2(1, 0):
       game.snake.next_direction = Vector2(-1, 0)
     

 
  screen.fill(BG_COLOR)
  
  pygame.draw.rect(screen,
    SNAKE_COLOR,
    (OFFSET - 5, OFFSET - 5, cell_size * number_of_cells + 10, cell_size * number_of_cells + 10), 5
)
  tittle_surface = tittle_font.render("Retro Snake", True, SNAKE_COLOR)
  score_surface = score_font.render(str(game.score), True, SNAKE_COLOR)
  
  screen.blit(tittle_surface, (OFFSET - 5, 20))
  screen.blit(score_surface, (OFFSET + cell_size*number_of_cells + 10,OFFSET - 5))
  
  game.draw()
  
  pygame.display.update()
  clock.tick(60)
  