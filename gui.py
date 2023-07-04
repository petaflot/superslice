#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: noet ts=4 ai number
# -----------------------------------------------------------------------------
# Copyright (c) JCZD@ / engrenage. All Rights Reserved.
# Copyright (c) Vispy Development Team. All Rights Reserved.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
"""
Use VisPy to display an Object

https://github.com/vispy/vispy/
"""

LINE_RENDERING_CORRECT = False

import numpy as np

from vispy import scene, app
from vispy.geometry import meshdata as MeshData
from vispy.scene.visuals import Mesh, MeshNormals
from vispy.visuals.filters import WireframeFilter
from vispy.color.colormap import get_colormaps

from sys import exit as sysexit


try:
	from sip import setapi
	setapi("QVariant", 2)
	setapi("QString", 2)
except ImportError:
	pass

try:
	from PyQt4 import QtCore
	from PyQt4.QtCore import Qt
	from PyQt4.QtGui import (QMainWindow, QWidget, QLabel,
							 QSpinBox, QComboBox, QGridLayout, QVBoxLayout,
							 QSplitter, QPushButton)
except Exception:
	# To switch between PyQt5 and PySide2 bindings just change the from import
	from PyQt5 import QtCore
	from PyQt5.QtCore import Qt
	from PyQt5.QtWidgets import (QMainWindow, QWidget, QLabel,
								 QSpinBox, QComboBox, QGridLayout, QVBoxLayout,
								 QSplitter, QSizePolicy, QApplication, QPushButton)

# Provide automatic signal function selection for PyQtX/PySide2
pyqtsignal = QtCore.pyqtSignal if hasattr(QtCore, 'pyqtSignal') else QtCore.Signal

style_h0 = "QLabel {background-color: #a0a0a0; font-weight: bold;}"
style_h1 = "QLabel {font-weight: bold;}"
style_TODO = "QLabel {font-style: italic; color: #c0c0c0}"

import superslice

