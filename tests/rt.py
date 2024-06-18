"""
Author: Bilal Vandenberge
Date: June 2024
-> Tests for source/read_theme.py
"""

# Color class tests:

import sys
sys.path.append('/home/B612/Devloper/2048/source')
from read_theme import Color, Theme, ColorError
import random

class TestColorClass:
    # def __init__(self):
    #     self._1()
    #     self._2()
    #     self._3()
    #     self._4()

    def test1(self):
        """
        check that the init works as expected
        """
        c1 = Color(0, 0, 0)
        c2 = Color(5, 67, 255)
        try:
            c3 = Color(256, -1, 5)
        except ColorError:
            pass # expected
        else:
            raise Exception("the Color class let the user use absurd rgb values")
    
    def test2(self):
        """
        check that the eq works as expected
        """
        c1 = Color(5, 150, 150)
        c2 = Color(5, 150, 150)
        c3 = Color(200, 0, 128)
        assert c1 == c2
        assert c2 != c3
        assert c1 != c3
    
    def test3(self):
        """
        check that the str works as expected
        """
        c1 = Color(0, 0, 0)
        c2 = Color(255, 253, 254)
        rand = [random.randint(0, 255) for _ in range(3)]
        c3 = Color(*rand)
        assert str(c1) == "rgb(0, 0, 0)"
        assert str(c2) == "rgb(255, 253, 254)"
        assert str(c3) == f"rgb{tuple(rand)}"

    def test4(self):
        """
        check that the int works as expected
        """
        c1 = Color(0, 0, 0)
        c2 = Color(255, 253, 254)
        rand = [random.randint(0, 255) for _ in range(3)]
        c3 = Color(*rand)
        assert int(c1) == 0
        assert int(c2) == 16776702
        assert int(c3) == (rand[0] << 16) + (rand[1] << 8) + (rand[2])

    def test5(self):
        """
        check that the colored method works as expected
        """
        c1 = Color(255, 0, 0)
        c1.colored("Hello") == "\x1b[48;2;255;0;0mHello\033[0m"

class TestThemeClass():
    
    def test1(self):
        """
        check that the init works as expected
        """
        t1 = Theme("themes/base.dmqu")
        t1.display()

if __name__ == "__main__":
    TestColorClass()
    TestThemeClass()