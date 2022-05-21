import sys
import pyglet
from pyglet.gl import *

# height of the tower
height = 5


class EmptyTowerException(Exception):
    """Error: Tried to remove a disk from and empty pillar"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class InvertedTowerException(Exception):
    """Error: Placed large disk on small disk"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class HanoiBoard:
    def __init__(self, height):
        """Constructs a board with all disks on pillars[1]"""
        self.height = height
        self.pillars = ([], [], [])
        for i in range(height):
            self.pillars[0].append(height - i)

    def pop(self, i):
        """Take a disk off the top of pillars[i] and return it"""
        if len(self.pillars[i]) > 0:
            return self.pillars[i].pop()
        else:
            raise EmptyTowerException(
                "Tried to pull a disk off pillar " + str(i) +
                ", which is empty")

    def push(self, i, disk):
        """Put a disk on top of pillars[i]"""
        if len(self.pillars[i]) == 0 or self.pillars[i][-1] > disk:
            self.pillars[i].append(disk)
            if len(self.pillars[-1]) == height:
                print("You win")
        else:
            raise InvertedTowerException(
                "Tried to put larger disk on smaller disk\n" +
                "    while moving disk of width " + str(disk) +
                " to pillar " + str(i))


def drawRect(win, color, x, y, w, h):
    verts = [(x, y + h),
             (x + w, y + h),
             (x, y),
             (x + w, y)]
    glBegin(GL_TRIANGLE_STRIP)
    for idx in range(len(verts)):
        glColor3ub(*color)
        glVertex2f(*verts[idx])
    glEnd()
    glColor3ub(255, 255, 255)


def drawDisk(win, towerHeight, width, x, y):
    ratio = (width * 1.0 / towerHeight)
    iratio = 1.0 - ratio
    color = (int(16 + 144 * iratio), int(96 + 64 * iratio), int(32 + 32 * iratio))
    drawRect(win, color, x + 128 * iratio // 2, y, 128 * ratio, 16)
    if not texture == False:
        texture.get_region(128 * iratio // 2, 0, 128 * ratio, 16).blit(x + 128 * iratio // 2, y)


def drawPillar(win, pillar, height, x, y):
    drawRect(win, (32, 112, 196), x + 60, y, 8, 20 * height)
    i = 0
    for disk in pillar:
        drawDisk(win, height, disk, x, y + i * 20)
        i += 1


def drawBoard(win, board, x, y):
    i = 0
    for pillar in board.pillars:
        drawPillar(win, pillar, board.height, x + i * 128, y)
        i += 1


def runInteractive():
    """Runs the program in interactive mode
    lets the user click and drag to move disks"""
    global texture
    global grabbed
    global height
    grabbed = 0
    window = pyglet.window.Window()
    label = pyglet.text.Label("Tower of Hanoi",
                              font_name="Times New Roman",
                              font_size=36,
                              x=window.width // 2, y=window.height,
                              anchor_x="center", anchor_y="top")
    board = HanoiBoard(height)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    try:
        texture = pyglet.resource.image("Sandy.png")
    except pyglet.resource.ResourceNotFoundException:
        print("Sandy.png (the decorative 128x16 image drawn over the disks) is missing.")
        texture = False
    winx = window.width // 2 - 192

    @window.event
    def on_mouse_press(x, y, button, modifiers):
        global grabbed
        if (winx <= x and x < winx + 384 and
            64 <= y and y < 64 + board.height * 20) and grabbed == 0:
            i = (x - winx) // 128
            try:
                grabbed = board.pop(i)
            except EmptyTowerException as e:
                print(str(e))

    @window.event
    def on_mouse_release(x, y, button, modifiers):
        global grabbed
        if (winx <= x and x < winx + 384 and
            64 <= y and y < 64 + board.height * 20) and not grabbed == 0:
            i = (x - winx) // 128
            try:
                grabbed = board.push(i, grabbed)
                grabbed = 0
            except InvertedTowerException as e:
                print(str(e))

    @window.event
    def on_mouse_motion(x, y, dx, dy):
        global mousex
        global mousey
        mousex = x
        mousey = y

    @window.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        global mousex
        global mousey
        mousex = x
        mousey = y

    @window.event
    def on_draw():
        window.clear()
        label.draw()
        drawBoard(window, board, winx, 64)
        if not grabbed == 0:
            drawDisk(window, board.height, grabbed, mousex - 64, mousey - 8)

    pyglet.app.event_loop.run()


if __name__ == "__main__":
    runInteractive()