class ObjectWidget(QWidget):
	"""
	Widget for editing OBJECT parameters
	"""
	signal_object_changed = pyqtsignal(name='objectChanged')

	def __init__(self, canvas, parent=None):
		super(ObjectWidget, self).__init__(parent)
		self.canvas = canvas

		gbox = QGridLayout()
		i = 0

		l = QLabel("Object options")
		l.setStyleSheet(style_h0)
		gbox.addWidget(l, i, 0, 1,2)
		i += 1
		l = QLabel("ObjectName")
		l.setStyleSheet(style_TODO)
		gbox.addWidget(l, i, 0)
		i += 1
		# TODO popoulate from class
		l = QLabel("Foo")
		self.foo = QSpinBox()
		self.foo.setMinimum(0)
		self.foo.setMaximum(180)
		self.foo.setValue(45)
		self.foo.valueChanged.connect(self.update_param)
		gbox.addWidget(l, i, 0)
		gbox.addWidget(self.foo, i, 1)
		i += 1
		l = QLabel("Bar")
		self.bar = QSpinBox()
		self.bar.setMinimum(0)
		self.bar.setMaximum(180)
		self.bar.setValue(45)
		self.bar.valueChanged.connect(self.update_param)
		gbox.addWidget(l, i, 0)
		gbox.addWidget(self.bar, i, 1)
		i += 1

		l = QLabel("Viewing options")
		l.setStyleSheet(style_h0)
		gbox.addWidget(l, i, 0, 1,2)
		i += 1
		l = QLabel("Point-of-View")
		l.setStyleSheet(style_TODO)
		gbox.addWidget(l, i, 0)
		# Reset view
		# Save view -> view list
		# Center view
		# Front
		# Back
		# Left
		# Right
		# Top
		# Bottom
		i += 1
		l = QLabel("elevation/azimuth/roll center/distance/depth")
		l.setStyleSheet(style_TODO)
		gbox.addWidget(l, i, 0, 1,2)
		i += 1
		l = QLabel("Field-of-View")
		self.fov = QSpinBox()	# TODO allow floats?
		self.fov.setMinimum(0)
		self.fov.setMaximum(180)
		self.fov.setValue(0)	# TODO get value from camera
		self.fov.valueChanged.connect(self.update_param)
		gbox.addWidget(l, i, 0)
		gbox.addWidget(self.fov, i, 1)
		i += 1
		l = QLabel("Show")
		l.setStyleSheet(style_TODO)
		self.show = ['Segments', 'Segments + Faces', 'Faces']
		self.show = QComboBox(self)
		self.show.addItems(['Segments', 'Segments + Faces', 'Faces'])
		self.show.currentIndexChanged.connect(self.update_param)
		gbox.addWidget(l, i, 0)
		gbox.addWidget(self.show, i, 1)
		i += 1
		l = QLabel("Normals")
		self.normals = ['None', 'Faces', 'Edges', 'Both']
		self.normals = QComboBox(self)
		self.normals.addItems(['None', 'Faces', 'Both', 'Vertices'])
		self.normals.currentIndexChanged.connect(self.update_param)
		gbox.addWidget(l, i, 0)
		gbox.addWidget(self.normals, i, 1)
		i += 1
		l = QLabel("Shading")
		self.shading = QComboBox(self)
		self.shading.addItems(['Flat', 'Smooth', 'None'])
		self.shading.currentIndexChanged.connect(self.update_param)
		gbox.addWidget(l, i, 0)
		gbox.addWidget(self.shading, i, 1)
		i += 1
		l = QLabel("Color map")
		l.setStyleSheet(style_TODO)
		self.cmap = QComboBox(self)
		self.cmap.addItems(sorted(get_colormaps().keys()))
		self.cmap.currentIndexChanged.connect(self.update_param)
		gbox.addWidget(l, i, 0)
		gbox.addWidget(self.cmap, i, 1)
		i += 1


		l = QLabel("Layer clipping")
		l.setStyleSheet(style_h0)
		gbox.addWidget(l, i, 0, 1,2)
		i += 1
		# TODO
		# - operation AND/OR
		# - reset
		# - enable/disable
		"""
		l = QLabel("Horizontal (X)")
		l.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		l.setAlignment(Qt.AlignCenter)
		#l.setStyleSheet(style_h1)
		l.setStyleSheet(style_TODO)
		gbox.addWidget(l, i, 0, 1,2)
		i += 1

		l = QLabel("Front")
		l.setStyleSheet(style_TODO)
		self.start_layer_x = QSpinBox()
		self.start_layer_x.setMinimum(box[2][0])
		self.start_layer_x.setMaximum(box[2][1])
		self.start_layer_x.setValue(box[2][0])
		self.start_layer_x.valueChanged.connect(self.update_param)
		gbox.addWidget(l, i, 0)
		gbox.addWidget(self.start_layer_x, i, 1)
		i += 1

		l = QLabel("Back")
		l.setStyleSheet(style_TODO)
		self.stop_layer_x = QSpinBox()
		self.stop_layer_x.setMinimum(box[2][0])
		self.stop_layer_x.setMaximum(box[2][1])
		self.stop_layer_x.setValue(box[2][1])
		self.stop_layer_x.valueChanged.connect(self.update_param)
		gbox.addWidget(l, i, 0)
		gbox.addWidget(self.stop_layer_x, i, 1)
		i += 1

		l = QLabel("Horizontal (Y)")
		l.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		l.setAlignment(Qt.AlignCenter)
		#l.setStyleSheet(style_h1)
		l.setStyleSheet(style_TODO)
		gbox.addWidget(l, i, 0, 1,2)
		i += 1

		l = QLabel("Right")
		l.setStyleSheet(style_TODO)
		self.start_layer_y = QSpinBox()
		self.start_layer_y.setMinimum(box[2][0])
		self.start_layer_y.setMaximum(box[2][1])
		self.start_layer_y.setValue(box[2][0])
		self.start_layer_y.valueChanged.connect(self.update_param)
		gbox.addWidget(l, i, 0)
		gbox.addWidget(self.start_layer_y, i, 1)
		i += 1

		l = QLabel("Left")
		l.setStyleSheet(style_TODO)
		self.stop_layer_y = QSpinBox()
		self.stop_layer_y.setMinimum(box[2][0])
		self.stop_layer_y.setMaximum(box[2][1])
		self.stop_layer_y.setValue(box[2][1])
		self.stop_layer_y.valueChanged.connect(self.update_param)
		gbox.addWidget(l, i, 0)
		gbox.addWidget(self.stop_layer_y, i, 1)
		i += 1
		"""
		l = QLabel("Paths")
		l.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		l.setAlignment(Qt.AlignCenter)
		l.setStyleSheet(style_h1)
		#l.setStyleSheet(style_TODO)
		gbox.addWidget(l, i, 0, 1,2)
		i += 1

		l = QLabel("Bottom ")
		#l.setStyleSheet(style_TODO)
		self.paths_start_layer_z = QSpinBox()
		self.paths_start_layer_z.setMinimum(0)
		#TODO self.paths_start_layer_z.setMaximum(self.canvas.P.totallayers)
		self.paths_start_layer_z.setMaximum(10)
		self.paths_start_layer_z.setValue(0)
		self.paths_start_layer_z.valueChanged.connect(self.update_param)
		gbox.addWidget(l, i, 0)
		gbox.addWidget(self.paths_start_layer_z, i, 1)
		i += 1

		l = QLabel("Top ")
		#l.setStyleSheet(style_TODO)
		self.paths_stop_layer_z = QSpinBox()
		self.paths_stop_layer_z.setMinimum(0)
		#TODO self.paths_stop_layer_z.setMaximum(self.canvas.P.totallayers)
		self.paths_stop_layer_z.setMaximum(10)
		#TODO self.paths_stop_layer_z.setValue(self.canvas.P.totallayers)
		self.paths_stop_layer_z.setValue(10)
		self.paths_stop_layer_z.valueChanged.connect(self.update_param)
		gbox.addWidget(l, i, 0)
		gbox.addWidget(self.paths_stop_layer_z, i, 1)
		i += 1

		l = QLabel("Faces")
		l.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		l.setAlignment(Qt.AlignCenter)
		l.setStyleSheet(style_h1)
		#l.setStyleSheet(style_TODO)
		gbox.addWidget(l, i, 0, 1,2)
		i += 1

		l = QLabel("Bottom ")
		#l.setStyleSheet(style_TODO)
		self.faces_start_layer_z = QSpinBox()
		self.faces_start_layer_z.setMinimum(0)
		#TODO self.faces_start_layer_z.setMaximum(self.canvas.P.totallayers-1)
		self.faces_start_layer_z.setMaximum(10)
		self.faces_start_layer_z.setValue(0)
		self.faces_start_layer_z.valueChanged.connect(self.update_param)
		gbox.addWidget(l, i, 0)
		gbox.addWidget(self.faces_start_layer_z, i, 1)
		i += 1

		l = QLabel("Top ")
		#l.setStyleSheet(style_TODO)
		self.faces_stop_layer_z = QSpinBox()
		self.faces_stop_layer_z.setMinimum(0)
		#TODO self.faces_stop_layer_z.setMaximum(self.canvas.P.totallayers-1)
		self.faces_stop_layer_z.setMaximum(10)
		#TODO self.faces_stop_layer_z.setValue(self.canvas.P.totallayers-1)
		self.faces_stop_layer_z.setValue(10)
		self.faces_stop_layer_z.valueChanged.connect(self.update_param)
		gbox.addWidget(l, i, 0)
		gbox.addWidget(self.faces_stop_layer_z, i, 1)
		i += 1

		l = QLabel("Slicing options")
		l.setStyleSheet(style_h0)
		gbox.addWidget(l, i, 0, 1,2)
		i += 1
		l = QLabel("Layer height")	# TODO we may want this to be dynamic!
		l.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		l.setStyleSheet(style_TODO)
		gbox.addWidget(l, i, 0, 1,2)
		i += 1

		l = QLabel("Export")
		l.setStyleSheet(style_h0)
		gbox.addWidget(l, i, 0, 1,2)
		i += 1
		l = QLabel("G-Code")
		l.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		l.setAlignment(Qt.AlignCenter)
		#l.setStyleSheet(style_h1)
		l.setStyleSheet(style_TODO)
		gbox.addWidget(l, i, 0, 1,2)
		i += 1
		l = QLabel("PNG")
		l.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		l.setAlignment(Qt.AlignCenter)
		#l.setStyleSheet(style_h1)
		l.setStyleSheet(style_TODO)
		gbox.addWidget(l, i, 0, 1,2)
		i += 1
		l = QLabel("SVG")
		l.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		l.setAlignment(Qt.AlignCenter)
		#l.setStyleSheet(style_h1)
		l.setStyleSheet(style_TODO)
		gbox.addWidget(l, i, 0, 1,2)
		i += 1
		l = QPushButton("Wavefront OBJ")
		l.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		#TODO l.clicked.connect(self.canvas.P.export_obj)
		#l.setAlignment(Qt.AlignCenter)
		#l.setStyleSheet(style_h1)
		gbox.addWidget(l, i, 0, 1,2)
		i += 1

		l = QLabel("Machine")
		l.setStyleSheet(style_h0)
		gbox.addWidget(l, i, 0, 1,2)
		i += 1
		l = QLabel("Choose from list")
		l.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		l.setAlignment(Qt.AlignCenter)
		#l.setStyleSheet(style_h1)
		l.setStyleSheet(style_TODO)
		gbox.addWidget(l, i, 0, 1,2)
		i += 1
		l = QLabel("Configure")
		l.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		l.setAlignment(Qt.AlignCenter)
		#l.setStyleSheet(style_h1)
		l.setStyleSheet(style_TODO)
		gbox.addWidget(l, i, 0, 1,2)
		i += 1
		l = QLabel("Control")
		l.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		l.setAlignment(Qt.AlignCenter)
		#l.setStyleSheet(style_h1)
		l.setStyleSheet(style_TODO)
		gbox.addWidget(l, i, 0, 1,2)
		i += 1



		vbox = QVBoxLayout()
		vbox.addLayout(gbox)
		vbox.addStretch(1)

		self.setLayout(vbox)

	def update_param(self, option):
		self.signal_object_changed.emit()
	
