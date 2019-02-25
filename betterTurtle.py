# -*- coding: utf-8 -*-

"""
A new turtle which is faster.

>>> t = Turtle()
>>> t.Init()
>>> t.setPosition((0, 0))
>>> t.fractale.outline(6, 2, 5)
>>> t.mainloop()

.. autoclass:: Figures
   :members:
   :undoc-members:


.. autoclass:: Turtle
   :members:
   :undoc-members:
"""


import math
import time

from PIL import Image, ImageDraw

import tkinter as Tk


class Figures():
    """A lot of function to create some well-know shapes

    :param master: turtle2 to use for draw
    :type master: Turtle

    :returns: Nothing
    :rtype: None"""

    def __init__(self, master):
        self.canvas = master

    def _outline_trace(self, number_of_iterations, length, number_of_sides):
        """Internal fonction to draw outline of a recursive shape

        :param number_of_iterations: Number of iteration used to draw
        :param length: Size of a single side
        :param number_of_sides: Number of sides of the initial shape
        :type number_of_iterations: int
        :type length: int
        :type number_of_sides: int

        :returns: Nothing
        :rtype: None"""

        # Stop the recursivity if the number of iteration is equal to zero
        if number_of_iterations == 0:
            self.canvas.avance(length)
        else:
            self._outline_trace(number_of_iterations - 1, length, number_of_sides)
            self.canvas.droite(360. / number_of_sides)
            self._outline_trace(number_of_iterations - 1, length, number_of_sides)
            self.canvas.droite(-360. / number_of_sides)
            self._outline_trace(number_of_iterations - 1, length, number_of_sides)
            self.canvas.droite(-360. / number_of_sides)
            self._outline_trace(number_of_iterations - 1, length, number_of_sides)
            self.canvas.droite(360. / number_of_sides)
            self._outline_trace(number_of_iterations - 1, length, number_of_sides)

    def regular_polygon(self, number_of_sides, length):
        """Draw a regular polygon

        :param number_of_sides: Number of sides of the polygon
        :param length: Length of a side
        :type number_of_sides: int
        :type length: int

        :returns: Nothing
        :rtype: None"""
        angle = 360. / number_of_sides
        for i in range(number_of_sides):
            self.canvas.avance(length)
            self.canvas.droite(angle)
            i = i

    def poly_repeat(self, length, number_of_side, density):
        """Draw a repetition of a regular polygon

        :param length: Length of a side
        :param number_of_side: Regular polygon's side number
        :param density: quantity of polygon
        :type length: int
        :type number_of_side: int
        :type density: int

        :returns: Nothing
        :rtype: None"""
        angle = 360. / density
        for i in range(density):
            self.regular_polygon(number_of_side, length)
            self.canvas.droite(angle)
            i = i

    def outline(self, number_of_iteration, length, number_of_sides):
        """Draw outline of a recursive shape

        :param number_of_iterations: Number of iteration used to draw
        :param length: Length of a single side
        :param number_of_sides: Number of sides of the initial shape
        :type number_of_iterations: int
        :type length: int
        :type number_of_sides: int

        :returns: Nothing
        :rtype: None"""
        for i in range(number_of_sides):
            self._outline_trace(number_of_iteration, length, number_of_sides)
            self.canvas.droite(360. / number_of_sides)
            i = i

    def tree(self, length, angles, factor = 1.5, min_size = 5):
        """Draw a tree recursively

        :param length: Length of the root of the tree
        :param angles: List of angles for branch
        :param factor: Reduce factor for next branch
        :param min_size: Minimal length of a branch
        :type length: int
        :type angles: list
        :type factor: float
        :type min_size: float

        :returns: Nothing
        :rtype: None"""
        if length < min_size:
            return ""
        else:
            self.canvas._etat["couleur"]=(int(length), int(length), int(length))
            for angle in angles:
                pos = self.canvas.getPosition()
                anglebase = self.canvas.getAngle()
                self.canvas.droite(angle)
                self.canvas.avance(length)
                self._tree(length / factor, angles, factor=factor, min_size=min_size)
                self.canvas.setPosition(pos)
                self.canvas.setAngle(anglebase)

    def dragon(self, length, number_of_iteration, angle = 1):
        """Draw the dragon curve

        :param length: Length of a side
        :param number_of_iteration: Number of iteration for the curve
        :type length: int
        :type number_of_iteration: int

        :returns: Nothing
        :rtype: None"""
        if number_of_iteration == 0:
            self.canvas.avance(length)
        else:
            self.dragon(length, number_of_iteration - 1, 1)
            self.canvas.gauche(angle * 90)
            self.dragon(length, number_of_iteration - 1, -1)

    def power(self, length, power, base=1.5):
        k = base
        L = []
        for i in range(power):
            k = 10 * (k * 0.15 - int(k * 0.15))
            n = int((k - int(k)) * 10)
            L.append(n)
        for i in L:
            angle = 36 * i
            self.canvas.droite(angle)
            self.canvas.avance(length)

    def turning_tree(self, length, angles):
        while True:
            self.tree(length, angles)
            time.sleep(0.1)
            i = 0
            for a in angles:
                angles[i] += 1
                i += 1

    def _koch_curve(self, length):
        self.canvas.avance(length)
        self.canvas.gauche(60)
        self.canvas.avance(length)
        self.canvas.droite(120)
        self.canvas.avance(length)
        self.canvas.gauche(60)
        self.canvas.avance(length)

    def koch_curve(self, length, number_of_iteration):
        if number_of_iteration > 0:
            self.koch_curve(length / 3., number_of_iteration - 1)
            self.canvas.gauche(60)
            self.koch_curve(length / 3., number_of_iteration - 1)
            self.canvas.droite(120)
            self.koch_curve(length / 3., number_of_iteration - 1)
            self.canvas.gauche(60)
            self.koch_curve(length / 3., number_of_iteration - 1)
        else:
            self._koch_curve(length)

