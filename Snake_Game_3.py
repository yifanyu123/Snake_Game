from tkinter import *
from tkinter import font
from tkinter import ttk
import random
import pygame
class Score:
    def __init__(self,snake):
        self.snakelength=snake.length
    def render(self,canvas):
        canvas.create_rectangle(660,540,720,580,fill="#FF6464",outline="")
        canvas.create_text(690,560,text="Score",font="Courier 15 bold",fill="#4AA6B5")
        canvas.create_text(740,560,text=str(self.snakelength),font="Courier 15 bold", fill="#D6C481")
    def update(self,snake):
        self.snakelength=snake.length
class Food:
    # Try to implement this in OOP way
    def __init__(self, width, height):
        self.x = random.randrange(width*0.8)
        self.y = random.randrange(height*0.8)
        self.color = random.choice(["#FC624D", "#FCA7A7", "#18587A","#BC5148","#7BCECC","#8D6262","#F5C8BD","#FFE3B0","#096C47", "#A9ECA2"])
        self.shape=random.choice(["rectangle","oval"])

    def render(self, canvas, size):
        if self.shape=="rectangle":
            canvas.create_rectangle(self.x * size, self.y * size, (self.x + 1) * size, (self.y + 1) * size, fill=self.color, outline="")
        if self.shape=="oval":
            canvas.create_oval(self.x * size, self.y * size, (self.x + 1) * size, (self.y + 1) * size, fill=self.color, outline="")

class Snake:

    def __init__(self):
        self.body = [[0, 0], [0, 1], [0, 2], [0, 3]]
        self.bodycolor=["#FC624D", "#FCA7A7", "#18587A","#BC5148"]
        self.tail = None
        self.direction = "Right"
        self.length = len(self.body)
        

    def turn(self, d):
        if d == "Right" and self.direction != "Left":
            self.direction = d
        if d == "Left" and self.direction != "Right":
            self.direction = d
        if d == "Up" and self.direction != "Down":
            self.direction = d
        if d == "Down" and self.direction != "Up":
            self.direction = d

    def move(self):
        (x, y) = self.body[-1]
        if self.direction == "Right":
            self.body += [[x+1, y]]
        elif self.direction == "Left":
            self.body += [[x-1, y]]
        elif self.direction == "Up":
            self.body += [[x, y-1]]
        elif self.direction == "Down":
            self.body += [[x, y+1]]
        self.tail = self.body[0]
        del self.body[0]

    def grow(self,foodcolor):
        self.body.insert(0, self.tail)
        self.length+=1
        self.bodycolor.insert(0,foodcolor)

    def render(self, canvas, size,food):
        i=0
        for (x, y) in self.body:
            canvas.create_rectangle(x * size, y * size, (x + 1)*size, (y+1)*size, fill=self.bodycolor[i], outline="")
            i+=1
