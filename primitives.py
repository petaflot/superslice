#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: noet ts=4 ai number

import quaternion
import numpy as np
qi = np.pi/2

def norm( vec ):
	""" norm of a cartesian vector """
	return pow( sum([pow(x,2) for x in vec]), 1/2 )

#################################
#								#
# base objects for everything	#
#								#
#################################
class Quat(np.quaternion):
	def __init__(self, *args, **kwargs):
		super().__init__( *args, **kwargs )

	@classmethod
	def new_cartesian( self, x_y_z_phi, y = None, z = None, phi = 0 ):
		"""
			return a quaternion from cartesian coordinates.
		"""
		try:
			x = x_y_z_phi[0]
			y = x_y_z_phi[1]
			z = x_y_z_phi[2]
			phi = x_y_z_phi[3]
		except TypeError:
			x = x_y_z_phi
		except IndexError:
			pass
		if y is None or z is None:
			raise ValueError("y and/or z is not set")
	
		return quaternion.from_euler_angles(
				atan(y/x),
				atan(z/norm(x,y)), 
				phi ) * pow(norm(x,y,z),1/2)

	@classmethod
	def new_polar( self, norm_echo_delta_phi, echo = None, delta = 0, phi = 0 ):
		"""
			return a quaternion from polar coordinates.
		"""
		try:
			norm = norm_echo_delta_phi[0]
		except (IndexError,TypeError):
			norm = norm_echo_delta_phi
		else:
			echo = norm_echo_delta_phi[1]
			try:
				delta = norm_echo_delta_phi[2]
				phi = norm_echo_delta_phi[3]
			except IndexError:
				pass
		if echo is None:
			raise ValueError("echo cannot be None")
		
		#print(f"{norm = }\t{echo = }\t{delta = }\t{phi = }")
		return pow(norm,1/2)*quaternion.from_euler_angles( echo, delta, phi )

