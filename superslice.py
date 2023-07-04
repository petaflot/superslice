#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: noet ts=4 ai number

# requires Python3.6 because of f-strings!
VERSION_STRING = '0.1.2'


# TODO superslice.require( min_version, max_version = None )

"""

#from translation_system import *
from settings import *
from truecolor import fore_print, fore_text
color_red = (255,0,0)
color_white = (255,255,255)

try:
	from quaternion import quaternion
except ModuleNotFoundError:
	# module source at https://github.com/moble/quaternion
	pError("ModuleNotFoundError: run "+fore_text("pip install numpy-quaternion",color_white))
	raise

import numpy as np
qi = np.pi/2
import spirals


#################################
#								#
# development features			#
#								#
#################################
ENABLE_SUPERSEG = True
MIX_LINEAR = True
DEBUG = False
VERBOSE = False

#################################
#								#
# misc. definitions   			#
#								#
#################################
MAXNAME = 16
DIMS = 2	# first dim is xyz position
			# second dim is phase/extruder/COLOR
TRAVEL_ALPHA = .01	# alpha value for travel moves
LEFT = 1
RIGHT = 0

#################################
#								#
# utility functions				#
#								#
#################################
# debugging
import pprint
pp = pprint.PrettyPrinter(indent=4)

phi = (1+pow(5,1/2))/2

from cmath import exp
def polar( rho, theta ):
	'''converts 2D polar coordinates to complex cartesian'''
	return rho * exp(1j * theta)

from math import e
from numpy import pi as Pi
def rotate( vec, pi = 1 ):
	'''rotates a complex vector by a given multiple of Pi (1 is a half-turn)'''
	return e**(1j*Pi*pi)*vec

class NothingToShow(Exception): pass
"""


print("superslice test/example\n")

from primitives import Polytope, Polygon, Spiral, Parastichy
from platonic import Tetrahedron, Cube, Octahedron, Dodecahedron, Icosahedron
from tilings import TriGrid, QuadDrid, HexGrid, Penrose, Quasicrystal

shapes = [
		# Here are some Polytopes ; they have no faces, just Vertices
		#Spiral( 12, ('Ellipse', {'a': 1}) ),
		#Spiral( 12, ('Logarithmic', {'a':2, 'k':5, }) ),
		#Spiral( 12, ('Archimedean', {'a':2, }) ),
		#Spiral( 12, ('Hyperbolic', {'a':2, }) ),
		#Spiral( 12, ('Fermat', {'a':2, }) ),
		#Spiral( 12, ('Clothoid', {'a':2, }) ),
		#Spiral( 12, ('Lituus', {'a':2, }) ),

		#Spiral( 12, ('Clothoid', {'a':2, }) ),
		#Spiral( 12, ('Fibonacci', {'a':2, }) ),
		#Spiral( 12, ('Theodorus', {'a':2, }) ),
		#Spiral( 12, ('Involute', {'a':2, }) ),

		# Here are some Polygons
		#Tetrahedron(),
		Cube(),
		#Octahedron(),
		#Dodecahedron(),
		#Icosahedron(),
	]

for shape in shapes:
	print(shape)
	print()

