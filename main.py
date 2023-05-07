import turtle
import math
import random
import tkinter as tk

def exit_app():
    root.destroy()

bulletstate = "ready"

def game_level_1_start():
    root.destroy()
    wn = turtle.Screen()
    wn.tracer(9)
    game_start()

def game_level_2_start():
    root.destroy()
    wn = turtle.Screen()
    wn.tracer(12)
    game_start()

def game_level_3_start():
    root.destroy()
    wn = turtle.Screen()
    wn.tracer(18)
    game_start()

def game_start():
    wn = turtle.Screen()
    wn.title("Space Invaders")
    wn.setup(width=665, height=775)
    wn.bgpic("Untitledback_graund_main.gif")
    turtle.resizemode("auto")

    # Объекты
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

    # добавляю противников на игровое поле
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
    score_pen.goto(-290, 280)
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
    bulletstate = "ready"

    def fire_bullet():
        global bulletstate
        if bulletstate == "ready":
            bulletstate = "fire"
            x = player.xcor()
            y = player.ycor() + 10
            bullet.goto(x, y)
            bullet.showturtle()

    def move_bullet():
        global bulletstate
        if bulletstate == "fire":
            y = bullet.ycor()
            y += bulletspeed
            bullet.sety(y)

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

    # Выстрел пули

    # Проверка на столкновение противника и пули
    def isCollision(t1, t2):
        distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
        if distance < 15:
            return True
        else:
            return False

    # бинд клаиш
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
                scorestring = "Score: %s" % score
                score_pen.clear()
                score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))

             # проигрыш
            if isCollision(player, enemy):
                player.hideturtle()
                enemy.hideturtle()
                turtle.bye()
                root1 = tk.Tk()  # будующее меню при проигрыше
                root1.title('game over')
                root1.geometry('670x800+630+150')
                bgimage = tk.PhotoImage(file="Untitledback_graund_main.gif")
                backgroundlabel = tk.Label(root1, image=bgimage)
                backgroundlabel.place(x=0, y=0, relwidth=1, relheight=1)
                play_label1 = tk.Label(root1, text="Игра окончена", font=("Arial", 32, "bold"), bg='#D19C58')
                play_label1.place(relx=0.5, rely=0.2, anchor=tk.CENTER)  # размещение надписи над кнопками
                root1.mainloop()
                break
            if enemy.ycor() < -250:
                player.hideturtle()
                turtle.bye()
                root1 = tk.Tk()  # будующее меню при проигрыше
                root1.title('game over')
                root1.geometry('670x800+630+150')
                bgimage = tk.PhotoImage(file="Untitledback_graund_main.gif")
                backgroundlabel = tk.Label(root1, image=bgimage)
                backgroundlabel.place(x=0, y=0, relwidth=1, relheight=1)
                play_label1 = tk.Label(root1, text="Игра окончена", font=("Arial", 32, "bold"), bg='#D19C58')
                play_label1.place(relx=0.5, rely=0.2, anchor=tk.CENTER)  # размещение надписи над кнопками
                root1.mainloop()
                break

        # выстрел пули
        if bulletstate == "fire":
            y = bullet.ycor()
            y += bulletspeed
            bullet.sety(y)

        # переспавн пули при промахе
        if bullet.ycor() > 275:
            bullet.hideturtle()
            bulletstate = "ready"

root = tk.Tk()
root.geometry('670x800+630+150')
root.title("Space Invaders")
root.resizable(False, False)  # запрет масштабирования окна
# добавляем изображение на фон
bgimage = tk.PhotoImage(file="Untitledback_graund_main.gif")
backgroundlabel = tk.Label(root, image=bgimage)
backgroundlabel.place(x=0, y=0, relwidth=1, relheight=1)

    # Создание надписи "Играть:"
play_label = tk.Label(root, text="SPACE INVADERS", font=("Arial", 32, "bold"), bg='#D19C58')
play_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER) # размещение надписи над кнопками