class Point:
	"""
		a Point() is a fancy object where coordinates are expressed in quaternions

		a point has an orientation, it is basically a vector of zero length with
		additional properties allowing it to place it context with other Points
		and to enable fine control of arbitrary CNC machines.

		the standard for the axii definitions in the quaternions are shown in 
		doc/images/quaternion.svg

	"""
	def __init__(self, segment, normals = None, **kwargs ):
		"""
			segment: instance_of_the_segment 
			normals: a of with whatever properties are attached to the point
		"""
		#if type(segment) is np.quaternion: raise Exception
		self.segment = segment
		if normals is None:
			self._normals = {}
		else:
			self._normals = normals

		self._quat = kwargs.pop('quat', None)

	def __str__(self):
		return f"Point{self.components}"
	
	def __repr__(self):
		return f"<Point{self.components} 0x{hex(id(self))}>"

	@property
	def index(self):
		return self._index
		# yuk probably very slow because called often!
		#return f.vertices.index( point )
	
	@property
	def quat(self):
		# yuk probably slow downstream unless cached (with refresh rate problems)
		if self._quat is None:
			return self.segment._default_quat( self.index )
		elif str(type(self._quat)) == "<class 'function'>":
			return self._quat( *self.segment._omega_psi )
		else:
			return self._quat

	@property
	def components(self):
		return self.quat.components

	@property
	def norm(self):
		return self.quat.norm()
	
	def cog_offset(self, proj = (True, False)):
		"""
			offset to center of gravity of segment

			proj: respective to projection on omega and psi axii
				( False, False ): identity
				( True, False ): psi is fixed
				( False, True ): omega is fixed
				( True, True ): relative to full segment
		"""
		raise NotImplementedError

	@property
	def d(self):
		""" delta (azimuth/yaw on the horizontal plane, positive in the CCW direction) """
		#print(f"{self.components = }")
		return self.quat.a*pow(1j,-1/2)

	@property
	def e(self):
		""" echo (elevation/pitch relative to the origin) """
		return norm( (self.components[0], self.components[2]) )*qi

	@property
	def p(self):
		""" phi (roll relative to the horizon) """
		return norm( (self.components[0], self.components[3]) )*qi

	@property
	def polar(self):
		"""
			returns polar components without phi (roll axis)

			make sure to read the note on quaternion.as_euler_angles()
		"""
		return np.array([ self.d, self.e, self.quat.norm() ])

	@property
	def xyz(self):
		"""
			returns (x,y,z) components in the cartesian subsystem.

			make sure to read the note on quaternion.as_euler_angles()
		"""
		# projection on x-y plane (cartesian)
		xy = self.quat.norm() * np.cos(self.e)
		return np.array( [
				xy * np.cos(self.d),
				xy * np.sin(self.d),
				self.quat.norm() * np.sin(self.e)
			])
	

	@property
	def distance_to_next(self, same_segment = True ):
		""" absolute distance to the next point in the Segment

		if point is last in Segment:
			if same_segment == True, returns None for last point in Segment (travel move)
			if same_segment == False, tries to find the length of the travel move to the next Segment
		"""
		try:
			nextseg = self.segment[0][self.segment[1]+1]
		except IndexError:
			if same_segment is True:
				return None
			else:
				raise Exception("TODO")
		else:
			return norm( nextseg.xyz - self.xyz )

	@property
	def flat_normal(self):
		""" the bissector of the angle between the vectors to the previous and next points in Segment
			this is close to the local acceleration vector of a point along this curve
		"""
		raise Exception("TODO")

	def pseudonormal_to(self, target):
		""" a normalized vector (length 1) directed to another point in space ; useful for cameras

		target is a quaternion

		norm of return value is likely _never_ to be exactly one (recursion/float precision)
		"""
		vector_to = target - self
		return vector_to/vector_to.abs()


	"""
		geometric transforms
	"""
	def rotate(self, delta_echo_phi, echo = None, phi = None):
		"""
			TODO

			rotate point by Euler angles, relative to origin
		"""
		return self
	
	@classmethod
	def translate(self, xyz, y = None, z = None):
		"""
			translate point by x,y,z vector, relative to coordinate system. phi stays fixed.
		"""
		try:
			x, y, z = xyz
		except IndexError:
			x = xyz

		self.quat = new_cartesian( self.xyz + xyz, phi = self.phi )
		return self

	@classmethod
	def scale(self, f ):
		"""
			"resize" point by a factor f, relative to origin
		"""
		self.quat *= pow(f,1/2)
		return self
	
	@classmethod
	def pinch(self, f):
		"""
			'pinch' reduces the angles while maintaining the norm
	
			it can be seen as the complement of the 'scale' method

			f: factor to pinch
				float:					echo, delta
				(float, float):			echo, delta
				(float, float, float):	echo, delta, phi
		"""
		if type(f) is int:
			self.quat = Quat.new_polar( self.norm, self.e*f, self.d*f, self.phi )
		else:
			match len(f):
				case 2:
					self.quat = Quat.new_polar( self.norm, self.e*f[0], self.d*f[1], self.phi )
				case 3:
					self.quat = Quat.new_polar( self.norm, self.e*f[0], self.d*f[1], self.phi*f[2] )

		return self



class Polytope:
	"""
		a Polytope is an oriented solid ; it has :

		* an inside and an outside (by default, this can be overriden per-face)
		* a number of vertices (singularities that lay on edges AND on faces)
		* a number of edges that join vertices two-by-two ; the total number of edges
		  needs not be equal to the total number of combinations of vertices
		* a number of faces that are a looped sequence of vertices ; the orientation 

		TODO: area, volume
	"""
	def __init__( self, vertices, edges, faces, *, 
			gamma_range = (( 0, qi, np.linspace ), ( 0, qi, np.linspace)),	# third argument is len(self.vertices)
			steps = 3,	# how many "steps" or layers to use for gamma.imag ("elevation")
			name = 'Polytope' ):
		self.vertices = vertices
		self.edges = edges
		self.faces = faces
		self.steps = steps
		self.name = name

		self._gamma_range = gamma_range
		self.range_reset()
	
	def range_reset(self):
		"""
			must be called after the number of vertices is changed
		"""
		self.len = len(self.vertices)

		self.gammas = [ self._gamma_range[0][2]( self._gamma_range[0][0], self._gamma_range[0][1], self.len ),
			self._gamma_range[1][2]( self._gamma_range[1][0], self._gamma_range[1][1], self.steps ) ]

		for i in range(self.len):
			# in case of update problems, make _index a property with setter
			self.vertices[i]._index = i
	
	def __str__( self ):
		return f"{self.name} (F={self._faces},E={len(self.edges)},V={len(self.vertices)})"
	
	def _gamma(self, point_index):
		# TODO not sure about return value % and //
		return self.gammas[0][point_index%self.len]# + self.gammas[1][point_index//l]*1j	TODO .imag reserved for Surface (SuperSeg)
	
	@property
	def _faces(self):
		try:
			return len(self.faces)
		except TypeError:
			return 'n/a'


