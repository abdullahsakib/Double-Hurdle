
from itertools import cycle
from random import randrange
from tkinter import Canvas, Tk, messagebox, font

canvas_width = 600
canvas_height = 400

root = Tk()
root.title("Double Hurdle")

color_cycle = cycle(["light blue", "light green", "light pink", "light yellow", "light cyan"])
color_cycle2 = cycle(["blue", "green", "pink", "yellow", "cyan","purple"])

c = Canvas(root, width=canvas_width, height=canvas_height, background="deep sky blue")
c.create_rectangle(0,0,80,40, fill='orange', width=0)
c.create_rectangle(canvas_width-80 ,0,canvas_width ,40, fill='orange', width=0)
c.create_rectangle(0,canvas_height/1.5+20,canvas_width,canvas_height,fill="sea green")
c.pack()

catcher = c.create_arc(20, canvas_height-40, 80, canvas_height-80, start=200, extent=140, style='arc',outline=next(color_cycle2), width=5)

star = c.create_polygon(60, 60, 90, 60, 90, 90, 60, 90, 115, 75)
score=0
score_text=c.create_text(10,10,anchor='nw',fill="darkblue", text="Score: "+ str(score))
life=100
life_text=c.create_text(canvas_width-20,10,anchor='ne',fill="darkblue", text="Life: "+ str(life))

eggs = []
enemies = []

def create_egg(event):
    (x1, y1, x2, y2, x3, y3, x4, y4, x5, y5) = c.coords(star)
    new_egg = c.create_oval(x5 - 10, y5 - 4, x5 + 10, y5+4 , fill=next(color_cycle), width=0)
    eggs.append(new_egg)

def move_eggs():
    for egg in eggs:
        c.move(egg, 20, 0)  # Move eggs downward
        if c.coords(egg)[1] > canvas_height:  # If egg is out of canvas
            eggs.remove(egg)
            c.delete(egg)
    root.after(100, move_eggs)

def enemy():
    x = canvas_width - 20
    y = randrange(60, canvas_height/2-60)
    new_enemy = c.create_oval(x, y, x + 20, y + 20, fill="red", width=2)
    enemies.append(new_enemy)
    root.after(4000, enemy)

def move_enemy():
    for enemy in enemies:
        c.move(enemy, -5, 0)  # Move enemies leftward
        if c.coords(enemy)[0] < 0:  # If enemy is out of canvas
            enemies.remove(enemy)
            c.delete(enemy)
    root.after(100, move_enemy)

def create_star(x, y, size=10):
    """Create a star shape centered at (x, y) with the specified size."""
    points = [
        x, y - size,  # Top point
        x + size, y + size,  # Bottom-right point
        x - size, y - size / 2,  # Left point
        x + size, y - size / 2,  # Right point
        x - size, y + size  # Bottom-left point
    ]
    return c.create_polygon(points, fill="gold", outline="black", width=2)

new_starts=[]

def collision():
    for egg in eggs[:]:
        x1, y1, x2, y2 = c.coords(egg)
        for enemy in enemies[:]:
            x3, y3, x4, y4 = c.coords(enemy)
            # Check if the bounding boxes overlap
            if (x1 < x4 and x2 > x3) and (y1 < y4 and y2 > y3):
                c.itemconfig(star, outline=next(color_cycle2))
                # Collision detected
                eggs.remove(egg)
                c.delete(egg)
                x, y = (x3 + x4) / 2, (y3 + y4) / 2  # Center position of enemy
                c.delete(enemy)
                enemies.remove(enemy)
                new_star = create_star(x, y)
                new_starts.append(new_star)
                def move_star_down():
                    c.move(new_star, 0, 10)
                    if c.coords(new_star)[1] > canvas_height:  # If  is out of canvas
                        new_starts.remove(new_star)
                        c.delete(new_star)
                    root.after(100, move_star_down)

                move_star_down()
    root.after(100, collision)

def lose_a_life():
    global life, score
    if life <= 0:
        # Clear the canvas and display "Game Over" message
        c.delete("all")
        c.create_text(canvas_width / 2, canvas_height / 2+30, text="Game Over", font=("Arial", 48), fill="red")
        c.create_text(canvas_width/2,canvas_height / 2-30, text="Score"+str(score), font=("Arial", 36), fill="blue" )
        return
    life_lost=False
    for item in new_starts:
        if c.coords(item)[1] > canvas_height-10 and not life_lost:
            life -= 5
            life_lost=True
    for enemy in enemies :
        if c.coords(enemy)[0]<10 and not life_lost:
            life -= 5
            life_lost = True

    c.itemconfig(life_text, text="Life: "+ str(life))
    root.after(100, lose_a_life)

def movel(event):
    (x1, y1, x2, y2, x3, y3, x4, y4, x5, y5) = c.coords(star)
    if x1>10:
        c.move(star, -20, 0)

def mover(event):
    (x1, y1, x2, y2, x3, y3, x4, y4, x5, y5) = c.coords(star)
    if x2 < canvas_width-30:
        c.move(star, 20, 0)

def moveu(event):
    (x1, y1, x2, y2, x3, y3, x4, y4, x5, y5) = c.coords(star)
    if y1>60:
        c.move(star, 0, -20)

def moved(event):
    (x1, y1, x2, y2, x3, y3, x4, y4, x5, y5) = c.coords(star)
    if y2 < canvas_height/1.5-30:
        c.move(star, 0, 20)

def move_left(event):
    x1, y1, x2, y2 = c.coords(catcher)
    if x1 > 0:
        c.move(catcher, -20, 0)

def move_right(event):
    x1, y1, x2, y2 = c.coords(catcher)
    if x2 < canvas_width:
        c.move(catcher, 20, 0)

def move_up(event):
    x1, y1, x2, y2 = c.coords(catcher)
    if y2 > canvas_height/1.5+40:
        c.move(catcher, 0, -20)

def move_down(event):
    x1, y1, x2, y2 = c.coords(catcher)
    if y2 < canvas_height-20:
        c.move(catcher, 0, 20)

def check_catch():
    global score
    (catcherx, catchery, catcherx2, catchery2) = c.coords(catcher)

    for item in new_starts:
        x1, y1, x2, y2, x3, y3, x4, y4, x5, y5=c.coords(item)
        if catcherx<x1 and catcherx2>x2 and catchery2-y2<40:
            new_starts.remove(item)
            c.delete(item)
            score+=10
            c.itemconfig(score_text, text="Score: " + str(score))
            c.itemconfig(catcher, outline=next(color_cycle2))
    root.after(100, check_catch)

# Bind keys for movement and egg creation
c.bind("<a>", move_left)
c.bind("<d>", move_right)
c.bind("<w>", move_up)
c.bind("<s>", move_down)
c.bind("<Left>", movel)
c.bind("<Right>", mover)
c.bind("<Up>", moveu)
c.bind("<Down>", moved)
c.bind("<space>", create_egg)
c.focus_set()

root.after(1000, move_eggs)
root.after(2000, enemy)
root.after(1000, move_enemy)
root.after(100, collision)
root.after(100, check_catch)
root.after(100, lose_a_life)

root.mainloop()