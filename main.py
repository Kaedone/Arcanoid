# Подключаем графическую библиотеку
from tkinter import *
# Подключаем модули, которые отвечают за время и случайные числа
import time
import random

# Создаём новый объект — окно с игровым полем.
tk = Tk()
# Делаем заголовок окна — Games (с помощью свойства объекта title)
tk.title('Arcanoid')
# Запрещаем менять размеры окна
tk.resizable(0, 0)
# Помещаем наше игровое окно выше остальных окон на компьютере, чтобы другие окна не могли его заслонить
tk.wm_attributes('-topmost', 1)
# Создаём новый холст, где и будем рисовать игру
canvas = Canvas(tk, width=500, height=400, highlightthickness=0)
# Говорим холсту, что у каждого видимого элемента будут свои отдельные координаты
canvas.pack()
# Обновляем окно с холстом
tk.update()


# Описание класса Ball
class Ball:
    """Отвечает за шарик: задание начального положения и направления движения, касания платформы, само-отрисовка"""

    # Конструктор
    def __init__(self, game_field, paddle, score, color):
        # Задаём параметры объекта
        self.canvas = game_field
        self.paddle = paddle
        self.score = score

        self.id = game_field.create_oval(10, 10, 25, 25, fill=color)
        # Помещаем шарик в "стартовое" положение (245,100)
        self.canvas.move(self.id, 245, 100)
        # Все возможные для старта направления
        starts = [-2, -1, 1, 2]
        # Перемешиваем и выбираем 1 из предложенных, будующий вектор движения
        random.shuffle(starts)
        self.x = starts[0]
        # Вначале он всегда падает
        self.y = -2
        # Определяем высоту и ширину
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        # Определяем выпал ли он за границы мира
        self.hit_bottom = False

    # Обработка касания платформы (4 координаты в переменной pos)
    # (левая верхняя и правая нижняя точки)
    def hit_paddle(self, pos):
        # Получение координат платформы через объект paddle
        paddle_pos = self.canvas.coords(self.paddle.id)
        # Когда координаты касания совпадают с координатами платформы (шарик упал на неё)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if paddle_pos[1] <= pos[3] <= paddle_pos[3]:
                # Счётчик + 1 (обработчик этого события будет описан ниже)
                self.score.hit()
                # Возвращаем метку касания
                return True
        # Иначе говорим что касания небыло (шарик недолетел либо выпал)
        return False

    # Отрисовка шарика
    def draw(self):
        # Перемещение шарика на данные координаты заданные координаты x и y
        self.canvas.move(self.id, self.x, self.y)
        # Сохраняем новые координаты шарика
        pos = self.canvas.coords(self.id)
        # Если шарик падает сверху
        if pos[1] <= 0:
            # Задаём падение на следующем шаге = 2 (ускоряем)
            self.y = 2
        # Если шарик правым нижним углом коснулся дна (выпал)
        if pos[3] >= self.canvas_height:
            # Помечаем это в отдельной переменной
            self.hit_bottom = True
            # Выводим сообщение и количество очков
            canvas.create_text(250, 120, text='Вы проиграли', font=('Courier', 30), fill='red')
        # Если шарик коснулся платформы (отскочил)
        if self.hit_paddle(pos):
            # Отправляем шарик наверх
            self.y = -2
        # Если коснулся левой стенки
        if pos[0] <= 0:
            # Движем его вправо
            self.x = 2
        # Если коснулся правой стенки
        if pos[2] >= self.canvas_width:
            # Движем его влево
            self.x = -2


#  Описание класса Paddle (отрисовка платформы)
class Paddle:
    # Конструктор
    def __init__(self, game_field, color):
        # Платформа рисуется на том же самом холсте
        self.canvas = game_field
        # Создаем платформу и получаем её внутреннее имя
        self.id = game_field.create_rectangle(0, 0, 100, 10, fill=color)
        # Все возможные стартовые положения платформы
        start_1 = [40, 60, 90, 120, 150, 180, 200]
        # Случайная стартовая точка для платформы
        self.starting_point_x = random.choice(start_1)
        # Ставим платформу на старт
        self.canvas.move(self.id, self.starting_point_x, 300)
        # Платформа стоит
        self.x = 0
        # Узнаём ширину
        self.canvas_width = self.canvas.winfo_width()
        # Обработчик нажатий:
        # Метод turn_right() если нажата стрелка вправо
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        # Метод turn_left() если стрелка влево
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        # Ожидание начала игры
        self.started = False
        # Запускаем игру, как только нажат энтер
        self.canvas.bind_all('<KeyPress-Return>', self.start_game)

    # Движение вправо
    def turn_right(self, event):
        # Минимальное смещение, на 1 пиксель по оси x
        self.x = 5

    # Движение влево
    def turn_left(self, event):
        # Минимальное смещение, на 1 пиксель по оси x
        self.x = -5

    # Начало игры
    def start_game(self, event):
        # Запуск
        self.started = True

    # Движение платформы
    def draw(self):
        # Сдвигаем платформу на заданное количество пикселей (1 пиксель)
        self.canvas.move(self.id, self.x, 0)
        # Координаты холста
        pos = self.canvas.coords(self.id)
        # Что-бы не врезаться в границу (в левую)
        if pos[0] <= 0:
            # Остановка (не выезжаем за край)
            self.x = 0
        # Что-бы не врезаться в границы (в правую)
        elif pos[2] >= self.canvas_width:
            # Остановка (не выезжаем за край)
            self.x = 0


#  Описание класса Score (Отображение и работа счётчика)
class Score:
    # Конструктор
    def __init__(self, game_field, color):
        # Изначальное значение счетчика (0)
        self.score = 0
        # Использование ужего соданного холста
        self.canvas = game_field
        # Создаём надпись, которая показывает текущий счёт, делаем её нужно цвета
        # и запоминаем её внутреннее имя
        self.id = game_field.create_text(450, 10, text=self.score, font=('Times New Roman', 15), fill=color)

    # Обработка касаний платформы
    def hit(self):
        # Увелечение счета
        self.score += 1
        # Обновление счета
        self.canvas.itemconfig(self.id, text=self.score)


# Создание объекта — зелёный счёт
score = Score(canvas, 'green')
# Создание платформы
paddle = Paddle(canvas, 'White')
# Создание шарика
ball = Ball(canvas, paddle, score, 'red')
# Ждём, пока шарик не вывалится
while not ball.hit_bottom:
    # Когда игра началась, разрешаем платформе начать передвижение
    if paddle.started:
        # Двигаем шарик
        ball.draw()
        # Двигаем платформу
        paddle.draw()
    # Обновляем игровое поле, для отрисовки
    tk.update_idletasks()
    # Обновляем ещё раз
    tk.update()
    # Делаем микро паузу, для плавности
    time.sleep(0.01)
# Если программа дошла досюда то, значит что шарик коснулся дна.
# Ждём 3 секунды, что-бы игрок прочитал финальную надпись, и завершаем игру
time.sleep(3)