class Turtle(Tk.Tk):

    ### Fonctions internes ###

    def _calcCentre(self, taille):
        return (taille[0] / 2, taille[1] / 2)


        # self.canvas.update()

    def _avance(self, distance):
        AB = (distance * math.cos(math.radians(self._etat.get("angle")))) + \
            self._etat.get("coordx")
        AC = (distance * math.sin(math.radians(self._etat.get("angle")))) + \
            self._etat.get("coordy")
        self.canvas.create_line(self._etat.get("coordx"),
                                self._etat.get("coordy"),
                                AB,
                                AC)
        if self.sauvegarde:
            self._avanceIMG(distance)
        self._setCoords((AB, AC))
        # self.canvas.update()
        # self.canvas.update()

    def _avanceIMG(self, distance):
        AB = (distance * math.cos(math.radians(self._etat.get("angle")))) + \
            self._etat.get("coordx")
        AC = (distance * math.sin(math.radians(self._etat.get("angle")))) + \
            self._etat.get("coordy")
        self.draw.line(
            (self.getPosition('x') *
             self.resolution,
             self.getPosition('y') *
             self.resolution,
             AB *
             self.resolution,
             AC *
             self.resolution),
            fill=self._etat.get("couleur"))

    def _tourne(self, angle):
        self._setAngle(self._etat.get("angle") + angle)
        # self.canvas.update

    def _setAngle(self, angle):
        self._etat["angle"] = angle
        while self._etat.get("angle") >= 360:
            self._etat["angle"] = self._etat.get("angle") - 360

    def _clear(self):
        self.canvas.delete("all")
        self.canvas.update()
    ### Fonction publiques ###

    def _clearIMG(self):
        self.image = Image.new(
            '1', (self._config.get("taille")), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.image)

    def Init(self, titre="Turtle", taille=(
            400, 400), sauvegarde=False, resolution=10):
        self._config = {"titre": titre,
                        "taille": taille,
                        "tailleIMG": (taille[0] * resolution, taille[1] * resolution),
                        "centre": self._calcCentre(taille),
                        }
        self._etat = {"angle": 0,
                      "coordx": self._config.get("centre")[0],
                      "coordy": self._config.get("centre")[1],
                      "couleur": (0, 0, 0),
                      }
        self.title(self._config.get("titre"))
        self.canvas = Tk.Canvas(self,
                                width=self._config.get("taille")[0],
                                height=self._config.get("taille")[1],
                                background='white')
        self.canvas.pack()
        self.fractale = Figures(self)
        self.image = Image.new(
            'RGB',
            (self._config.get("tailleIMG")),
            (255,
             255,
             255))
        self.draw = ImageDraw.Draw(self.image)
        self.sauvegarde = sauvegarde
        self.resolution = resolution

    def avance(self, distance):
        self._avance(distance)

    def recule(self, distance):
        self._avance(-distance)
        if self.sauvegarde:
            self._avanceIMG(-distance)

    def droite(self, angle):
        self._tourne(angle)

    def gauche(self, angle):
        self._tourne(-angle)

    def goto(self, coordonnees):
        self.canvas.create_line(self._etat.get("coordx"),
                                self._etat.get("coordy"),
                                coordonnees[0],
                                coordonnees[1])
        self._setCoords(coordonnees)
        if self.sauvegarde:
            self.draw.line(coordonnees)

    def _setCoords(self, coordonnees):
        self._etat["coordx"] = coordonnees[0]
        self._etat["coordy"] = coordonnees[1]


    def clear(self):
        self._clear()
    # ## Accès aux variables ##

    def setPosition(self, coordonnees):
        self._setCoords(coordonnees)

    def getPosition(self, typeCOORD=''):
        if typeCOORD == 'x':
            return self._etat.get("coordx")
        elif typeCOORD == "y":
            return self._etat.get("coordy")
        return (self._etat.get("coordx"), self._etat.get("coordy"))

    def setAngle(self, angle):
        self._setAngle(angle)

    def getAngle(self):
        return self._etat.get("angle")

    def getEtat(self):
        texte = ""
        for i in self._etat.items():
            texte = texte + "\n" + str(i[0]) + ":" + str(i[1])
        return texte

    def save(self, chemin, typeIMG=None):
        self.image.save(chemin, typeIMG)

if __name__=="__main__":
    t = Turtle()
    t.Init()
    t.setPosition((0, 0))
    t.fractale.outline(6, 2, 5)
    t.mainloop()