# Функция для открытия инструкции
def open_instructions():
    # Удаляем все виджеты в главном окне
    for widget in root.winfo_children():
        widget.destroy()

    # Создание текстового диапазона
    text_frame = tk.Frame(root)
    text_frame.place(relx=0.5, rely=0.5, relwidth=1, relheight=0.7, anchor=tk.CENTER)

    # Создание текста правил игры
    instructions_text = """СТРАХА НЕТ"""

    # Создание метки для текста правил игры и размещение ее в текстовом диапазоне
    instructions_label = tk.Label(text_frame, text=instructions_text, font=("Arial", 14), justify="left",
                                  wraplength=562, bg='#D8DE87')
    instructions_label.pack(fill="both", expand=True)

    # Создание кнопки "В главное меню"
    instruction_button = tk.Button(root, text="назад", font=("Arial", 24), width=20, height=1, command=main_menu, bg='#D19C58')
    instruction_button.place(relx=0.5, rely=0.92, anchor=tk.CENTER)  # центрирование кнопки по горизонтали и вертикали


# Создание кнопки "Инструкция"
instruction_button = tk.Button(root, text="Правила", font=("Arial", 24), width=20, height=1, command=open_instructions, bg='#D19C58')
instruction_button.place(relx=0.5, rely=0.55, anchor=tk.CENTER)  # центрирование кнопки по горизонтали и вертикали

# Создание кнопки "Выход"
exit_button = tk.Button(root, text="Выход", font=("Arial", 24), width=20, height=1, command=exit_app, bg='#D19C58')
exit_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)  # центрирование кнопки по горизонтали и вертикали

def open_game_menu():
    # Удаляем все виджеты в главном окне
    for widget in root.winfo_children():
        widget.destroy()

    # Создание уровней сложности
    game_button = tk.Button(root, text="Легко", font=("Arial", 24), width=20, height=1, command=game_level_1_start, bg='#D19C58')
    game_button.place(relx=0.5, rely=0.2, anchor=tk.CENTER)  # центрирование кнопки по горизонтали и вертикали

    game_button = tk.Button(root, text="Сложно", font=("Arial", 24), width=20, height=1, command=game_level_2_start, bg='#D19C58')
    game_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # центрирование кнопки по горизонтали и вертикали

    game_button = tk.Button(root, text="Невозможно", font=("Arial", 24), width=20, height=1, command=game_level_3_start, bg='#D19C58')
    game_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)  # центрирование кнопки по горизонтали и вертикали


play_button = tk.Button(root, text="Играть", font=("Arial", 24), width=20, height=1, command=open_game_menu, bg='#D19C58')
play_button.place(relx=0.5, rely=0.4, anchor=tk.CENTER)  # центрирование кнопки по горизон

def main_menu():
    for widget in root.winfo_children():
        widget.destroy()

    play_label = tk.Label(root, text="SPACE INVADERS", font=("Arial", 32, "bold"), bg='#D19C58')
    play_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)  # размещение надписи над кнопками

    play_button = tk.Button(root, text="Играть", font=("Arial", 24), width=20, height=1, command=open_game_menu, bg='#D19C58')
    play_button.place(relx=0.5, rely=0.4, anchor=tk.CENTER)  # центрирование кнопки по горизонтали и вертикали

    # Создание кнопки "Инструкция"
    instruction_button = tk.Button(root, text="Правила", font=("Arial", 24), width=20, height=1, command=open_instructions, bg='#D19C58')
    instruction_button.place(relx=0.5, rely=0.55, anchor=tk.CENTER)  # центрирование кнопки по горизонтали и вертикали

    # Создание кнопки "Выход"
    exit_button = tk.Button(root, text="Выход", font=("Arial", 24), width=20, height=1, command=exit_app, bg='#D19C58')
    exit_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)  # центрирование кнопки по горизонтали и вертикали

root.mainloop()