class SnakeGame:

    class State:
        RUNNING = 0
        GAMEOVER = 1
        REOPEN=-1
    
    # Constructor
    def __init__(self):
        print("Snake initialing")
        self.frame = Tk()
        self.width = 40
        self.height = 30
        self.size = 20
        self.canvas = Canvas(self.frame, width = self.width * self.size, height = self.height * self.size, bg="#FFFCEF")
        self.canvas.pack()
        
        self.frame.bind("<KeyPress>", self.keyboard_even_hanlder)
        self.frame.bind("<Button-1>",self.mouse_even_handler)
        # Game entities:
        self.snake = Snake()
        self.food = Food(self.width, self.height)
        self.score=Score(self.snake)
        # Game Status:
        self.state = self.State.REOPEN
        # Game Effects:
        pygame.mixer.init()
        self.sound_eat = pygame.mixer.Sound("./eat.wav")
        self.sound_over = pygame.mixer.Sound("./over.wav")

    #keyboard and mouse handler
    def keyboard_even_hanlder(self, event):
        if self.state == self.State.RUNNING:
            if event.keysym in ["Up", "Down", "Left", "Right"]:
                self.snake.turn(event.keysym)

        if self.state == self.State.GAMEOVER:
            if event.keysym == 'Return':
                self.snake = Snake()
                self.food = Food(self.width, self.height)
                self.state = self.State.RUNNING
    def mouse_even_handler(self,event):
        if self.state == self.State.REOPEN:
            if (event.x>=350 and event.x<=450) and (event.y>=300 and event.y<=350):
                self.state=self.State.RUNNING
            if (event.x>=350 and event.x<=450) and (event.y>=360 and event.y<=410):
                self.frame.destroy()

        if self.state == self.State.GAMEOVER:
            if (event.x>=350 and event.x<=450) and (event.y>=300 and event.y<=350):
                self.restart()
                self.state=self.State.RUNNING
            if (event.x>=350 and event.x<=450) and (event.y>=360 and event.y<=410):
                self.restart()
                self.state=self.State.REOPEN
            if (event.x>=350 and event.x<=450) and (event.y>=420 and event.y<=470):
                self.frame.destroy()

    #Main loop and data / graphic layer
    def gameLoop(self):
        self.update()   # This is the data layer
        self.render()   # This is the graphic layer
        self.frame.after(100, self.gameLoop)

    def update(self):
        if self.state == self.State.RUNNING:
            self.snake.move()
            self.score.update(self.snake)
            # Check if you eat the food.
            if self.snake.body[-1] == [self.food.x, self.food.y]:
                self.sound_eat.play()
                self.snake.grow(self.food.color)
                del self.food
                self.food = Food(self.width, self.height)

            if self.isOver():
                self.sound_over.play()
                del self.food
                del self.snake
                self.state = self.State.GAMEOVER
                
    def render(self):
        if self.state==self.State.REOPEN:
            self.StartWindow()          
        if self.state == self.State.RUNNING:
            self.RunningWindow()
        if self.state == self.State.GAMEOVER:
            self.GameOverWindow()
    
    #3 Major interface
    def RunningWindow(self):
        self.canvas.delete(ALL)
        self.snake.render(self.canvas, self.size,self.food)
        self.food.render(self.canvas, self.size)
        self.score.render(self.canvas)
    
    def GameOverWindow(self):
        self.canvas.delete(ALL)
        self.canvas.create_text(400, 200, text="GAME OVER", fill="#24BDDF", font="Helvetica 45 bold")
        #Resart Button
        self.canvas.create_rectangle(350,300,450,350,fill="#404969",activefill="#FFCD00",outline="")
        self.canvas.create_text(400,325,text="Restart",fill="#DC552C",activefill="#FFCD00", font="Times 15 bold underline")
        
        #Backto MainMenu Button
        self.canvas.create_rectangle(350,360,450,410,fill="#404969",activefill="#FFCD00",outline="")
        self.canvas.create_text(400,385,text="MainMenu",fill="#DC552C",activefill="#FFCD00",font="Times 15 bold underline")

        #Exit Button
        self.canvas.create_rectangle(350,420,450,470,fill="#404969",activefill="#FFCD00",outline="")
        self.canvas.create_text(400,445,text="Exit",fill="#DC552C",activefill="#FFCD00",font="Times 15 bold underline")


    def  StartWindow(self):
        self.canvas.delete(ALL)
        self.canvas.create_text(400,200,text="SNAKE GAME", fill="#48BA95",font="Helvetica 45 bold")    
        
        #Start Button
        self.canvas.create_rectangle(350,300,450,350,fill="#404969",activefill="#FFCD00",outline="")
        self.canvas.create_text(400,325, text="Start", fill="#DC552C",activefill="#FFCD00", font="Times 25 bold underline")
        
        #Exit Button
        self.canvas.create_rectangle(350,360,450,410,fill="#404969",activefill="#FFCD00",outline="")
        self.canvas.create_text(400,385,text="Exit",fill="#DC552C",activefill="#FFCD00",font="Times 25 bold underline")
        
        #@YYF
        self.canvas.create_text(60,560,text="@YYF",font="Helvetica 25 bold italic",fill="#FFCD19")

       
	# For checking game status
    def isOver(self):
        head = self.snake.body[-1]
        # Check boundary
        if head[0] > self.width or head[0] < 0:
            return True
        if head[1] > self.height or head[1] < 0:
            return True
        # Check eat body
        if head in self.snake.body[:-1]:
            return True

    #For changing game status
    def restart(self):
        self.snake=Snake()
        self.food=Food(self.width,self.height)


g = SnakeGame()
g.gameLoop()
g.frame.mainloop()
