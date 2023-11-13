import pygame

def cross_product(v, w):
    return ((v.y*w.z - v.z*w.y), (v.z*w.x - v.x*w.z), (v.x*w.y - v.y*w.x))

def dot_product(v, w):
    return v[0]*w[0] + v[1]*w[1] + v[2]*w[2]