#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: noet ts=4 ai number

import numpy as np

def Ellipse( phi, **kwargs ):
	"""
		draws an Ellipse (or a circle)

		by default ellipse is centered on right focus point ; {'center': True} overrides this

		a: deviation from circle
			1/2 = Ellipse is twice as tall as it is wide
			1 = Circle
			2 = Ellipse is twice as wide as it is tall

	"""
	a = kwargs.pop('a',1)
	if not kwargs.pop('center', False):
		return a*(1-np.e**2)/(1+np.e*np.cos(phi))	# TODO defunct, screw LLMs
	else:
		return pow( a**2*(1-np.e**2)/(1-np.e**2*cos(pi)**2), 1/2 )	# TODO probably defunct too

def Logarithmic( phi, **kwargs ):
	"""
		the (smooth) spiral that looks the same regardless of the zoom level
	"""
	return kwargs['a']*np.exp(kwargs['k']*phi)

def Archimedean( phi, **kwargs ):
	"""
		the "roll-a-carpet" spiral
	"""
	return kwargs['a']*phi

def Hyperbolic( phi, **kwargs ):
	"""
		starts like Logarithmic but y-limit to kx
	"""
	return kwargs['a']/phi

def Fermat( phi, **kwargs ):
	"""
		sort-of like a symetric Archimedean spiral but not quite
	"""
	return kwargs['a']*pow(phi,1/2)

def Lituus ( phi, **kwargs ):
	"""
		sort-of Logarithmic but curvature inverts and y-limit to ~1/x
	"""
	return kwargs['a']*pow(phi,-1/2)

def Clothoid( phi, **kwargs ):
	"""
		also known as Euler or Cornu spiral

		used to make train track segments connect nicely
	"""
	raise NotImplementedError

def Fibonacci( phi, **kwargs ):
	"""
		also known as the Golden spiral (squares next to squares next to squares..)

		made of of bunch of Pi/2 arcs
	"""
	raise NotImplementedError

def Theodorus( phi, **kwargs ):
	"""
		the Theodorus spiral is an approximation of the Archimedean spiral composed of contiguous right triangles
	"""
	raise NotImplementedError

def Involute( phi, **kwargs ):
	"""
		the type that is used in cogs and gears
	"""
	raise NotImplementedError

