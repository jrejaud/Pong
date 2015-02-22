#!/usr/bin/env python

"""
Battle Pong
Written by Jordan Rejaud
Version 1.0
Controls: Q/A - Left Paddle
O/L - Right Paddle
"""

#Import Game Class
import pygame, os, random, time
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'


#Next update:
#Add Sounds
#Add Powerups
#Change speed of ball based on speed of paddle?

#Declare Universal Colors
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

class program(object):   
    def __init__(self):
        pygame.init()
        self.ScreenSize = (1000,750)
        self.screen = pygame.display.set_mode(self.ScreenSize)
        self.background = pygame.Surface(self.screen.get_size())
        self.clock = pygame.time.Clock()
        self.ScreenCaption = "Battle Pong"
        pygame.display.set_caption(self.ScreenCaption)     
    
class pong(program):
    def __init__(self):
        super(pong,self).__init__()
    #Declare Variables
        self.width = self.background.get_width()
        self.height = self.background.get_height()
        self.wall_height = self.height*0.0325
        self.center_line_size = self.height/50
        self.center_line_x = self.width/2 - self.center_line_size/2
        self.starting_center_line_y = self.center_line_size + self.wall_height
        self.center_line_offset = 2*self.center_line_size
        self.number_center_line = 23 #Number of individual elements in center line
        
    def Create_Background(self):
    #Printbackground
        self.background.fill(black)
    #Create Center Line
        for i in range(self.number_center_line):
            self.center_line = pygame.draw.rect(self.background,white,(self.center_line_x,self.starting_center_line_y+self.center_line_offset*i,self.center_line_size,self.center_line_size))
        self.screen.blit(self.background, (0, 0))

class GameSprite(object):
    def __init__(self):
    #Universal Variables for all game sprites
        self.height = pygame.display.get_surface().get_height()
        self.width = pygame.display.get_surface().get_width()
    #Load Sounds
        self.PongSound = self.LoadSound("Pong.wav")
        self.PingSound = self.LoadSound("Ping.wav")
        self.DingSound = self.LoadSound("Ding.wav")
        self.YouLoseSound = self.LoadSound("You_Lose.wav")
    
    #Load Sound (Blatantly stolen from chimp tutorial)
    def LoadSound(self, name):
        class NoneSound:
            def play(self): pass
        if not pygame.mixer: return NoneSound()
        file_name = os.path.join('data', name)
        try:
            sound = pygame.mixer.Sound(file_name)
        except pygame.error, message:
            print "Cannot find sound file: ", file_name
            raise SystemExit, message
        return sound 
       
class Wall_Class(GameSprite,pygame.sprite.Sprite):
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        super(Wall_Class,self).__init__()
        self.wall_height = self.height*0.0325
        self.wall_offset = self.height/50
    #Draw Image    
        self.image = pygame.Surface((self.width,self.wall_height))
    #Fill Image
        self.image.fill(white)
    #Place Image
        self.rect = self.image.get_rect()
        self.rect.left = 0
        if location == "top": self.rect.top = self.wall_offset
        if location == "bot": self.rect.top = self.height-self.wall_offset-self.wall_height      

class Paddle_Class(GameSprite, pygame.sprite.Sprite):
#Constructor, pass the player number and the window size
    def __init__(self,player_number):
      pygame.sprite.Sprite.__init__(self)
      super(Paddle_Class,self).__init__()
      self.PaddleHeight = .0875*self.height
      self.PaddleWidth = .017*self.width
      self.stepsize = 30
    #Draw image (A rectangle!)
      self.image = pygame.Surface((self.PaddleWidth,self.PaddleHeight))
    #Fill image
      self.image.fill(white)
    #Get Initial Rect calue
      self.rect = self.image.get_rect()
    #Position image
      if player_number == 0:
        self.rect.left = .051*self.width
        self.rect.top = self.height/2 - self.PaddleHeight/2
      elif player_number == 1:
        self.rect.left = self.width-.051*self.width-self.PaddleWidth
        self.rect.top = self.height/2 - self.PaddleHeight/2
    
    def move(self,direction):
        if direction == "up": self.rect.move_ip((0, -self.stepsize))
        if direction == "down": self.rect.move_ip((0, self.stepsize))

    def update(self, Walls):
        for wall in Walls:
        #If Paddle hits a wall
            if self.rect.colliderect(wall.rect) == 1:
            #If it is the top wall
                if self.rect.top < self.height/2: self.move("down")
            #If it is the bot wall
                if self.rect.top > self.height/2: self.move("up")
                
