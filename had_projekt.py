import pyglet
from random import randrange
from pyglet.window import key

# uživatel si sám může zvolit rychlost hada - v rozsahu 1-10
while True:
    vstup = input('Zadej rychlost hada (1 - nejpomalejší, 10 - nejrychlejší): ')
    try:
        rychlost = int(vstup)
    except ValueError:
        print('Toto není ani číslo! Zkus to znovu.')
    else:
        if rychlost > 0 and rychlost < 11:
            break
        else:
            print('Jsi mimo rozsah! Zkus to znovu.')

window = pyglet.window.Window(640, 640)

obrazek = pyglet.image.load('tail-head.png')
cely_had = [pyglet.sprite.Sprite(obrazek,2*64,0),pyglet.sprite.Sprite(obrazek,1*64,0),pyglet.sprite.Sprite(obrazek,0,0)]
klavesa = key.RIGHT

zradlo = pyglet.image.load('apple.png')
jablko = pyglet.sprite.Sprite(zradlo, 128, 128)
jidlo = (jablko.x, jablko.y)


def tik(t):
    hlava = cely_had[0]
    ocas = cely_had[-2] #-2, protože v případě -1 mi odskakoval ocas po sežrání ovoce
    souradnice = []
    for cast in cely_had:
        souradnice.append((cast.x, cast.y)) #pro kontrolu s žrádlem

    # ověření, že had nejí sám sebe
    for i in range(1, len(cely_had)):
        if cely_had[i].x == hlava.x and cely_had[i].y == hlava.y:
            pyglet.app.exit()
            print('Game Over! Nemůžeš jíst sám sebe. Délka hada:', len(souradnice))

    # definice pohybu všemi směry - umazání posledního článku, přidání nového
    if klavesa == key.RIGHT:
        cely_had.pop().delete()
        cely_had.insert(0, pyglet.sprite.Sprite(obrazek, hlava.x + 64, hlava.y))
    elif klavesa == key.LEFT:
        cely_had.pop().delete()
        cely_had.insert(0, pyglet.sprite.Sprite(obrazek, hlava.x - 64, hlava.y))
    elif klavesa == key.UP:
        cely_had.pop().delete()
        cely_had.insert(0, pyglet.sprite.Sprite(obrazek, hlava.x, hlava.y + 64))
    elif klavesa == key.DOWN:
        cely_had.pop().delete()
        cely_had.insert(0, pyglet.sprite.Sprite(obrazek, hlava.x, hlava.y - 64))

    # ošetření, aby had nezdrhl za zeď
    if hlava.x < 0 or hlava.x > 640 or hlava.y < 0 or hlava.y > 640:
        pyglet.app.exit()
        print('Game Over! Narazil jsi do zdi. Délka hada:', len(souradnice))

    # had sní jablko
    if hlava.x == jablko.x and hlava.y == jablko.y:
        cely_had.insert(-1, pyglet.sprite.Sprite(obrazek, ocas.x, ocas.y)) # přidání článku - ocas
        while True: # aby se jablko negenerovalo přes tělo hada
            jablko.x = randrange(10)*64
            jablko.y = randrange(10)*64
            if (jablko.x, jablko.y) not in souradnice:
                return jablko.x, jablko.y

pyglet.clock.schedule_interval(tik, 1/rychlost)

def odchyt(symbol, modifikatory):
    global klavesa #tohle mi přímo napsal kouč na hodině
    klavesa = symbol

def vykresli():
    window.clear()
    for cast in cely_had:
        cast.draw()
    jablko.draw()

window.push_handlers(
    on_draw=vykresli,
    on_key_press=odchyt,
)

pyglet.app.run()
