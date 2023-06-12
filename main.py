import turtle
import random
import tkinter as tk
import time

def exit_app():
    menu.destroy()
    turtle.bye()

# уровень легко
def game_level_1_start():
    menu.withdraw()
    screen = turtle.Screen()
    screen.tracer(9)
    game_start()

# уровень сложно
def game_level_2_start():
    menu.withdraw()
    screen = turtle.Screen()
    screen.tracer(12)
    game_start()
# уровень невозможно
def game_level_3_start():
    menu.withdraw()
    screen = turtle.Screen()
    screen.tracer(18)
    game_start()

# функция запуска игры
def game_start():
    global bulletstate
    bulletstate = "ready"
    # создание экрана turtle
    screen = turtle.Screen()
    screen.title("Space Invaders")
    screen.setup(width=665, height=775)
    window = screen.getcanvas().winfo_toplevel()
    window.wm_attributes('-fullscreen', False)
    window.wm_maxsize(665, 775)
    window.wm_minsize(665, 775)
    screen.bgpic("back_graund.gif")

    # модель игрока и противника
    turtle.register_shape("invader.gif")
    turtle.register_shape("player.gif")

    # Игрок
    player = turtle.Turtle()
    player.shape("player.gif")
    player.penup()
    player.speed(0)
    player.goto(0, -250)
    player.setheading(90)
    player.speed = 0

    # количество противников
    number_of_enemies = 10
    enemies = []

    # добавление противников на игровое поле
    for i in range(number_of_enemies):
        enemies.append(turtle.Turtle())

    for enemy in enemies:
        enemy.shape("invader.gif")
        enemy.penup()
        enemy.speed(0)
        x = random.randint(-200, 200)
        y = random.randint(100, 250)
        enemy.goto(x, y)

    enemyspeed = 0.1

    # счетчик
    score = 0
    score_pen = turtle.Turtle()
    score_pen.speed(0)
    score_pen.color("white")
    score_pen.penup()
    score_pen.goto(-285, 275)
    score_pen.hideturtle()

    # пуля
    bullet = turtle.Turtle()
    bullet.color("yellow")
    bullet.shape("triangle")
    bullet.penup()
    bullet.speed(0)
    bullet.setheading(90)
    bullet.shapesize(0.5, 0.5)
    bullet.hideturtle()

    bulletspeed = 2

    # ready - исходное положение
    # fire - пуля стреляет

    def fire_bullet():
        global bulletstate
        if bulletstate == "ready":
            bulletstate = "fire"
            x = player.xcor()
            y = player.ycor() + 10
            bullet.goto(x, y)
            bullet.showturtle()

    # передвижение
    def move_left():
        player.speed = -0.5

    def move_right():
        player.speed = 0.5

    def move_player():
        x = player.xcor()
        x += player.speed
        if x < -280:
            x = - 280
        if x > 280:
            x = 280
        player.setx(x)

    # Проверка на столкновение противника и пули
    def isCollision(t1, t2):
        distance = ((t1.xcor() - t2.xcor()) ** 2 + (t1.ycor() - t2.ycor()) ** 2) ** 0.5
        if distance < 15:
            return True
        else:
            return False

    # назначение клаиш
    turtle.listen()
    turtle.onkey(move_left, "Left")
    turtle.onkey(move_right, "Right")
    turtle.onkey(fire_bullet, "space")

    # главный блок кодда
    while True:
        # перемещение игрока
        move_player()
        # перемещение противников
        for enemy in enemies:
            x = enemy.xcor() + enemyspeed
            enemy.setx(x)

            if enemy.xcor() > 280:
                for e in enemies:
                    y = e.ycor()
                    y -= 40
                    e.sety(y)
                enemyspeed *= -1

            if enemy.xcor() < -280:
                for e in enemies:
                    y = e.ycor()
                    y -= 40
                    e.sety(y)
                enemyspeed *= -1

            # Проверка, есть ли столкновение с пулей
            if isCollision(bullet, enemy):
                # сбросить пулю
                bullet.hideturtle()
                bulletstate = "ready"
                bullet.setposition(0, -400)

                # Сбросить врага
                x = random.randint(-200, 200)
                y = random.randint(100, 250)
                enemy.setposition(x, y)

                # Отображение счета
                score += 10
                scorestring = "счет: %s" % score
                score_pen.clear()
                score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))

            # проигрыш при столкновение с противником
            if isCollision(player, enemy):
                player.hideturtle()
                enemy.hideturtle()
                time.sleep(1)
                screen.clear()
                lose_game()
                menu.mainloop()
                break
            # проигрыш при достижение противником нижней части экрана
            if enemy.ycor() < -250:
                player.hideturtle()
                enemy.hideturtle()
                time.sleep(1)
                screen.clear()
                lose_game()
                menu.mainloop()
                break

        # выстрел пули
        if bulletstate == "fire":
            y = bullet.ycor()
            y += bulletspeed
            bullet.sety(y)

        # перезарядка оружия при промохе
        if bullet.ycor() > 275:
            bullet.hideturtle()
            bulletstate = "ready"

