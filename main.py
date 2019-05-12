import pygame
import random

screen_width = 500
screen_height = 500
wall = pygame.image.load('img/wall.png')
SCREEN = (screen_width, screen_height)
screen = pygame.display.set_mode(SCREEN)



width = 60
height = 62
speed = 7

walk_left = [pygame.image.load('img/gif04.png'),
              pygame.image.load('img/gif05.png'),
              pygame.image.load('img/gif06.png')]
walk_right = [pygame.image.load('img/gif01.png'),
              pygame.image.load('img/gif02.png'),
              pygame.image.load('img/gif03.png')]

static_img = pygame.image.load('img/gif04.png')
iceberg_img = [pygame.image.load('img/ice01.png'),
               pygame.image.load('img/ice02.png'),
               pygame.image.load('img/ice03.png')]
iceberg_options = [28, 410, 40, 430, 27, 410]

cloud_image = [pygame.image.load('img/cloud.png'),
               pygame.image.load('img/cloud2.png'),
               ]
scores = 0
above_iceberg = False  # проверка находимся ли мы над айсбергом или нет




class Object:
    def __init__(self, x, y, width, image, speed):
        self.x = x
        self.y = y
        self.width = width
        self.image = image
        self.speed = speed

    def move(self):
        if self.x >= -self.width:
            # pygame.draw.rect(screen, (224, 121, 147), (self.x, self.y, self.width, self.height))
            screen.blit(self.image, (self.x, self.y))
            self.x -= self.speed
            return True
        else:  # если айсберг вышел за границу дисплея
            self.x = screen_width + 100 + random.randrange(-80, 60)
            return False

    def return_iceberg(self, radius, y, width, image):
        self.x = radius
        self.y = y
        self.width = width
        self.image = image
        screen.blit(self.image, (self.x, self.y))


