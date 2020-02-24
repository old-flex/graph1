import numpy as np
from tkinter import *
import math


class Edges:
    move_to_zero = np.array([[1, 0, 0, 0],
                             [0, 1, 0, 0],
                             [0, 0, 1, 0],
                             [-350, -150, 0, 1]]).transpose()

    move_to_center = np.array([[1, 0, 0, 0],
                               [0, 1, 0, 0],
                               [0, 0, 1, 0],
                               [350, 150, 0, 1]]).transpose()

    def __init__(self):
        self.edges = np.loadtxt('edges.txt')

    @staticmethod
    def read_from_file():
        return np.loadtxt("edges.txt")


def move(message_x, message_y, message_z):
    a = 0
    b = 0
    c = 0
    if len(message_x.get()) > 0:
        a = int(message_x.get())
    if len(message_y.get()) > 0:
        b = int(message_y.get())
    if len(message_z.get()) > 0:
        c = int(message_z.get())

    matrix_moving = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [a, b, c, 1]
    ]).transpose()

    edges.edges = multiplication(matrix_moving)


def scale(a, b, c):
    matrix_scaling = np.array([[a, 0, 0, 0],
                               [0, b, 0, 0],
                               [0, 0, c, 0],
                               [0, 0, 0, 1]]).transpose()

    edges.edges = multiplication(edges.move_to_zero)
    edges.edges = multiplication(matrix_scaling)
    edges.edges = multiplication(edges.move_to_center)


def turn(message_x, message_y, message_z):
    a = 0
    b = 0
    c = 0
    if len(message_x.get()) > 0:
        a = int(message_x.get())
    if len(message_y.get()) > 0:
        b = int(message_y.get())
    if len(message_z.get()) > 0:
        c = int(message_z.get())

    matrix_turn_x = np.array([[1, 0, 0, 0],
                              [0, math.cos(math.radians(a)), math.sin(math.radians(a)), 0],
                              [0, -math.sin(math.radians(a)), math.cos(math.radians(a)), 0],
                              [0, 0, 0, 1]]).transpose()
    matrix_turn_y = np.array([[math.cos(math.radians(b)), 0, -math.sin(math.radians(b)), 0],
                              [0, 1, 0, 0],
                              [math.sin(math.radians(b)), 0, math.cos(math.radians(b)), 0],
                              [0, 0, 0, 1]]).transpose()
    matrix_turn_z = np.array([[math.cos(math.radians(c)), math.sin(math.radians(c)), 0, 0],
                              [-math.sin(math.radians(c)), math.cos(math.radians(c)), 0, 0],
                              [0, 0, 1, 0],
                              [0, 0, 0, 1]]).transpose()

    if a > 0:
        edges.edges = multiplication(edges.move_to_zero)
        edges.edges = multiplication(matrix_turn_x)
        edges.edges = multiplication(edges.move_to_center)
    if b > 0:
        edges.edges = multiplication(edges.move_to_zero)
        edges.edges = multiplication(matrix_turn_y)
        edges.edges = multiplication(edges.move_to_center)
    if c > 0:
        edges.edges = multiplication(edges.move_to_zero)
        edges.edges = multiplication(matrix_turn_z)
        edges.edges = multiplication(edges.move_to_center)


def multiplication(matrix):
    temp = []
    for edge in edges.edges:
        new_str = []
        for i in range(len(matrix)):
            new_str.append(sum(edge * matrix[i]))
        temp.append(new_str)
    return temp


def reset():
    edges.edges = edges.read_from_file()


def drawing(canvas):
    canvas.delete('all')
    matrix_oblique = np.array([[1, 0, 0, 0],
                               [0, 1, 0, 0],
                               [-0.5 * math.cos(math.radians(45)), -0.5 * math.sin(math.radians(45)), 0, 0],
                               [0, 0, 0, 1]]).transpose()

    temp = multiplication(matrix_oblique)
    for i in range(len(temp) - 2):
        canvas.create_line(temp[i][0], temp[i][1], temp[i + 1][0], temp[i + 1][1], fill='white')
    canvas.create_line(temp[len(temp) - 2][0], temp[len(temp) - 2][1], temp[len(temp) - 1][0], temp[len(temp) - 1][1],
                       fill='white')


edges = Edges()


def main():
    root = Tk()
    root.title('Первая пошла')
    root.geometry('900x600')

    canvas = Canvas(root, width=700, height=600, bg='grey')
    canvas.place(x=0, y=0)
    drawing(canvas)

    move_x_message = StringVar()
    move_y_message = StringVar()
    move_z_message = StringVar()

    turn_x_message = StringVar()
    turn_y_message = StringVar()
    turn_z_message = StringVar()

    move_x = Label(root, text="x").place(x=750, y=20)
    move_y = Label(root, text="y").place(x=750, y=40)
    move_z = Label(root, text="z").place(x=750, y=60)

    e_move_x = Entry(root, textvariable=move_x_message, width=5).place(x=780, y=20)
    e_move_y = Entry(root, textvariable=move_y_message, width=5).place(x=780, y=40)
    e_move_z = Entry(root, textvariable=move_z_message, width=5).place(x=780, y=60)

    turn_x = Label(root, text="x").place(x=750, y=260)
    turn_y = Label(root, text="y").place(x=750, y=280)
    turn_z = Label(root, text="z").place(x=750, y=300)

    e_turn_x = Entry(root, textvariable=turn_x_message, width=5).place(x=780, y=260)
    e_turn_y = Entry(root, textvariable=turn_y_message, width=5).place(x=780, y=280)
    e_turn_z = Entry(root, textvariable=turn_z_message, width=5).place(x=780, y=300)

    button_move = Button(root, text="Переместить",
                         command=lambda: [move(move_x_message, move_y_message, move_z_message), drawing(canvas)]).place(
        x=750, y=100)

    button_scale_plus = Button(root, text="Масштабировать +",
                               command=lambda: [scale(2, 2, 2),
                                                drawing(canvas)]).place(x=750, y=160)

    button_scale_minus = Button(root, text="Масштабировать - ",
                                command=lambda: [scale(0.5, 0.5, 0.5),
                                                 drawing(canvas)]).place(x=750, y=190)

    button_turn = Button(root, text="Повернуть",
                         command=lambda: [turn(turn_x_message, turn_y_message, turn_z_message), drawing(canvas)]).place(
        x=770, y=340)

    button_reset = Button(root, text="Сбросить изменения", command=lambda: [reset(), drawing(canvas)]).place(x=740,
                                                                                                             y=500)
    root.mainloop()


if __name__ == '__main__':
    main()
