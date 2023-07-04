#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: noet ts=4 ai number

import numpy as np
from primitives import Quat, Point, Polytope
phi = (1 + pow(5,1/2))/2 # golden ratio
qi = np.pi/2

# TODO stellations
# TODO inscribed_sphere
# TODO midradius

#################################
#								#
# platonic solids				#
#								#
#################################
class Polyhedron(Polytope):
	"""
		Functions to draw polyhedrae, where each face is a Polgygon
	"""
	def __init__( self, r, vertices, edges, faces, bounds = (-np.pi, np.pi), def_poly = None, **kwargs ):
		"""
			r: radius of circumscribed sphere (all vertices will be there)
			bounds : where to start and stop drawing points, relative to origin
			def_poly : default Polygon instance to use unless otherwise specified
		"""
		self.r = r
		self.bounds = bounds
		self.def_poly = def_poly

		super().__init__( vertices, edges, faces, name = kwargs.pop('name','Polytope') )

class Tetrahedron(Polyhedron):
	"""
		draws a Tetrahedron inside a sphere of radius 'r'
	"""
	num_vertices = 4
	num_edges = 6
	num_faces = 4
		
	def __init__( self, r = 1, *args, **kwargs ):
		# TODO vertices are wrong!! it is halfway to being an octahedron
		vertices = np.array([
				Quat( self, Quat( self, quat = Quat.new_polar( r, 0, -qi ) )),	# bottom vertex
				Quat( self, Quat( self, quat = Quat.new_polar( r, -2*pi/3, 0) )),
				Quat( self, Quat( self, quat = Quat.new_polar( r, 0, 0 ) )),						# center vertex
				Quat( self, Quat( self, quat = Quat.new_polar( r, 2*pi/3, 0) )),
				Quat( self, Quat( self, quat = Quat.new_polar( r, 0, qi ) )),	# top vertex
			])

		edges = []

		super().__init__( r,
				vertices, 
				edges = edges,
				faces = [[ edges[face[0]], edges[face[1]], edges[face[2]], edges[face[3]] ] for face in [
					#(6,8,0,14),
				]],
				name = 'Cube',
			*args, **kwargs )
		
class Cube(Polyhedron):
	"""
		draws a Cube inside a sphere of radius 'r'
	"""
	num_vertices = 8
	num_edges = 12
	num_faces = 6
		
	def __init__( self, r = 1, *args, **kwargs ):
		# TODO bounds ; we want to be able to draw a partial cube
		vertices = np.array([Point( self, quat = Quat.new_polar( r, delta*qi/2, echo*qi/2 )) for delta in (-2,-1,1,2) for echo in (-1,1)])

		edges = []
		for edge in [
		    (0, 1), (1, 2), (2, 3), (3, 0),  # top square
		    (0, 4), (1, 5), (2, 6), (3, 7),  # vertical edges
		    (4, 5), (5, 6), (6, 7), (7, 4),  # bottom square
		]:
			edges.append((vertices[edge[0]], vertices[edge[1]]))
			edges.append((vertices[edge[1]], vertices[edge[0]]))
		
		super().__init__( r,
				vertices, 
				edges = edges,
				faces = [[ edges[face[0]], edges[face[1]], edges[face[2]], edges[face[3]] ] for face in [
					(0,2,4,6),
					(0,2,10,8),
					(2,4,12,10),
					(4,6,14,12),
					(6,8,0,14),
					(16,18,20,22),
				]],
				name = 'Cube',
			*args, **kwargs )

		
class Octahedron(Polyhedron):
	"""
		draws an Octahedron inside a sphere of radius 'r'
	"""
	num_vertices = 6
	num_edges = 12
	num_faces = 8

	def __init__( self, *args, **kwargs ):
		super().__init__( self, *args, **kwargs )

		raise NotImplementedError
		