# создание меню
# созднаие основного окна tkinter
menu = tk.Tk()
menu.title("Space Invaders")
menu.resizable(False, False)  # запрет масштабирования окна
# Определить размеры окна
window_width = 670
window_height = 800

# Определить размеры экрана
screen_width = menu.winfo_screenwidth()
screen_height = menu.winfo_screenheight()

# Рассчитать координаты центра экрана
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

# Установить центрированное окно
menu.geometry("{}x{}+{}+{}".format(window_width, window_height, x, y))

# добавляем изображение на фон
bgimage = tk.PhotoImage(file="back_graund.gif")
backgroundlabel = tk.Label(menu, image=bgimage)
backgroundlabel.place(x=0, y=0, relwidth=1, relheight=1)

# Функция для открытия инструкции
def open_instructions():
    # Удаляем все виджеты в главном окне
    for widget in menu.winfo_children():
        widget.destroy()

    image = tk.PhotoImage(file='back_graund.gif')
    canvas = tk.Canvas(menu, width=image.width(), height=image.height(), highlightthickness=0)
    canvas.pack(fill='both', expand=True)
    canvas.image = image
    bg = canvas.create_image(0, 0, anchor="nw", image=canvas.image)

    # Создание текстового диапазона
    text_frame = tk.Frame(menu)
    text_frame.place(relx=0.5, rely=0.5, relwidth=0.85, relheight=0.5, anchor=tk.CENTER)

    # Создание текста правил игры
    rules_text = """    Главная задача игрока — это управление космическим кораблем, расположенным внизу экрана, в верхней
части экрана будут появляться противники, которых игрок должен не подпустить к нижней части экрана, в случае
если противники доберутся до нижней части экрана, то
игра заканчивается, а игрок считается проигравшим."""

    # Создание метки для текста правил игры и размещение ее в текстовом диапазоне
    rules_label = tk.Label(text_frame, text=rules_text, font=("Arial", 14), justify="left",
                           wraplength=562, bg='black', fg='white')
    rules_label.pack(fill="both", expand=True)

    # Создание кнопки "В главное меню"
    rules_button = tk.Button(menu, text="В меню", font=("Arial", 24), width=20, height=1, command=main_menu, bg='#D19C58')
    rules_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)  # центрирование кнопки по горизонтали и вертикали


# Создание кнопки "Инструкция"
rules_button = tk.Button(menu, text="Правила", font=("Arial", 24), width=20, height=1, command=open_instructions, bg='#D19C58')
rules_button.place(relx=0.5, rely=0.55, anchor=tk.CENTER)  # центрирование кнопки по горизонтали и вертикали

# Создание кнопки "Выход"
exit_button = tk.Button(menu, text="Выход", font=("Arial", 24), width=20, height=1, command=exit_app, bg='#D19C58')
exit_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)  # центрирование кнопки по горизонтали и вертикали

