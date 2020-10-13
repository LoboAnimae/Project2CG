'''
NOT ALL THE CODE INSIDE THIS PROJECT WAS MY IDEA/IS MINE. A LOT OF IT
IS FROM DENNIS' CLASS AND SOME IS INSPIRED BY ONLINE SOLUTIONS.
'''

import time
from ray import Raytracer
from classes import *
from datamodifiers import *

# colors & Materials


water = Material(diffuse=color(100, 100, 160), albedo=(
    0, 0.5, 0.1, 0.8), spec=125, refractive_index=1.5)
sand = Material(active_texture=Texture('./sand.bmp'))
cactus = Material(active_texture=Texture('./cactus.bmp'))
sun = Material(diffuse=color(255, 255, 255), albedo=(
    1, 0, .1, 1), spec=1000,
)
sun_disk_1 = Material(diffuse=color(255, 255, 255), albedo=(
    0, 0.5, .1, 1), spec=1000, refractive_index=2)
obsidian = Material(active_texture=Texture('./obsidian.bmp'))
obsidian_color = Material(diffuse=color(16, 16, 24),
                          albedo=(0.9, 0.1, 0, 0), spec=1,)
displacement = 4
# Render
camera = V3(0, 1, -1)
background = textureprocessor('./sky.bmp')
light = Light(position=V3(0, 2, 0.2), intensity=1.5)
environment = environment(intensity=0.1)
background_color = color(124, 169, 254)
r = Raytracer(768, 432, camera, background, light,
              environment, background_color)

