import pygame.font
import requests
import pygame as pg
from random import randrange
import random
city = "umeå"


def get_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    if data["cod"] == 200:
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        print(f"Weather in {city}:")
        print(f"Description: {weather_description}")
        print(f"Temperature: {temperature}°C")
        print(f"Humidity: {humidity}%")
        print(f"Wind Speed: {wind_speed} m/s")
        return (weather_description, temperature)
    else:
        print("City not found.")


class food: #Class for food
    def _init_(self): #random food spawnpoint
        self.rectx = int(random.randint(0, WINDOW)/ TILE_SIZE) * TILE_SIZE
        self.recty = int(random.randint(0, WINDOW)/ TILE_SIZE) * TILE_SIZE
        self.rect = pygame.Rect(self.rectx, self.recty, TILE_SIZE, TILE_SIZE)


class powerApple(food): #arv
    def _init_(self):
        segments = [snake.copy()*2]

def runGame(description, temperature):
    print(description)
    print(temperature)


    WINDOW = 1000 #window size
    TILE_SIZE = 40 #Tile sizes on the screen
    RANGE = (TILE_SIZE // 4, WINDOW - TILE_SIZE // 4, TILE_SIZE)
    get_random_position = lambda: [randrange(*RANGE), randrange(*RANGE)] #function for position
    snake = pg.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2]) #Properties for snake
    snake.center = get_random_position() #random spawnpoint for snake
    length = 1 #For snake lenght
    segments = [snake.copy()] #Creates a copy of snace Rect
    snake_dir = (0, 0) #start direction
    time, time_step = 0, 110
    food = snake.copy() #action when food coolid with snake
    food.center = get_random_position() #food random spawnpoint
    screen = pg.display.set_mode([WINDOW] * 2)
    clock = pg.time.Clock() #time for framerate
    dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}

    #color values
    green = (0,255,0)
    blue = (0,0,128)
    pg.font.init()
    font = pg.font.SysFont('Comic Sans MS', 25, False, False) #font style + size
    text = font.render(description + ": In " + city + "    //  temp(C):" + str(temperature), True, green, blue) #description + temp output
    textRect = text.get_rect() #Text box
    textRect.center = (400, 200) #text position

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.KEYDOWN: #When w,a,s,d gets pressed, change direction
                if event.key == pg.K_w and dirs[pg.K_w]:
                    snake_dir = (0, -TILE_SIZE)
                    dirs = {pg.K_w: 1, pg.K_s: 0, pg.K_a: 1, pg.K_d: 1} #dirs = Set opposite key to 0, unavailable to self eat
                if event.key == pg.K_s and dirs[pg.K_s]:
                    snake_dir = (0, TILE_SIZE)
                    dirs = {pg.K_w: 0, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}
                if event.key == pg.K_a and dirs[pg.K_a]:
                    snake_dir = (-TILE_SIZE, 0)
                    dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 0}
                if event.key == pg.K_d and dirs[pg.K_d]:
                    snake_dir = (TILE_SIZE, 0)
                    dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 0, pg.K_d: 1}
        red = (int(temperature) * 5, 0,0) #Higher temperature means more redness multiplied with 5
        screen.fill(red)
        screen.blit(text, textRect)

        self_eating = pg.Rect.collidelist(snake, segments[:-1]) != -1 #if snake touches segment
        if snake.left < 0  or snake.right > WINDOW or snake.top < 0 or snake.bottom > WINDOW or self_eating: #if snake touches borders
            snake.center, food.center = get_random_position(), get_random_position()
            length, snake_dir = 1, (0,0)
            segments = [snake.copy()]

        if snake.center == food.center: #if food get touched, get new rand position + add lenght to snake
            food.center = get_random_position()
            length += 1
        pg.draw.rect(screen, 'blue', food)
        [pg.draw.rect(screen, 'green', segment) for segment in segments]
        time_now = pg.time.get_ticks()

        if time_now - time > time_step: # if game restart, remove
            time = time_now
            snake.move_ip(snake_dir)
            segments.append(snake.copy())
            segments = segments[-length:]
        pg.display.flip()
        clock.tick(60) #60 framerate




def main():
    api_key = "c6e5dc5cc0a5f052753064e213ec18db"
  # Replace this with your actual API key

    description, temperature = get_weather(city, api_key)
    runGame(description, temperature)



if __name__ == "__main__":
    main()
