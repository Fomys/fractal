# -*- coding: utf-8 -*-

"""
A new turtle which is faster.

>>> t = Turtle()
>>> t.init()
>>> t.set_position((0, 0))
>>> t.fractal.outline(6, 2, 5)

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


class Figures:
    """A lot of function to create some well-know shapes

    :param master: turtle2 to use for draw
    :type master: Turtle

    :returns: Nothing
    :rtype: None"""

    def __init__(self, master):
        self.canvas = master

    def _outline_trace(self, number_of_iterations, length, number_of_sides):
        """Internal function to draw outline of a recursive shape

        :param number_of_iterations: Number of iteration used to draw
        :param length: Size of a single side
        :param number_of_sides: Number of sides of the initial shape
        :type number_of_iterations: int
        :type length: int
        :type number_of_sides: int

        :returns: Nothing
        :rtype: None"""

        # Stop the recursion if the number of iteration is equal to zero
        if number_of_iterations == 0:
            self.canvas.forward(length)
        else:
            self._outline_trace(number_of_iterations - 1, length, number_of_sides)
            self.canvas.right(360. / number_of_sides)
            self._outline_trace(number_of_iterations - 1, length, number_of_sides)
            self.canvas.right(-360. / number_of_sides)
            self._outline_trace(number_of_iterations - 1, length, number_of_sides)
            self.canvas.right(-360. / number_of_sides)
            self._outline_trace(number_of_iterations - 1, length, number_of_sides)
            self.canvas.right(360. / number_of_sides)
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
            self.canvas.forward(length)
            self.canvas.right(angle)

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
            self.canvas.right(angle)

    def outline(self, number_of_iteration, length, number_of_sides):
        """Draw outline of a recursive shape

        :param number_of_iteration: Number of iteration used to draw
        :param length: Length of a single side
        :param number_of_sides: Number of sides of the initial shape
        :type number_of_iteration: int
        :type length: int
        :type number_of_sides: int

        :returns: Nothing
        :rtype: None"""
        for i in range(number_of_sides):
            self._outline_trace(number_of_iteration, length, number_of_sides)
            self.canvas.right(360. / number_of_sides)

    def tree(self, length, angles, factor=1.5, min_size=5):
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
            self.canvas._state["color"] = (int(length), int(length), int(length))
            for angle in angles:
                pos = self.canvas.get_position()
                base_angle = self.canvas.get_angle()
                self.canvas.right(angle)
                self.canvas.forward(length)
                self._tree(length / factor, angles, factor=factor, min_size=min_size)
                self.canvas.set_position(pos)
                self.canvas.set_angle(base_angle)

    def dragon(self, length, number_of_iteration, angle=1):
        """Draw the dragon curve

        :param angle: Start angle
        :param length: Length of a side
        :param number_of_iteration: Number of iteration for the curve
        :type length: int
        :type number_of_iteration: int

        :returns: Nothing
        :rtype: None"""
        if number_of_iteration == 0:
            self.canvas.forward(length)
        else:
            self.dragon(length, number_of_iteration - 1, 1)
            self.canvas.left(angle * 90)
            self.dragon(length, number_of_iteration - 1, -1)

    def power(self, length, power, base=1.5):
        k = base
        list_powers = []
        for i in range(power):
            k = 10 * (k * 0.15 - int(k * 0.15))
            n = int((k - int(k)) * 10)
            list_powers.append(n)
        for i in list_powers:
            angle = 36 * i
            self.canvas.right(angle)
            self.canvas.forward(length)

    def turning_tree(self, length, angles):
        while True:
            self.tree(length, angles)
            time.sleep(0.1)
            i = 0
            for _ in angles:
                angles[i] += 1
                i += 1

    def _koch_curve(self, length):
        self.canvas.forward(length)
        self.canvas.left(60)
        self.canvas.forward(length)
        self.canvas.right(120)
        self.canvas.forward(length)
        self.canvas.left(60)
        self.canvas.forward(length)

    def koch_curve(self, length, number_of_iteration):
        if number_of_iteration > 0:
            self.koch_curve(length / 3., number_of_iteration - 1)
            self.canvas.left(60)
            self.koch_curve(length / 3., number_of_iteration - 1)
            self.canvas.right(120)
            self.koch_curve(length / 3., number_of_iteration - 1)
            self.canvas.left(60)
            self.koch_curve(length / 3., number_of_iteration - 1)
        else:
            self._koch_curve(length)


class Turtle:

    @staticmethod
    def _calc_center(size):
        return size[0] / 2, size[1] / 2

    def _forward(self, distance):
        AB = (distance * math.cos(math.radians(self._state.get("angle")))) + self._state.get("coordinate_x")
        AC = (distance * math.sin(math.radians(self._state.get("angle")))) + self._state.get("coordinate_y")
        self._forward_image(distance)
        self._set_coordinates((AB, AC))

    def _forward_image(self, distance):
        AB = (distance * math.cos(math.radians(self._state.get("angle")))) + self._state.get("coordinate_x")
        AC = (distance * math.sin(math.radians(self._state.get("angle")))) + self._state.get("coordinate_y")
        self.draw.line((self.get_position('x') * self.resolution, self.get_position('y') * self.resolution,
                        AB * self.resolution, AC * self.resolution), fill=self._state.get("colour"))

    def _turn(self, angle):
        self._set_angle(self._state.get("angle") + angle)

    def _set_angle(self, angle):
        self._state["angle"] = angle
        while self._state.get("angle") >= 360:
            self._state["angle"] = self._state.get("angle") - 360

    def _clear(self):
        pass

    ### Fonction publiques ###

    def _clear_img(self):
        self.image = Image.new(
            '1', (self._config.get("size")), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.image)

    def __init__(self, titre="Turtle", size=(
            400, 400), resolution=10):
        self._config = {"titre": titre,
                        "size": size,
                        "size_IMG": (size[0] * resolution, size[1] * resolution),
                        "center": self._calc_center(size),
                        }
        self._state = {"angle": 0,
                       "coordinate_x": self._config.get("center")[0],
                       "coordinate_y": self._config.get("center")[1],
                       "colour": (0, 0, 0),
                       }
        self.fractal = Figures(self)
        self.image = Image.new(
            'RGB',
            (self._config.get("size_IMG")),
            (255,
             255,
             255))
        self.draw = ImageDraw.Draw(self.image)
        self.resolution = resolution

    def forward(self, distance):
        self._forward(distance)

    def backward(self, distance):
        self._forward(-distance)
        if self.sauvegarde:
            self._forward_image(-distance)

    def right(self, angle):
        self._turn(angle)

    def left(self, angle):
        self._turn(-angle)

    def goto(self, coordinates):
        self._set_coordinates(coordinates)
        self.draw.line(coordinates)

    def _set_coordinates(self, coordinates):
        self._state["coordinate_x"] = coordinates[0]
        self._state["coordinate_y"] = coordinates[1]

    def clear(self):
        self._clear()

    # ## Accès aux variables ##

    def set_position(self, coordinates):
        self._set_coordinates(coordinates)

    def get_position(self, type_coord=''):
        if type_coord == 'x':
            return self._state.get("coordinate_x")
        elif type_coord == "y":
            return self._state.get("coordinate_y")
        return self._state.get("coordinate_x"), self._state.get("coordinate_y")

    def set_angle(self, angle):
        self._set_angle(angle)

    def get_angle(self):
        return self._state.get("angle")

    def get_state(self):
        text = ""
        for i in self._state.items():
            text = text + "\n" + str(i[0]) + ":" + str(i[1])
        return text

    def save(self, path, type_img=None):
        self.image.save(path, type_img)


if __name__ == "__main__":
    t = Turtle()
    t.set_position((0, 0))
    t.fractal.outline(6, 2, 5)
    t.save("test.jpg")