r.scene = [

    Cube(V3(-4.5,       -1.5,               -6),            1.5,        sand),
    Cube(V3(-3,         -1.5,               -6),            1.5,        sand),
    Cube(V3(-1.5,         -1.5,             -6),            1.5,        sand),
    Cube(V3(0,         -1.5,                -6),            1.5,        sand),
    Cube(V3(1.5,         -1.5,              -6),            1.5,        sand),
    Cube(V3(3,         -1.5,                -6),            1.5,        sand),
    Cube(V3(4.5,         -1.5,              -6),            1.5,        sand),

    Cube(V3(3,         -1.5,              -12),            1.5,        sand),
    Cube(V3(4.5,         -1.5,              -12),            1.5,        sand),
    Cube(V3(6,         -1.5,              -12),            1.5,        sand),
    Cube(V3(7.5,         -1.5,              -12),            1.5,        sand),
    Cube(V3(9,         -1.5,              -10.5),            1.5,        sand),
    Cube(V3(9,         -1.5,              -9),            1.5,        sand),
    Cube(V3(9,         -1.5,              -7.5),            1.5,        sand),
    Cube(V3(1.5,         -1.5,              -10.5),            1.5,        sand),
    Cube(V3(-1.5,         -1.5,              -8),            1.5,        sand),
    Cube(V3(-3,         -1.5,              -8),            1.5,        sand),
    Cube(V3(-4.5,         -1.5,              -8),            1.5,        sand),

    Cube(V3(-4.5,       -1.5,               -7),            1.5,        sand),
    Cube(V3(-3,         -1.5,               -7),            1.5,        sand),
    Cube(V3(-1.5,         -1.5,             -7),            1.5,        sand),
    Cube(V3(0,         -1.5,                -7),            1.5,        sand),
    Cube(V3(1.5,         -1.5,              -7),            1.5,        sand),
    Cube(V3(3,         -1.5,                -7),            1.5,        sand),
    Cube(V3(4.5,         -1.5,              -7),            1.5,        sand),
    Cube(V3(1.5,         -1.5,              -12),            1.5,        sand),
    Cube(V3(0,         -1.5,              -10.5),            1.5,        sand),
    Cube(V3(4.5,         0,              -13.5),            1.5,        sand),
    Cube(V3(6,         0,              -13.5),            1.5,        sand),
    Cube(V3(7.5,         0,              -13.5),            1.5,        sand),
    Cube(V3(9,         0,              -12),            1.5,        sand),
    Cube(V3(3,         0,              -15),            1.5,        sand),
    Cube(V3(1.5,         0,              -15),            1.5,        sand),
    Cube(V3(0,         0,              -15),            1.5,        sand),
    Cube(V3(-1.5,         0,              -15),            1.5,        sand),
    Cube(V3(-3,         0,              -15),            1.5,        sand),
    Cube(V3(-4.5,         0,              -15),            1.5,        sand),
    Cube(V3(-6,         0,              -15),            1.5,        sand),
    Cube(V3(-1.5,         -1.5,              -15),            1.5,        sand),
    Cube(V3(-3,         -1.5,              -15),            1.5,        sand),
    Cube(V3(-4.5,         -1.5,              -15),            1.5,        sand),
    Cube(V3(-6,         -1.5,              -15),            1.5,        sand),

    Cube(V3(-6,         -1.5,              -13.5),            1.5,        water),
    Cube(V3(-6,         -1.5,              -12),            1.5,        water),
    Cube(V3(-4.5,         -1.5,              -12),            1.5,        water),
    Cube(V3(-4.5,         -1.5,              -13.5),            1.5,        water),
    Cube(V3(-3,         -1.5,              -12),            1.5,        water),
    Cube(V3(-3,         -1.5,              -13.5),            1.5,        water),
    Cube(V3(-1.5,         -1.5,              -12),            1.5,        water),
    Cube(V3(-4.5,         -1.5,              -5),            1.5,        water),
    Cube(V3(-3,         -1.5,              -5),            1.5,        water),
    Cube(V3(-1.5,         -1.5,              -5),            1.5,        water),
    Cube(V3(-0,         -1.5,              -5),            1.5,        water),
    Cube(V3(1.5,         -1.5,              -5),            1.5,        water),
    Cube(V3(3,         -1.5,              -5),            1.5,        water),
    Cube(V3(4.5,         -1.5,              -5),            1.5,        water),
    Cube(V3(6,         -1.5,              -5),            1.5,        water),

    Cube(V3(-3,         -1.5,              -3.5),            1.5,        water),
    Cube(V3(-1.5,         -1.5,              -3.5),            1.5,        water),
    Cube(V3(-0,         -1.5,              -3.5),            1.5,        water),
    Cube(V3(1.5,         -1.5,              -3.5),            1.5,        water),
    Cube(V3(3,         -1.5,              -3.5),            1.5,        water),

    Cube(V3(-3,         -1.5,              -2),            1.5,        water),
    Cube(V3(-1.5,         -1.5,              -2),            1.5,        water),
    Cube(V3(-0,         -1.5,              -2),            1.5,        water),
    Cube(V3(1.5,         -1.5,              -2),            1.5,        water),
    Cube(V3(3,         -1.5,              -2),            1.5,        water),

    Cube(V3(-3,         -1.5,              -0.5),            1.5,        water),
    Cube(V3(-1.5,         -1.5,              -0.5),            1.5,        water),
    Cube(V3(-0,         -1.5,              -0.5),            1.5,        water),
    Cube(V3(1.5,         -1.5,              -0.5),            1.5,        water),
    Cube(V3(3,         -1.5,              -0.5),            1.5,        water),


    Cube(V3(-3, 0, -7), 1.5, cactus),
    Cube(V3(1.5, 0, -12), 1.5, cactus),
    Cube(V3(1.5, 1.5, -12), 1.5, cactus),
    Cube(V3(0, 0, -10.5), 1.5, cactus),
    Cube(V3(4.5,         1.5, -16.5), 1.5, cactus),
    Cube(V3(-3, 1.5, -7), 1.5, obsidian),
    Cube(V3(1.5, 3, -12), 1.5, obsidian),
    Cube(V3(4.5, 3, -16.5), 1.5,        obsidian),

    Pyramid([V3(-9.5, 0.5 - displacement, -11), V3(-6.5, 0.5 - displacement, -11),
             V3(-9.8, 0.8 - displacement, -11.5), V3(-8, 3.4 - displacement, -11.5), ], obsidian_color),
    Pyramid([V3(-9.5 + (displacement * 3), 0.5 - 2, -11), V3(-6.5 + (displacement * 3), 0.5 - 2, -11),
             V3(-9.8 + (displacement * 3), 0.8 - 2, -11.5), V3(-8 + (displacement * 3), 3.4 - 2, -11.5), ], obsidian_color),


    Cube(V3(0,         3.5,                  -10.5),            1.5,        sun),
    Cube(V3(0,         3.4,                  -9),
         2.4,        sun_disk_1),
]

r.render('output_strange_place.bmp')