class Dodecahedron(Polyhedron):
	"""
		draws a Dodecahedron inside a sphere of radius 'r'
	"""
	num_vertices = 20
	num_edges = 30
	num_faces = 12

	def __init__( self, *args, **kwargs ):
		vertices = [ Point( self, quat = Quat.new_polar( p )) for p in [
			(r, np.arctan2(1, phi), np.arccos(1/phi)), # Vertex 0
			(r, np.arctan2(phi, 1), np.arccos(1/phi)), # Vertex 1
			(r, np.arctan2(phi, -1), np.arccos(1/phi)), # Vertex 2
			(r, np.arctan2(1, -phi), np.arccos(1/phi)), # Vertex 3
			(r, np.arctan2(-1, -phi), np.arccos(1/phi)), # Vertex 4
			(r, np.arctan2(-phi, -1), np.arccos(1/phi)), # Vertex 5
			(r, np.arctan2(-phi, 1), np.arccos(1/phi)), # Vertex 6
			(r, np.arctan2(-1, phi), np.arccos(1/phi)), # Vertex 7
			(r, np.arctan2(0, 1), np.arccos(phi)), # Vertex 8
			(r, np.arctan2(1, 0), np.arccos(phi)), # Vertex 9
			(r, np.arctan2(0, -1), np.arccos(phi)), # Vertex 10
			(r, np.arctan2(-1, 0), np.arccos(phi)), # Vertex 11
			(r, np.arctan2(1/phi, phi), np.arccos(phi)), # Vertex 12
			(r, np.arctan2(phi, 1/phi), np.arccos(phi)), # Vertex 13
			(r, np.arctan2(-phi, 1/phi), np.arccos(phi)), # Vertex 14
			(r, np.arctan2(-1/phi, phi), np.arccos(phi)), # Vertex 15
			(r, np.arctan2(1/phi, -phi), np.arccos(phi)), # Vertex 16
			(r, np.arctan2(-1/phi, -phi), np.arccos(phi)), # Vertex 17
			(r, np.arctan2(-phi, -1/phi), np.arccos(phi)), # Vertex 18
			(r, np.arctan2(phi, -1/phi), np.arccos(phi)), # Vertex 19
		]]

		edges = []
		for edge in [
			(0, 1), (0, 7), (0, 9), (1, 2), (1, 12),
			(2, 3), (2, 14), (3, 4), (3, 16), (4, 5),
			(4, 18), (5, 6), (5, 19), (6, 7), (6, 13),
			(7, 8), (8, 9), (8, 11), (9, 10), (10, 11),
			(10, 17), (11, 15), (12, 13), (12, 14), (13, 15),
			(14, 16), (15, 17), (16, 18), (17, 19), (18, 19)
		]:
			edges.append((vertices[edge[0]], vertices[edge[1]]))
			edges.append((vertices[edge[1]], vertices[edge[0]]))

		super().__init__( self,
				vertices, 
				edges = edges,
				faces = [ [ edges[face[0]], edges[face[1]], edges[face[2]], edges[face[3]], edges[face[4]] ] for face in [
					(0, 2, 4, 6, 8),
					(0, 14, 26, 16, 18),
					(2, 24, 28, 4, 10),
					(6, 32, 36, 8, 12),
					(14, 12, 38, 30, 26),
					(10, 38, 36, 32, 22),
					(16, 22, 34, 20, 18),
					(20, 34, 30, 28, 24)
				]],
				name = 'Dodecahedron',
			*args, **kwargs )


class Icosahedron(Polyhedron):
	"""
		draws an Icosahedron inside a sphere of radius 'r'
	"""
	num_vertices = 12
	num_edges = 30
	num_faces = 20

	def __init__( self, *args, **kwargs ):
		vertices = [ Point( self, quat = Quat.new_polar( p )) for p in (
			(phi, 0),
			(theta, pi/5),
			(theta, 3*pi/5),
			(theta, 5*pi/5),
			(theta, 7*pi/5),
			(theta, 9*pi/5),
			(-phi, 0),
			(-theta, pi/5),
			(-theta, 3*pi/5),
			(-theta, 5*pi/5),
			(-theta, 7*pi/5),
			(-theta, 9*pi/5),
		)]
		super().__init__( self,
				vertices, 
				edges = [NotImplementedError],
				faces = [NotImplementedError], 
				name = 'Icosahedron',
			*args, **kwargs )