def open_game_menu():
    # Удаляем все виджеты в главном окне
    for widget in menu.winfo_children():
        widget.destroy()

    # Создание уровней сложности
    image = tk.PhotoImage(file='back_graund.gif')
    canvas = tk.Canvas(menu, width=image.width(), height=image.height(), highlightthickness=0)
    canvas.pack(fill='both', expand=True)
    canvas.image = image
    bg = canvas.create_image(0, 0, anchor="nw", image=canvas.image)

    level_btn = tk.Button(menu, text="Легко", font=("Arial", 24), width=20, height=1, command=game_level_1_start, bg='#D19C58')
    level_btn.place(relx=0.5, rely=0.2, anchor=tk.CENTER)  # центрирование кнопки по горизонтали и вертикали

    level_btn = tk.Button(menu, text="Сложно", font=("Arial", 24), width=20, height=1, command=game_level_2_start, bg='#D19C58')
    level_btn.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # центрирование кнопки по горизонтали и вертикали

    level_btn = tk.Button(menu, text="Невозможно", font=("Arial", 24), width=20, height=1, command=game_level_3_start, bg='#D19C58')
    level_btn.place(relx=0.5, rely=0.8, anchor=tk.CENTER)  # центрирование кнопки по горизонтали и вертикали

play_btn = tk.Button(menu, text="Играть", font=("Arial", 24), width=20, height=1, command=open_game_menu, bg='#D19C58')
play_btn.place(relx=0.5, rely=0.4, anchor=tk.CENTER)  # центрирование кнопки по горизон

def main_menu():
    for widget in menu.winfo_children():
        widget.destroy()

    image = tk.PhotoImage(file='back_graund.gif')
    canvas = tk.Canvas(menu, width=image.width(), height=image.height(), highlightthickness=0)
    canvas.pack(fill='both', expand=True)
    canvas.image = image
    bg = canvas.create_image(0, 0, anchor="nw", image=canvas.image)

    play_btn = tk.Button(menu, text="Играть", font=("Arial", 24), width=20, height=1, command=open_game_menu, bg='#D19C58')
    play_btn.place(relx=0.5, rely=0.4, anchor=tk.CENTER)  # центрирование кнопки по горизонтали и вертикали

    # Создание кнопки "Инструкция"
    rules_button = tk.Button(menu, text="Правила", font=("Arial", 24), width=20, height=1, command=open_instructions, bg='#D19C58')
    rules_button.place(relx=0.5, rely=0.55, anchor=tk.CENTER)  # центрирование кнопки по горизонтали и вертикали

    # Создание кнопки "Выход"
    exit_button = tk.Button(menu, text="Выход", font=("Arial", 24), width=20, height=1, command=exit_app, bg='#D19C58')
    exit_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)  # центрирование кнопки по горизонтали и вертикали

def lose_game():
    menu.deiconify()
    for widget in menu.winfo_children():
        widget.destroy()

    image = tk.PhotoImage(file='back_graund.gif')
    canvas = tk.Canvas(menu, width=image.width(), height=image.height(), highlightthickness=0)
    canvas.pack(fill='both', expand=True)
    canvas.image = image
    bg = canvas.create_image(0, 0, anchor="nw", image=canvas.image)

    play_btn = tk.Button(menu, text="Играть", font=("Arial", 24), width=20, height=1, command=open_game_menu, bg='#D19C58')
    play_btn.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # центрирование кнопки по горизон
    rules_btn = tk.Button(menu, text="В меню", font=("Arial", 24), width=20, height=1, command=main_menu, bg='#D19C58')
    rules_btn.place(relx=0.5, rely=0.8, anchor=tk.CENTER)  # центрирование кнопки по горизонтали и вертикали
    play_label = tk.Label(menu, text="ИГРА ОКОНЧЕНА:", font=("Arial", 32, "bold"), bg='#D19C58')
    play_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)  # размещение надписи над кнопками


menu.mainloop()