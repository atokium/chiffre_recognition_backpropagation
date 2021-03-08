import tkinter as tk
from PIL import Image
from PIL import ImageDraw
import numpy as np
import cv2

from crop import crop

from model import myNN
from model import apply_model


# canvas and bottons
class CanvasCreat:
    def __init__(self, parent, posx, posy, *kwargs):
        self.parent = parent
        self.posx = posx
        self.posy = posy
        self.sizex = 200
        self.sizey = 200
        self.b1 = "up"
        self.xold = None
        self.yold = None
        self.drawing_area = tk.Canvas(self.parent,
                                      width=self.sizex,
                                      height=self.sizey)
        self.drawing_area.place(x=self.posx, y=self.posy)
        self.drawing_area.bind("<Motion>", self.motion)
        self.drawing_area.bind("<ButtonPress-1>", self.b1down)
        self.drawing_area.bind("<ButtonRelease-1>", self.b1up)
        self.button = tk.Button(self.parent,
                                text="Magic",
                                width=10,
                                bg='gray',
                                command=self.magic)
        self.button.place(x=self.sizex / 7, y=self.sizey + 20)
        self.button1 = tk.Button(self.parent,
                                 text="Clear",
                                 width=10,
                                 bg='gray',
                                 command=self.clear)
        self.button1.place(x=(self.sizex / 7) + 80, y=self.sizey + 20)

        self.image = Image.new("RGB", (200, 200), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.image)

    # save drowings and extract and feed it to the model:
    def magic(self):
        # do magic
        self.image.save('image.jpg')
        img = cv2.imread('image.jpg', 0)
        img = crop(img)
        prid = apply_model(img)
        #print("predicted value is : ", prid)
        my_label = tk.Label(root, text=prid, font=("Arial Bold", 150))
        my_label.config(bg="black")
        my_label.place(x=50, y=480, anchor='sw')

    # clear canvas
    def clear(self):
        self.drawing_area.delete("all")
        self.image = Image.new("RGB", (200, 200), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.image)

    # mouse clicked :
    def b1down(self, event):
        self.b1 = "down"

    # mouse not clicked
    def b1up(self, event):
        self.b1 = "up"
        self.xold = None
        self.yold = None

    # cursour is moving and clicked :
    def motion(self, event):
        if self.b1 == "down":
            if self.xold is not None and self.yold is not None:
                event.widget.create_line(self.xold,
                                         self.yold,
                                         event.x,
                                         event.y,
                                         smooth='true',
                                         width=15,
                                         fill='red')
                self.draw.line(((self.xold, self.yold), (event.x, event.y)),
                               (0, 0, 0),
                               width=15)

        self.xold = event.x
        self.yold = event.y


if __name__ == "__main__":
    root = tk.Tk()
    root.wm_geometry("%dx%d+%d+%d" % (225, 500, 10, 10))
    root.config(bg='black')
    CanvasCreat(root, 10, 10)
    root.mainloop()