#################################
#								#
# flat shape generators		 	#
#								#
#################################
class Polygon(Polytope):
	def __init__( self, r = 1, vertices = 6, convexity = 1, arange = (-np.pi, np.pi), resolution = 1 ):
		''' draws a circle, a square, a triangle, a star..

		although flat by default, a Polygon is a Polytope that can be "inflated" with an elevation_func TODO

		r = radius of circle
		vertices = number of dots (aka "obvious resolution")
		convexity = how many dots to skip when connecting polygon
		alpha = number of half-turns of the polygon (Pi multiplicator ; 2*Pi is one full rotation), a value of 1 will make a half-circle with `sides` sides
		resolution = how many subdivisions for a single segment (see resolution_func() )

		'''

import spirals

class Spiral(Polytope):
	"""
		although flat by default, a Spiral is a Polytope that can be "inflated" with an elevation_func TODO, allowing to
		generate (but not limited to) conical and spherical spirals

		draws a spiral, one of:

		'Ellipse'
		'Logarithmic' (the default)
		'Archimedean'
		'Hyperbolic'
		'Fermat'
		'Lituus '
		'Clothoid'
		'Fibonacci'
		'Theodorus'
		'Involute'
		other: specify function of Phi [-inf;inf] or tan([-qi;qi])

		npts : number of points on the spiral
		func : default to ['Logarithmic', None, None] ; [0] is friendly name, [1] is dict of args, [2] is function (optional)

		see https://en.wikipedia.org/wiki/Spiral
	"""
	def __init__(self, vertices, func, **kwargs ):
		"""
			vertices: number of vertices, or a list of vertices
			func: a tuple ( 'ArbitraryName', func_args, [ func, ] ) where func_args is a dict, func is called as func( phi, func_args )
		"""
		match func[0]:
			case 'Ellipse':
				self.func = spirals.Ellipse
			case 'Logarithmic':
				self.func = spirals.Logarithmic
			case 'Archimedean':
				self.func = spirals.Archimedean
			case 'Hyperbolic':
				self.func = spirals.Hyperbolic
			case 'Fermat':
				self.func = spirals.Fermat
			case 'Lituus':
				self.func = spirals.Lituus
			case 'Clothoid':
				self.func = spirals.Clothoid
			case 'Fibonacci':
				self.func = spirals.Fibonacci

			case 'Theodorus':
				self.func = spirals.Theodorus
			case 'Involute':
				self.func = spirals.Involute
			case other:
				self.func = func[2]
		self.fargs = func[1]

		if str(type(self.func)) != "<class 'function'>":
			print(f"ERROR, not a function: {self.func}")
			raise Exception
		if type(self.fargs) is not dict:
			print(f"ERROR, not a dict: {self.dict}")
			raise Exception

		if type(vertices) is int:
			vertices = [Point(self) for _ in range(vertices)]

		super().__init__( vertices, 
				edges = [(vertices[i], vertices[i+1]) for i in range(len(vertices)-1)],
				faces = NotImplementedError,
				name = func[0]
			)
	
	def __repr__(self):
		return f"<{self.name} Spiral 0x{hex(id(self))}, V={len(self.vertices)} {self.fargs} 0x{hex(id(self.func))}>"
	
	def _default_quat(self, index):
		# yuk that reeks like memleaks and lots of CPU for new quaternion instances
		# TODO won't do any sort of interpolation between segments -> .imag
		return Quat.new_polar( self.func( self._gamma( index ).real, **self.fargs ), self._gamma( index ).real )

class Parastichy(Polytope):
	"""
		draws a path that follows a Parastichy https://en.wikipedia.org/wiki/Parastichy

		(connects the seeds of a sunflower)
	"""
	def __init__(self, npts, **kwargs ):
		#self.samples = np.linspace( self.start, self.stop, npts)
		r = pow(self.samples,1/2)
		#vertices = [ Point( self, quat = quaternion.from_euler_angles( rr, 2*rr*np.pi )) for rr in r]
		raise NotImplementedError

		super().__init__( vertices,
				edges = [(vertices[i], vertices[i+1]) for i in range(len(vertices)-1)],
				faces = NotImplementedError,
				**kwargs )

	def rotate(self):
		raise NotImplementedError

	def translate(self):
		raise NotImplementedError

	def homotecy(self):
		raise NotImplementedError

