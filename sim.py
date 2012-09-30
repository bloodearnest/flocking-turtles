import time
from random import randint, random

from turtle import TurtleScreen, RawTurtle, TK


def get_screen(w, h):
    cv = TK.Canvas(width=w, height=h)
    cv.pack()
    return TurtleScreen(cv)

W = 300
H = 300

s = get_screen(W, H)


def wrap(t):
    x, y = t.pos()
    nx = ny = None
    if x > W/2:
        nx = x - W
    elif x < -W/2:
        nx = x + W

    if y > H/2:
        ny = y - H
    elif y < -H/2:
        ny = y + H

    if nx is not None:
        t.setx(nx)
    if ny is not None:
        t.sety(ny)


def clip(t):
    x, y = t.pos()
    nx = ny = None
    if x > W/2:
        nx = W/2
    elif x < -W/2:
        nx = -W/2

    if y > H/2:
        ny = H/2
    elif y < -H/2:
        ny = -H/2

    if nx is not None:
        t.setx(nx)
    if ny is not None:
        t.sety(ny)

xx_start = time.time()

s.tracer(0, 0)
turtles = [RawTurtle(s) for i in range(50)]


for t in turtles:
    t.ht()
    t.penup()
    t.goto(randint(0, W) - W / 2, randint(0, H) - H / 2)
    t.right(randint(0, 360))
    t.st()

ticks = 30
max_speed = 1
max_turn = 5
too_close = 10
e = 0.1
sight = 40
r = 1.0 / float(ticks)


def my_turtle(t, neighbours):
    if neighbours:
        heading = t.heading()
        dist, closest = min(neighbours)
        if dist < too_close:
            other = closest.heading()
            dir = t.left if random() < 0.5 else t.right
            if heading < other:
                dir = t.left
            elif heading > other:
                dir = t.right
            dir(max_turn)
            t.color('red')
        else:
            avg = sum(n[1].heading() for n in neighbours) / len(neighbours)
            #if random() < 0.1:
            #    avg += random() * e - (e / 2.0)
            if heading + max_turn > avg:
                t.left(max_turn)
            elif heading - max_turn < avg:
                t.right(max_turn)
            #else:
            #    t.setheading(avg)
            t.color('green')
    else:
        # random walk
        angle = random() * max_turn * 2 - max_turn
        t.right(angle)
        t.color('blue')

    t.forward(max_speed)


def get_neighbours(me, threshold=sight):
    n = []
    for t in turtles:
        if t != me:
            d = t.distance(me)
            heading = me.towards(t)
            if d < threshold and (heading < 90 or heading > 270):
                n.append((d, t))
    return n

for i in range(1000):
    start = time.time()
    for t in turtles:
        my_turtle(t, get_neighbours(t))
        wrap(t)

    s.update()
    elapsed = time.time() - start
    if elapsed < r:
        time.sleep(r - elapsed)
    else:
        print("Too slow!")

print(time.time() - xx_start)
