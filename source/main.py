from math import atan, cos, sin, pi
from typing import List, Any, Tuple

from PIL import Image, ImageDraw

"""
A lib to draw fractals on pillow image

>>> img = Image.new('RGB', (5000, 5000), (0, 0, 0))
>>> figures = Figures(im=img)
>>> figures.von_koch_curve_flake((2500, 2500), 2000,6)
>>> img.save("test.bmp")"""


class State:
    """State of Lsystem"""
    width: int
    color: Tuple[int, int, int]
    angle: int
    y: int
    x: int

    def __init__(self):
        """Initialisation of state

        >>> State().x
        0
        >>> State().y
        0
        >>> State().angle
        0
        >>> State().color
        (255, 255, 255)
        >>> State().width
        0"""
        self.x = 0
        self.y = 0
        self.angle = 0
        self.color = (255, 255, 255)
        self.width = 0


class Lsystem(ImageDraw.ImageDraw):
    """Draw a L system"""
    state: State
    states: List[State]

    def __init__(self, *args, **kwargs):
        """Initialisation

        Parameters are the same than ImageDraw.__init__"""
        super().__init__(*args, **kwargs)
        self.states = []
        self.state = State()

    def _right(self, angle):
        """Turn pen to right of angle

        :param angle: Angle to rotate
        :type angle: float
        """
        self.state.angle -= angle

    def _left(self, angle):
        """Turn pen to left of angle

        :param angle: Angle to rotate
        :type angle: float
        """
        self.state.angle += angle

    def _forward(self, distance):
        """Forward pen of distance

        :param distance: Distance to forward
        :type distance: float
        """
        x_2: float = (distance * cos(self.state.angle)) + self.state.x
        y_2: float = (distance * sin(self.state.angle)) + self.state.y
        self.line(((self.state.x, self.state.y), (x_2, y_2)), self.state.color, self.state.width)
        self.state.x, self.state.y = x_2, y_2

    def _backward(self, distance):
        """Backward pen of distance

        :param distance: Distance to backward
        :type distance: float
        """
        self._forward(-distance)

    def _save(self):
        """Save state of pen"""
        self.states.append(self.state)

    def _restore(self):
        """Restore last pen state"""
        self.state = self.states[-1]
        del self.states[-1]

    def draw_l(self, start, replacement, constants, nb_recursive, color = (255, 255, 255), width=0):
        """Draw a L system

        :param start: Axiome
        :param replacement: Dictionary which contain replacement values (F->F+F-F-F+F)
        :param constants: Dictionary which contain all elements with there function
        :param nb_recursive: Number of recursion
        :param color: Color to use for the drawing
        :param width: The line width, in pixels
        :type start: str
        :type replacement: dict
        :type constants: dict
        :type nb_recursive: int
        :type color: tuple(int, int, int)
        :type width: int
        """
        self.state.color = color
        self.state.width = width
        for i in range(nb_recursive):
            for key, value in replacement.items():
                start = start.replace(key, value)
        for item in start:
            constants[item]()

    def right(self, angle):
        """Return a lambda function which make pen turning of angle radians to right

        :param angle: Angle to build function
        :type angle: float

        :return: lambda function to make pen turning right
        :rtype: lambda"""
        return lambda: self._right(angle)

    def left(self, angle):
        """Return a lambda function which make pen turning of angle radians to left

        :param angle: Angle to build function
        :type angle: float

        :return: lambda function to make pen turning left
        :rtype: lambda"""
        return lambda: self._left(angle)

    def forward(self, distance):
        """Return a lambda function which make pen forward of distance

        :param distance: Distance to build function
        :type distance: float

        :return: lambda function to make pen forward
        :rtype: lambda"""
        return lambda: self._forward(distance)

    def backward(self, distance):
        """Return a lambda function which make pen backward of distance

        :param distance: Distance to build function
        :type distance: float

        :return: lambda function to make pen backward
        :rtype: lambda"""
        return lambda: self._backward(distance)

    def save(self):
        """Return a lambda function which save state of pen

        :return: lambda function to save pen state
        :rtype: lambda"""
        return lambda: self._save()

    def restore(self):
        """Return a lambda function which restore state of pen

        :return: lambda function to restore pen state
        :rtype: lambda"""
        return lambda: self._restore()


