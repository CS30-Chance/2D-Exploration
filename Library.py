import pygame
import Settings


def drawBackground(surface, color):
    """Fill Background (TEST USE !!!)"""

    surface.fill(color)
    return None

def drawLine(surface, color, start: [int, int], end: [int, int], lineWidth: int):
    """Draw line on surface"""
    pygame.draw.line(surface, color, start, end, lineWidth)
    return None


def test_fun():
    print('hello world')