class MainWindow(QMainWindow):

	def __init__(self):
		QMainWindow.__init__(self)

		self.setWindowTitle('Superslice')
		self.resize(1900, 1040)
		#self.showMaximized()	# doesn't work :-(

		splitter = QSplitter(Qt.Horizontal)

		self.canvas = Canvas()
		self.canvas.create_native()
		self.canvas.native.setParent(self)

		#self.setWindowTitle(' - '.join(['Superslice', self.canvas.P.name]))
		self.setWindowTitle(' - '.join(['Superslice', ]))

		self.props = ObjectWidget( canvas = self.canvas )
		splitter.addWidget(self.props)
		splitter.addWidget(self.canvas.native)

		self.setCentralWidget(splitter)
		self.props.signal_object_changed.connect(self.update_view)
		self.update_view()

		self.timer = app.Timer(1, connect=self.on_timer, start=True)

		@self.canvas.events.key_press.connect
		def on_key_press(event):
			modifiers = QApplication.keyboardModifiers()
			if event.key == 'f':
				self.canvas.face_normals.visible = not self.canvas.face_normals.visible
				self.canvas.update()
			elif event.key == 'v':
				self.canvas.vertex_normals.visible = not self.canvas.vertex_normals.visible
				self.canvas.update()
			elif (event.key == 'q' and modifiers == QtCore.Qt.ControlModifier) or (event.key == 'F4' and modifiers == QtCore.Qt.AltModifier):
				sysexit()
			elif (event.key == 'r' and modifiers == QtCore.Qt.ControlModifier) or event.key == 'F5':
				self.reload_slice()
			#else:
			#	print('Pressed', modifiers, event.key, "(not bound to anything)")

	def update_view(self):
		shading = {'None': None, 'Flat': 'flat', 'Smooth': 'smooth', }

		self.canvas.set_data(
				# layer clipping
				( self.props.paths_start_layer_z.value(), self.props.paths_stop_layer_z.value(), self.props.faces_start_layer_z.value(), self.props.faces_stop_layer_z.value()),
				# color map
				self.props.cmap.currentText(),
				self.props.fov.value(),
				shading[self.props.shading.currentText()],
				self.props.normals.currentText(),
			)

	def reload_slice(self):
		from importlib import reload
		reload(superslice)
		reload(ss)
		self.canvas.P = ss.shapes[0]
		self.canvas.points = self.canvas.P.get_points()
		self.props.paths_start_layer_z.setMaximum(self.canvas.P.totallayers)
		self.props.paths_stop_layer_z.setMaximum(self.canvas.P.totallayers)
		self.props.faces_start_layer_z.setMaximum(self.canvas.P.totallayers-1)
		self.props.faces_stop_layer_z.setMaximum(self.canvas.P.totallayers-1)
		self.update_view()

	def on_timer(self, event):
		''' checks file for modifications and reload source script '''
		import os.path
		global slice_file
	
		print("ping")
	
		try:
			if os.path.getmtime(slice_file) > self.slice_mtime:
				self.reload_slice()
		except AttributeError:
			# first run at startup ; not a big deal, it prevents having to import os.path somewhere else and have duplicate code
			print("first run, setting slice_mtime ; we don't need to reload module anyway because we just loaded it (another reason to not set slice_mtime before)")
			pass
		except FileNotFoundError:
			# file is probably being rewritten right now.. we simply wait until the next iteration
			print("waiting for file to become available")
			pass
		finally:
			try:
				self.slice_mtime = os.path.getmtime(slice_file)
			except FileNotFoundError:
				# file is probably still being rewritten
				print("still waiting for file to become available")
				pass