class Figures(ImageDraw.ImageDraw):
    """A lot of function to create some well-know shapes"""

    def von_koch_curve_flake(self, origin, radius, iterations, angle=0, color=None, width=0):
        """Draw thee von koch flake on image.

        :param origin: coordinate of the center of circumscribed circle of main triangle
        :param radius: radius of circumscribed circle of main triangle
        :param iterations: iterations for the drawings
        :param angle: rotation of main triangle
        :param color: color to use for the lines
        :param width: the line width, in pixels
        :type radius: float
        :type origin: tuple
        :type iterations: int
        :type angle: float
        :type color: tuple
        :type width: int"""
        angle = angle + pi / 2
        summit_1 = (origin[0] + cos(angle) * radius, origin[1] + sin(angle) * radius)
        summit_2 = (origin[0] + cos(angle + 2 / 3 * pi) * radius, origin[1] + sin(angle + 2 / 3 * pi) * radius)
        summit_3 = (origin[0] + cos(angle - 2 / 3 * pi) * radius, origin[1] + sin(angle - 2 / 3 * pi) * radius)
        self.von_koch_curve(summit_2, summit_1, iterations, color, width)
        self.von_koch_curve(summit_3, summit_2, iterations, color, width)
        self.von_koch_curve(summit_1, summit_3, iterations, color, width)

    @staticmethod
    def _int(value):
        """Make a tuple of float coordinate into tuple of int coordinate

        :param value: Tuple to convert
        :type value: tuple(float, float)

        :return: new tuple with int values
        :rtype: tuple(int, int)"""
        return int(value[0]), int(value[1])

    def von_koch_curve(self, origin, finish, iterations=1, color=None, width=0):
        """Draw thee von koch flake on image.

        :param origin: coordinate of the starting point
        :param finish: coordinate of the ending point
        :param iterations: iterations for the drawings
        :param color: color to use for the lines
        :param width: the line width, in pixels
        :type origin: tuple
        :type finish: tuple
        :type iterations: int
        :type color: tuple
        :type width: int"""
        third = origin[0] + (finish[0] - origin[0]) * 1 / 3, origin[1] + (finish[1] - origin[1]) * 1 / 3
        two_third = origin[0] + (finish[0] - origin[0]) * 2 / 3, origin[1] + (finish[1] - origin[1]) * 2 / 3

        length = (((origin[0] - finish[0]) ** 2 + (origin[1] - finish[1]) ** 2) ** 0.5) / 3
        angle = atan((finish[1] - origin[1]) / (finish[0] - origin[0]))
        angle_total = angle + pi / 3
        if origin[0] > finish[0]:
            angle_total += pi
        summit = (cos(angle_total) * length + third[0], sin(angle_total) * length + third[1])
        if iterations <= 1:
            self.line([self._int(origin), self._int(third), self._int(summit), self._int(two_third), self._int(finish)],
                      color, width)
        else:
            self.von_koch_curve(self._int(origin), self._int(third), iterations - 1, color, width)
            self.von_koch_curve(self._int(third), self._int(summit), iterations - 1, color, width)
            self.von_koch_curve(self._int(summit), self._int(two_third), iterations - 1, color, width)
            self.von_koch_curve(self._int(two_third), self._int(finish), iterations - 1, color, width)


if __name__ == "__main__":
    img = Image.new('RGB', (5000, 5000), (0, 0, 0))
    figures = Figures(im=img)
    figures.von_koch_curve_flake((2500, 2500), 2000, 6)
    img.save("D:\\Users\\louis chauvet\\Documents\\GitHub\\fractale\\test.bmp")

    img = Image.new('RGB', (5000, 5000), (255, 255, 255))
    figures = Lsystem(im=img)
    figures.state.x, figures.state.y = 4000, 4000
    figures.draw_l("F", {"F": "F+F-F", },
                   {"+": figures.left(pi * 2 / 3), '-': figures.right(pi * 2 / 3), "F": figures.forward(50), }, 7,
                   (255, 0, 0), 2)
    figures._left(2*pi/3)
    figures.draw_l("F", {"F": "F+F-F", },
                   {"+": figures.left(pi * 2 / 3), '-': figures.right(pi * 2 / 3), "F": figures.forward(50), }, 7,
                   (0, 255, 0, 2))
    figures._left(2*pi/3)
    figures.draw_l("F", {"F": "F+F-F", },
                   {"+": figures.left(pi * 2 / 3), '-': figures.right(pi * 2 / 3), "F": figures.forward(50), }, 7,
                   (0, 0, 255), 2)
    img.save("D:\\Users\\louis chauvet\\Documents\\GitHub\\fractale\\test.bmp")
