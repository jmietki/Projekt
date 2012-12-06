# -*- coding: utf-8 -*-

from pyglet.gl import *
from pyglet.event import *

class Camera(object):
    def project(self):
        '''Set up the GL projection matrix. Leave us in GL_MODELVIEW mode.
        '''
        raise NotImplemented()


class FlatCamera(Camera):
    def __init__(self,width, height):
        self.x = 0
        self.y = 0
        self.viewport_x = 0
        self.viewport_y = int((height-720)/2)
        if self.viewport_y < 0:
            self.viewport_y = 0

        self.width, self.height = width, height

    def project(self):
        offset = self.binded_obj.x - self.x
        if self.binded_obj.x + self.binded_obj.width - self.x >= self.width*2/3:
            self.x = self.binded_obj.x + self.binded_obj.width- self.width*2/3

        if self.binded_obj.x - self.x <= self.width/3:
            self.x = self.binded_obj.x - self.width/3

        if self.x < 0:
            self.x = 0

        glViewport(self.viewport_x, self.viewport_y, self.width, self.height)
        glMatrixMode(GL_MODELVIEW)

    def bind(self, obj):
        self.binded_obj = obj