class Canvas(scene.SceneCanvas):
	def __init__(self):

		scene.SceneCanvas.__init__(self, keys=None)
		self.size = 800, 600
		self.unfreeze()
		self.view = self.central_widget.add_view()
		self.view.camera = 'turntable'

		#self.points = []
		#for shape in ss.shapes:
		#	self.points.extend([p.xyz for p in shape.vertices])
		#	faces = shape.faces
		#	#self.P = ss.shapes[0]
		#	#self.points = self.P.get_points()	# ALL the points, required for the mesh
		#	#faces = self.P.get_mesh()
		#	#points = self.P.get_points()
		from vispy.geometry.generation import create_sphere
		mesh = create_sphere(20, 20, radius=2.0)
		self.points = mesh.get_vertices()
		faces = mesh.get_faces()

		"""
		this is the actual path data (the path the toolhead will follow)
		for now we consider the tool orientation is always "normal" to the zero-plane
		(ie. the build surface) but this is likely to change in the future
		"""
		
		if not LINE_RENDERING_CORRECT:
			# simpler version, but it's the points that get the shade! -> wrong
			print(self.points[1])
			#TODO self.line = scene.visuals.Line(pos=self.points[0], color=self.points[1], parent=self.view.scene)
			self.line = scene.visuals.Line(pos=self.points, parent=self.view.scene)

		else:
			# correct rendering version, but WAAAAY too slow! uses huge amount of CPU
			#connect='segments'
			#This generates an A->B, B->C, C->D series of segments
			segs, cols = self.P.get_segments_by_layer()
			self.lines = []
			for i in range(len(segs)):
				#TODO self.lines.append( scene.visuals.Line(pos=segs[i], color=cols[i], parent=self.view.scene) )
				self.lines.append( scene.visuals.Line(pos=segs[i], parent=self.view.scene) )

		"""
		this shows a solid that approximates the final solid as it would be printed

		TODO TODO get some shading to work with at least one light source ; I
		have _never_ done that kind of work, I barely know what it's for so
		some guidance would be really appreciated : static shading prevents from having a good view!
		"""
		#print(len(faces[0]))
		#print(len(faces[1]))
		#print(faces[1])
		meshdata = MeshData.MeshData(
				vertices=self.points[0],
				faces=faces[0],
				#face_colors = faces[1],
			)
		#self.mesh = scene.visuals.Mesh(
		#		meshdata=meshdata,
		#		parent=self.view.scene)

		# Wireframe for mesh
		#wireframe_filter = WireframeFilter(color='lightblue')
		#self.mesh.attach(wireframe_filter)

		#self.face_normals = MeshNormals(meshdata, primitive='face', color='yellow')
		#self.face_normals.parent = self.mesh
		#self.face_normals.visible = False
		#self.vertex_normals = MeshNormals(meshdata, primitive='vertex', color='orange', width=2)
		#self.vertex_normals.parent = self.mesh
		#self.vertex_normals.visible = False

		self.freeze()

		# Add a 3D axis to keep us oriented
		#scene.visuals.XYZAxis(parent=self.view.scene)


	def set_data(self, clip, cmap, fov, shading, normals):
		""" TODO
		if normals == 'None':
				self.vertex_normals.visible = False
				self.face_normals.visible = False
		elif normals == 'Faces':
				self.vertex_normals.visible = False
				self.face_normals.visible = True
		elif normals == 'Vertices':
				self.vertex_normals.visible = True
				self.face_normals.visible = False
		elif normals == 'Both':
				self.vertex_normals.visible = True
				self.face_normals.visible = True
		"""
		#if not LINE_RENDERING_CORRECT:
		#	# TODO check if a value was changed, only update that!
		#	self.P.layer_start, self.P.layer_stop = clip[0], clip[1]
		#	try:
		#		points = self.P.get_points()
		#		print("points/colors (vispy)", len(points[0]), len(points[1]))
		#		self.line.set_data( pos = points[0], color = points[1] )
		#		self.line.parent = self.view.scene
		#	except superslice.NothingToShow:
		#		self.line.parent = None
		#else:
		#	self.P.layer_start, self.P.layer_stop = clip[0], clip[1]
		#	for l in self.lines:
		#		l.parent = None
		#		del l
		#	try:
		#		segs, cols = self.P.get_segments_by_layer()
		#		for i in range(len(segs)):
		#			self.lines.append( scene.visuals.Line(pos=segs[i], color=cols[i], parent=self.view.scene) )
		#	except superslice.NothingToShow:
		#		pass

		# TODO check if a value was changed, only update that!
		#TODO self.P.layer_start_faces, self.P.layer_stop_faces = clip[2], clip[3]
		try:
			faces, colors = self.P.get_mesh()
			#print("face/colors (vispy)", len(faces), len(colors))
			meshdata = MeshData.MeshData(
					vertices=self.points[0],
					faces=faces,
					edges=None,
					face_colors = colors,
				)
			#self.mesh.set_data( meshdata = meshdata )
			#self.mesh.parent = self.view.scene

			#TODO self.face_normals.set_data(meshdata = meshdata)
			#TODO self.vertex_normals.set_data(meshdata = meshdata)
		except: #TODO superslice.NothingToShow:
			#self.mesh.parent = None
			#TODO self.face_normals.parent = None
			#TODO self.vertex_normals.parent = None
			pass

		self.view.camera.fov = fov
		#self.mesh.shading = shading

		#self.iso.set_color(cmap)
		# maybe it's faster to only hide some trianglesvrather than recompute, ie. with clipping planes? I'm not quite I understood the related example, though.
		#faces, normals, face_colors = self.P.get_faces(self.P.ppl, start_layer, stop_layer)
		# both following lines raise something like
		# AttributeError: 'vertices' is not an attribute of class <Isoline at 0x7f1da00c8ca0>
		# but they were set above?!?
		#self.iso.vertices = self.P.get_vertices(self.P.ppl, start_layer, stop_layer)
		#self.iso.tris = faces
		#self.iso.levels = face_colors
        
def on_timer(event):
	''' checks file for modifications and reload source script '''
	import os.path
	global slice_file, slice_mtime

	try:
		if os.path.getmtime(slice_file) > slice_mtime:
			app.reload_slice()
	except NameError:
		# first run at startup
		pass
	except FileNotFoundError:
		# file is probably being rewritten right now..
		pass
	finally:
		try:
			slice_mtime = os.path.getmtime(slice_file)
		except FileNotFoundError:
			# file is probably still being rewritten
			pass



#timer = app.Timer(1, connect=on_timer, start=True)

if __name__ == '__main__':
	from sys import argv

	if len(argv) == 1:
		print(f"usage: {argv[0]} <superslice_object_generator_script>")
		from sys import exit
		exit()
	else:
		from os import path, getcwd
		if path.isfile(argv[1]):
			exec(f"import {argv[1].rstrip('.py')} as ss")
			slice_file = getcwd()+'/'+argv[1]
		elif path.isfile(argv[1]+'.py'):
			exec(f"import {argv[1]} as ss")
			slice_file = getcwd()+'/'+argv[1]+'.py'
		else:
			print(f"Error: `{argv[1]}.py` is not a file")
			raise SystemExit

	app.create()
	win = MainWindow()

	win.show()
	app.run()