class Ball_Class(GameSprite, pygame.sprite.Sprite):
    def __init__(self):
      pygame.sprite.Sprite.__init__(self)
      super(Ball_Class,self).__init__()
    #Temporary LastPaddle set  
      self.LastPaddle = 0
      self.BallSize = .017*self.width
      self.image = pygame.Surface((self.BallSize,self.BallSize))
      self.image.fill(white)
      self.rect = self.image.get_rect()
      self.rect.left = self.width / 3
      self.rect.top = self.height / 3
    #Initial displacement
      self.x_displacement = 15
      self.y_displacement = 15
    
    def update(self, Walls, Paddles):
    #Move ball up/down
        self.rect.y -= self.y_displacement
    #Move the ball left/right
        self.rect.x += self.x_displacement
    #Check if ball hits a wall
        for wall in Walls:
            if self.rect.colliderect(wall.rect) == 1:
                self.DingSound.play()
                self.y_displacement = - self.y_displacement
    #Check if ball hits a paddle
        for paddle in Paddles:
            if self.rect.colliderect(paddle.rect) == 1:
                self.PingSound.play()
                if self.x_displacement > 0:
                    self.x_displacement += 1
                    self.LastPaddle = 1
                elif self.x_displacement < 0:
                    self.x_displacement += - 1
                    self.LastPaddle = 0
                self.x_displacement = -self.x_displacement       
    #Check if ball went out left side
        if (self.rect.left <= 0) or (self.rect.right >= self.width):
            self.YouLoseSound.play()
            time.sleep(3)
            pygame.quit()

class PowerUpClass(GameSprite, pygame.sprite.Sprite):
    def __init__(self):
      pygame.sprite.Sprite.__init__(self)
      super(PowerUpClass,self).__init__()
    #Make Powerup twice as large as a ball
      self.Size = 5*(.017*self.width)
      self.image = pygame.Surface((self.Size,self.Size))
      self.image.fill(white)
      self.rect = self.image.get_rect()
      self.rect.left  = random.randint(self.width/4, self.width - self.width/4)
      self.rect.top = random.randint(self.height/4, self.height - self.height/4)
    #Pick an ability
      self.abilities = ['Big Paddle', 'Reverse']
      self.ability = random.choice(self.abilities)
      self.ability = 'Big Paddle'
    
    def AbilitiesFunction(self, ball, PaddleList):
        if self.ability == "Big Paddle":
            NewHeight = 1.5 * PaddleList[ball.LastPaddle].PaddleHeight
            OldX = PaddleList[ball.LastPaddle].rect.left
            OldY = PaddleList[ball.LastPaddle].rect.top
            PaddleList[ball.LastPaddle].image = pygame.Surface((PaddleList[ball.LastPaddle].PaddleWidth,1.5 * PaddleList[ball.LastPaddle].PaddleHeight))
            PaddleList[ball.LastPaddle].image.fill(white)
            PaddleList[ball.LastPaddle].rect = self.image.get_rect()
            PaddleList[ball.LastPaddle].rect.left = OldX
            PaddleList[ball.LastPaddle].rect.left = OldY
        elif self.ability == "Reverse":
            print(PaddleList[ball.LastPaddle])

    def update(self, Balls, PaddleList):
        for ball in Balls:
        #See if a ball hits the powerup    
            if self.rect.colliderect(ball.rect) == 1:
                self.kill()
                self.AbilitiesFunction(ball, PaddleList)
                      
def Print_Title(title):
    font = pygame.font.Font(None,36)
    text = font.render(title,1,(10,10,10))
    textpos = text.get_rect(centerx=background.get_width()/2)
    background.blit(text,textpos)
   
def main():
#Initialize and Program Parameters
    Pong = pong()
    Pong.Create_Background()
    
#Build Paddles
    Paddle_0 = Paddle_Class(player_number = 0)
    Paddle_1 = Paddle_Class(player_number = 1)
    
#Build Walls
    top_wall = Wall_Class(location = "top")
    bot_wall = Wall_Class(location = "bot")

#Build Ball
    Ball = Ball_Class()
    
#Build Powerup (Temporary)
    #PowerUp = PowerUpClass()

#Sprite List
    PaddleList = [Paddle_0, Paddle_1]
    WallList = [top_wall, bot_wall]
    BallList = [Ball]
    #PowerUpList = [PowerUp]

#Sprite Groups
    Paddles = pygame.sprite.RenderPlain(PaddleList)
    Walls = pygame.sprite.RenderPlain(WallList)
    Balls = pygame.sprite.RenderPlain(BallList)
    #PowerUps = pygame.sprite.RenderPlain(PowerUpList)
    AllSprites = pygame.sprite.RenderPlain(Paddles, Walls, Balls)
    #AllSprites = pygame.sprite.RenderPlain(Paddles, Walls, Balls, PowerUps)

#Redraw entire display    
    pygame.display.flip()
    
    while 1:
    #Set Clock to run at no more than 20fps
        Pong.clock.tick(20)
    
    #Read what keys are pressed and move paddles accordingly
        keys = pygame.key.get_pressed()
        if keys[K_q]:
            Paddle_0.move("up")
        if keys[K_a]:
            Paddle_0.move("down")
        if keys[K_o]:
            Paddle_1.move("up")
        if keys[K_l]:
            Paddle_1.move("down")           
    
    #Generate PowerUps
        # Timer Check or random: should I summon a power up
        # PowerUp = PowerUpClass()
            # Places a powerup on the game grid
            # Picks a powerup "time"
        # Add powerup to "Powerups" sprite list
        # Add powerup to Allsprites list 
    
    #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                return     

    #Clear and refresh screen
        AllSprites.clear(Pong.screen, Pong.background)
        Paddles.update(Walls)
        Balls.update(Walls, Paddles)
        #PowerUps.update(Balls, PaddleList)
        AllSprites.draw(Pong.screen)
        pygame.display.flip()
                
#Calls the main function when this line is executed
if __name__ == '__main__': main()
