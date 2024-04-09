import pygame
from array import *
import math
import numpy as np
pygame.init()
sc = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
cube = array('d', [-1,-1,-1,  -1,-1,1,   1,-1,1,   1,-1,-1,   1,1,-1,   1,1,1,   -1,1,1,   -1,1,-1])
lindex = array('d',[0,1, 0,3, 0,7, 1,2, 1,6, 2,3, 2,5, 3,4, 4,5, 4,7, 5,6, 6,7])
camera_position = [0,0,0]

#0,0,0,2,0,0,0,2,0,2,2,0,0,0,2,0,2,2,2,2,2,2,0,2
distantion = 10
WHITE = (255,255,255)
numpoints = len(cube) // 3
zmassiv = [1]*numpoints
xmassiv = [1]*numpoints
ymassiv = [1]*numpoints

angle_x = 0.005
angle_y = 0.005
angle_z = 0.005

angle = 0.001
rotation_matrix_x = [
	[1, 0, 0],
	[0, math.cos(angle_x), -math.sin(angle_x)],
	[0, math.sin(angle_x), math.cos(angle_x)]
]
rotation_matrix_y = [
	[math.cos(angle_y), 0, math.sin(angle_y)],
	[0, 1, 0],
	[-math.sin(angle_y), 0, math.cos(angle_y)]
]
rotation_matrix_z = [
	[math.cos(angle_z), -math.sin(angle_z), 0],
	[math.sin(angle_z), math.cos(angle_z), 0],
	[0, 0, 1]
]

for i in range(numpoints):
	zmassiv[i] = cube[i*3+2]
	xmassiv[i] = cube[i*3]
	ymassiv[i] = cube[i*3+1]

tempz = [1] * len(zmassiv)
xmass = [1] * len(xmassiv)
ymass = [1] * len(ymassiv)
cameramassx = [0] * len(xmassiv)
cameramassy = [0] * len(ymassiv)
cameramassz = [0] * len(zmassiv)
def cuberender():
	for i in range(numpoints):
		cameramassx[i] = xmassiv[i] - camera_position[0]
		cameramassy[i] = ymassiv[i] - camera_position[1]
		cameramassz[i] = zmassiv[i] - camera_position[2]
		tempz[i] = (480) / (distantion+cameramassz[i])
		xmass[i] = cameramassx[i] * tempz[i] + 320
		ymass[i] = cameramassy[i] * tempz[i] + 240
	for i in range(0, len(lindex), 2):
		pygame.draw.line(sc,(255,255,255), (xmass[int(lindex[i])],ymass[int(lindex[i])]),(xmass[int(lindex[i+1])],int(ymass[int(lindex[i+1])])))
def zmovement():
	for i in range(numpoints):
		camera_position[2] += 0.001

def minzmovement():
	for i in range(numpoints):
		camera_position[2] -= 0.001

def xmovement():
	for i in range(numpoints):
		camera_position[0] += 0.001

def minxmovement():
	for i in range(numpoints):
		camera_position[0] -= 0.00005

def ymovement():
	for i in range(numpoints):
		camera_position[1] -= 0.00005

def minymovement():
	for i in range(numpoints):
		camera_position[1] += 0.00005

while True:
	for i in range(numpoints):
		xmassiv[i], ymassiv[i], zmassiv[i] = (
			xmassiv[i] * rotation_matrix_x[0][0] + ymassiv[i] * rotation_matrix_x[0][1] + zmassiv[i] *
			rotation_matrix_x[0][2],
			xmassiv[i] * rotation_matrix_x[1][0] + ymassiv[i] * rotation_matrix_x[1][1] + zmassiv[i] *
			rotation_matrix_x[1][2],
			xmassiv[i] * rotation_matrix_x[2][0] + ymassiv[i] * rotation_matrix_x[2][1] + zmassiv[i] *
			rotation_matrix_x[2][2]
		)
		xmassiv[i], ymassiv[i], zmassiv[i] = (
			xmassiv[i] * rotation_matrix_y[0][0] + ymassiv[i] * rotation_matrix_y[0][1] + zmassiv[i] *
			rotation_matrix_y[0][2],
			xmassiv[i] * rotation_matrix_y[1][0] + ymassiv[i] * rotation_matrix_y[1][1] + zmassiv[i] *
			rotation_matrix_y[1][2],
			xmassiv[i] * rotation_matrix_y[2][0] + ymassiv[i] * rotation_matrix_y[2][1] + zmassiv[i] *
			rotation_matrix_y[2][2]
		)
		xmassiv[i], ymassiv[i], zmassiv[i] = (
			xmassiv[i] * rotation_matrix_z[0][0] + ymassiv[i] * rotation_matrix_z[0][1] + zmassiv[i] *
			rotation_matrix_z[0][2],
			xmassiv[i] * rotation_matrix_z[1][0] + ymassiv[i] * rotation_matrix_z[1][1] + zmassiv[i] *
			rotation_matrix_z[1][2],
			xmassiv[i] * rotation_matrix_z[2][0] + ymassiv[i] * rotation_matrix_z[2][1] + zmassiv[i] *
			rotation_matrix_z[2][2]
		)
		cuberender()
		keys = pygame.key.get_pressed()
		if keys[pygame.K_UP]:
			zmovement()
		if keys[pygame.K_DOWN]:
			minzmovement()
		if keys[pygame.K_RIGHT]:
			xmovement()
		if keys[pygame.K_LEFT]:
			minxmovement()
		if keys[pygame.K_z]:
			ymovement()
		if keys[pygame.K_x]:
			minymovement()
		pygame.display.update()
		sc.fill((0, 0, 0))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()