class Penguin():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.left = False
        self.right = False


    def Screen(self, display, walk_count = 0):


        display.blit(wall, (0, 0))  # вставляем фоновый рисунок
        write_text('Scores: ' + str(scores), 350, 10)
        if walk_count + 1 >= 30:  # будет 30 кадров в секунду (3 картинки по 10 кадров)
            walk_count = 0
        if self.left:
            display.blit(walk_right[walk_count // 10 != 0], (self.x, self.y))
            walk_count += 1
        elif self.right:
            display.blit(walk_left[walk_count // 10 != 0], (self.x, self.y))
            walk_count += 1
        else:
            display.blit(static_img, (self.x, self.y))
        pygame.display.update()  # обновляем окно

    ''' Проверка на столкновения с айсбергами '''

    def check_collision(self, barriers):
        for barrier in barriers:
            if self.y + height >= barrier.y:
                if barrier.x <= self.x <= barrier.x + barrier.width:
                    return True
                elif barrier.x <= self.x + width <= barrier.x + barrier.width:
                    return True
        return False


    def count_scores(self, barriers, jumpcount):
        global scores, above_iceberg
        if not above_iceberg:
            for barrier in barriers:
                if barrier.x <= self.x + width / 2 <= barrier.x + barrier.width:
                    if self.y + height - 5 <= barrier.y:
                        above_iceberg = True
                        break
        else:
            if jumpcount == -10:
                scores += 1
                above_iceberg = False


class Game():
    @staticmethod
    def game_over():
        stopped = True
        while stopped:
            for item in pygame.event.get():
                if item.type == pygame.QUIT:  # кнопка "закрыть" в окне
                    run = False

            write_text('Игра завершена.', 70, 200)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:  # клавиша энтер
                stopped = True
            if keys[pygame.K_ESCAPE]:
                stopped = False

            pygame.display.update()
            clock = pygame.time.Clock()
            clock.tick(15)

    @staticmethod
    def pause():
        paused = True

        pygame.mixer_music.pause()

        while paused:
            for item in pygame.event.get():
                if item.type == pygame.QUIT:  # кнопка "закрыть" в окне
                    run = False

            write_text('Пауза. Нажмите ENTER, чтобы продолжить.', 10, 200)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:  # клавиша энтер
                paused = False

            pygame.display.update()
            clock = pygame.time.Clock()
            clock.tick(15)
        pygame.mixer_music.unpause()


class Iceberg():
    def __init__(self):
        '''Добавляем айсберги'''
        self.iceberg_width = 20
        self.iceberg_height = 70
        self.iceberg_x = screen_width - 50
        self.iceberg_y = screen_height - 70

    @staticmethod
    def create_iceberg_arr(array):
        choice = random.randrange(0, 3)  # 3 не учитывается!
        img = iceberg_img[choice]
        width = iceberg_options[choice * 2]
        height = iceberg_options[choice * 2 + 1]
        array.append(Object(screen_width + 20, height, width, img, 4))

        choice = random.randrange(0, 3)  # 3 не учитывается!
        img = iceberg_img[choice]
        width = iceberg_options[choice * 2]
        height = iceberg_options[choice * 2 + 1]
        array.append(Object(screen_width + 300, height, width, img, 4))

        choice = random.randrange(0, 3)  # 3 не учитывается!
        img = iceberg_img[choice]
        width = iceberg_options[choice * 2]
        height = iceberg_options[choice * 2 + 1]
        array.append(Object(screen_width + 600, height, width, img, 4))


    '''Функция, для того чтобы айсберги точно можно было перепрыгнуть'''
    @staticmethod
    def find_radius(array):
        maximum = max(array[0].x, array[1].x, array[2].x)
        if maximum < screen_width:
            radius = screen_width
            if radius - maximum < 60:
                radius += 150
        else:
            radius = maximum

        choice = random.randrange(0, 5)
        if choice == 0:
            radius += random.randrange(10, 15)
        else:
            radius += random.randrange(200, 350)
        return radius

    @staticmethod
    def draw_array(array):
        for iceberg in array:
            check = iceberg.move()
            if not check:
                radius = Iceberg.find_radius(array)

                choice = random.randrange(0, 3)
                img = iceberg_img[choice]
                width = iceberg_options[choice * 2]
                height = iceberg_options[choice * 2 + 1]

                iceberg.return_iceberg(radius, height, width, img)

def open_random_objects():
    choice = random.randrange(0, 2)
    cloud_img = cloud_image[choice]

    cloud = Object(screen_width, screen_height + 80, 60, cloud_img, 2)
    return cloud

def move_objects(cloud):
    check = cloud.move()
    if not check:
        choice = random.randrange(0, 2)
        cloud_img = cloud_image[choice]
        cloud.return_iceberg(screen_width, random.randrange(10, 200), cloud.width, cloud_img)  # либо 10 пикселей ниже экрана, либо 200 пикселей выше

def write_text(message, x, y, font_color = (0, 0, 0), font_type='Albionic.ttf', font_size=20):  # x, y - координаты сообщения
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))

def main():
    Jump = False
    jumpCount = 10
    pygame.init()

    ''' Music '''
    pygame.mixer_music.load('sound.mp3')
    pygame.mixer_music.set_volume(0.3)  # 30 % от громкости
    pygame.mixer_music.play(-1)  # весь цикл играет музыка

    screen = pygame.display.set_mode(SCREEN)
    pygame.display.set_caption('Masha"s game')
    clock = pygame.time.Clock()

    d = Penguin(50, 425)

    ''' создаём массив для айсбергов '''
    iceberg_arr = []
    Iceberg.create_iceberg_arr(iceberg_arr)
    cloud = open_random_objects()

    run = True
    while run:
        clock.tick(40)
        # pygame.time.delay(40)  # цикл будет выполняться каждую 0.1 секунду
        for item in pygame.event.get():
            if item.type == pygame.QUIT:  # кнопка "закрыть" в окне
                run = False

        ''' Нажимаем на кнопку и удерживаем'''
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            Game.pause()
        if keys[pygame.K_LEFT] and d.x > 5:  # граница левая == 5
            d.x -= speed
            d.left = True
            d.right = False
        elif keys[pygame.K_RIGHT] and d.x < 500 - width - 5:
            d.x += speed
            d.right = True
            d.left = False
        else:
            d.left = False
            d.right = False
            d.walk_count = 0

        if not(Jump):  # во время прыжка мы не можем перемещать объект вверх и вниз
            if keys[pygame.K_SPACE]:
                Jump = True
        else:
            if jumpCount >= -10:
                if jumpCount < 0:
                    d.y += (jumpCount ** 2) / 2
                else:
                    d.y -= (jumpCount ** 2) / 2  # прыжок
                jumpCount -= 1
            else:
                Jump = False
                jumpCount = 10

        d.count_scores(iceberg_arr, jumpCount)
        d.Screen(screen)
        move_objects(cloud)
        Iceberg.draw_array(iceberg_arr)

        if d.check_collision(iceberg_arr):
            pygame.mixer_music.stop()
            run = False

        pygame.display.update()
    return Game.game_over()

if __name__ == "__main__":
    main()

while main():
    pass
pygame.quit()