import pygame
import random #for getting foods at random position
import os


#initilizes py game module
x=pygame.init() #returns all the modules that are initilized
#print(x)

#initializes the music module
pygame.mixer.init()
#Just loades the music in the game file

#for movement of game according to frame
clock= pygame.time.Clock()

screen_width=900
screen_height=600

#display of pygame #Input in form of tuple hight and width
gameWindow = pygame.display.set_mode((screen_width,screen_height))

#colors
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue =  (0, 0, 255)
black = (0, 0, 0)

#title of game
pygame.display.set_caption("My Snake Game")



#just refreshing the game screen before getting into the game
pygame.display.update()

#gets default system font from the system
#55->Size of the font
font= pygame.font.SysFont(None,55)

#background image
bgimg = pygame.image.load("play.jpg")
wel = pygame.image.load("welcome.jpg")
out = pygame.image.load("out.png")
bgimg = pygame.transform.scale(bgimg,(screen_width, screen_height)).convert_alpha()
wel = pygame.transform.scale(wel,(screen_width, screen_height)).convert_alpha()
out = pygame.transform.scale(out,(screen_width, screen_height)).convert_alpha()
#gamewindow.blit(bgimg)

def text_screen(text, color, x, y):
    #parameter list of render fn(text,anti-alising,color)
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])

def plot_snake(gameWindow, color, snake_list, snake_size):
    for x,y in snake_list:
        pygame.draw.rect(gameWindow, color, (x, y, snake_size, snake_size))


def welcome():
    exit_game = False
    while not exit_game:
        #intro music
        #pygame.mixer.music.load('another.mp3')
        #this will make song to start to play
        #pygame.mixer.music.play()
        gameWindow.fill(white)
        gameWindow.blit(wel,(0,0))
        text_screen("Welcome to Snake Game", red, 200, 250)
        text_screen("Press Scape Bar to play", green, 210, 300)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('back.mp3')
                    #this will make song to start to play
                    pygame.mixer.music.play()
                    gameloop()
        pygame.display.update()
        clock.tick(60)


def gameloop():
    
    #just refreshing the game screen before getting into the game
    pygame.display.update()

    if( not os.path.exists("highscore.txt")):
        with open("highscore.txt","w") as f:
            f.write("0")
    with open("highscore.txt", "r") as f: #as f beacuse we don't need to close the file 
        highscore = f.read() #reads in form of string
        highscore = int(highscore)
        prevhs = highscore

    snake_x=45
    snake_y=55
    snake_size=10
    fps=60 #frames at which game sceen is updated

    velocity_x = 0
    velocity_y = 0

    #stores game score
    score = 0

    #game over variable
    game_over = False

    #By default set to false
    exit_game = False

    #Initial speed of the snake
    speed = 2

    food_x = random.randint(2,screen_width-10)
    food_y = random.randint(2,screen_height-10)
   

    snake_list=[]
    snake_length = 1

    #Caution: To make game fast put least as possble compuational stuff or works into the game loop
    while(not exit_game):
        # every events that u do is noticed
        # i.e.: every mouse move or keyboard click
        
        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))
            
            gameWindow.fill(white)
            #with open("highscorelist.txt", "a") as f:
            #    f.write("\n"+str(score))
            
            #text_screen("Game Over! Press Enter to Continue", red, screen_width//2 - 300, screen_height//2 - 100)
            gameWindow.blit(out, (0,0))
            if highscore > prevhs:
                text_screen("Snake Master!!  New High Score", green, screen_width//2 - 275, screen_height//2 - 50)

            for event in pygame.event.get():
                #This will make the game to terminate when closed 
                if event.type == pygame.QUIT:
                    exit_game=True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:

            for event in pygame.event.get():
                #print(event)
                
                #This will make the game to terminate when closed 
                if event.type == pygame.QUIT:
                    exit_game=True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        #snake_x += 5
                        velocity_x = speed
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        #snake_x -= 5
                        velocity_x = -speed
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        #snake_y -= 5
                        velocity_y = -speed
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        #snake_y += 5
                        velocity_y = speed
                        velocity_x = 0

                    #Cheatcode
                    if event.key == pygame.K_s:
                        score += 20

            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x - food_x)<9 and abs(snake_y - food_y)<9:
                score += 10
                #print(score)
                snake_length += 2
                
                food_x = random.randint(10,screen_width-20)
                food_y = random.randint(10,screen_height-20)
                speed += 0.5

            if score > highscore:
                highscore = score


            gameWindow.fill(white)
            gameWindow.blit(bgimg,(0,0))
            text_screen("Score: "+ str(score), blue, 5, 5)
            pygame.draw.rect(gameWindow, red, (food_x, food_y, snake_size, snake_size))

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            #controls the length of the sanke will increase in length if thesnake eats any food and will remove the head of the snake
            if len(snake_list) > snake_length:
                del snake_list[0]

            if head in snake_list[:-1]:
                game_over = True
                pygame.mixer.music.load('end.mp3')
                #this will make song to start to play
                pygame.mixer.music.play()

            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True
                #game over music
                pygame.mixer.music.load('end.mp3')
                #this will make song to start to play
                pygame.mixer.music.play()

            #pygame.draw.rect(gameWindow, black, (snake_x, snake_y, snake_size, snake_size))
            plot_snake(gameWindow, black, snake_list, snake_size)
        pygame.display.update()
        #updates according to frame
        clock.tick(fps)

    #whenever the game loop ends this will make the game to end 
    pygame.quit()
    quit()

welcome()
#gameloop()