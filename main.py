#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# orbitals. andershoff.net
# inspired by complexification.net
#

import os, sys,Image
from math import log, sin, cos, pi, atan2, sqrt
from random import random
import cairo
from operator import itemgetter
from time import time
import numpy as np

N      = 1000
N2     = N/2
R      = 0.2
NUM    = 200
GRAINS = 5
PI     = pi
PII    = PI*2.
BACK   = 1.
OUT    = 'img'
MAXFS  = 10
NEARL  = 0.1
FARL   = 0.2
RAD    = 0.2

R      = [0.]*NUM
A      = [0.]*NUM
F      = [[] for i in xrange(0,NUM)]
#X      = [0]*NUM
#Y      = [0]*NUM
#SX     = [0]*NUM
#SY     = [0]*NUM

def ctxInit():
  sur = cairo.ImageSurface(cairo.FORMAT_ARGB32,N,N)
  ctx = cairo.Context(sur)
  ctx.scale(N,N)
  ctx.set_source_rgb(BACK,BACK,BACK)
  ctx.rectangle(0,0,1,1)
  ctx.fill()
  return sur,ctx

def pInit(X,Y):
  for i in xrange(0,NUM):
    the = random()*PII
    x = RAD * sin(the)
    y = RAD * cos(the)
    X[i] = 0.5+x
    Y[i] = 0.5+y
  return

def showP(ctx,X,Y):
  ctx.set_source_rgba(1,0,0,0.01)
  for i in xrange(0,NUM):
    ctx.move_to(X[i],Y[i])
    ctx.arc(X[i],Y[i],2./N,0,PII)
  ctx.close_path()
  ctx.fill()
  return

#def setDistances(X,Y):
  #for i in xrange(0,NUM):
    #for j in xrange(0,NUM):
      #if i == j:
        #continue
      #dx = X[i] - X[j]
      #dy = Y[i] - Y[j]
      #a  = atan2(dy,dx)
      #d  = sqrt(dx*dx+dy*dy)
      #ii,jj = i*NUM+j,j*NUM+i
      #R[jj],R[ii] = d,d
      #A[ii],A[jj] = a,a+PI
  #return

def setDistances(X,Y):
  for i in xrange(0,NUM):
    dx = X[i] - X
    dy = Y[i] - Y
    a  = np.arctan2(dy,dx)
    d  = np.sqrt(dx*dx+dy*dy)
    R[i] = d
    A[i] = a
  return

def makeFriends(i):
  if len(F[i]) > MAXFS:
    return

  r = []
  for j in xrange(0,NUM):
    if i != j:
      r.append((R[i][j],j))
  sorted(r, key=itemgetter(0))

  index = NUM-2
  for k in xrange(0,NUM-1):
    if random() < 0.1:
      index = k
      break
  
  for k in xrange(0,len(F[i])):
    if F[i][k] == index:
      return
  if len(F[r[index][1]]) > MAXFS:
    return 
  F[i].append(r[index][1])
  F[r[index][1]].append(i)
  return

def drawConnections(ctx,X,Y):
  for i in xrange(0,NUM):
    for f in xrange(0,len(F[i])):
      if i == F[i][f] or F[i][f] < i:
        continue
      dist = R[i][F[i][f]] * random()
      a = A[i][F[i][f]]

      sx = cos(a)
      sy = sin(a)
      scale = dist/GRAINS
      
      xp,yp = 0.,0.
      if random() < 0.5:
        xp = X[i]
        yp = Y[i]
      else:
        xp = X[F[i][f]]
        yp = Y[F[i][f]]
        scale = -scale

      for q in xrange(0,GRAINS):
        xp -= sx*scale
        yp -= sy*scale
        ctx.rectangle(xp,yp,1./N,1./N)
        ctx.fill()
  return

def run(ctx,X,Y,SX,SY):
  t = []
  t.append(time())
  setDistances(X,Y)
  t.append(time())
  
  #for i in xrange(0,NUM):
    #SX[i] = 0.
    #SY[i] = 0.
  SX[:] = 0.
  SY[:] = 0.
  
  t.append(time())
  for i in xrange(0,NUM):
    for j in xrange(i+1,NUM):
      if len(F[i]) < 1 or F[j] < 1:
        continue
      dist = R[i][j]
      a = A[j][i]

      f = False
      for q in xrange(0,len(F[i])):
        if j == F[i][q]:
          f = True
          break

      if dist > NEARL and f:
        SX[i] += cos(a)/N 
        SY[i] += sin(a)/N 
        SX[j] -= cos(a)/N 
        SY[j] -= sin(a)/N 
      elif dist < FARL:
        force = FARL - dist
        aPI = a+PI
        SX[i] += force*cos(aPI)/N 
        SY[i] += force*sin(aPI)/N 
        SX[j] -= force*cos(aPI)/N 
        SY[j] -= force*sin(aPI)/N 
  t.append(time())

  #for i in xrange(0,NUM):
    #X[i] += SX[i]
    #Y[i] += SY[i]
  X  += SX 
  Y  += SY 

  t.append(time())
  makeFriends(int(random()*NUM))
  t.append(time())
  drawConnections(ctx,X,Y)
  t.append(time())
  
  for ti in xrange(0,len(t)-1):
    print str(t[ti+1] - t[ti]),
  print 

def main():
  X       = np.zeros((NUM,1))
  Y       = np.zeros((NUM,1))
  SX      = np.zeros((NUM,1))
  SY      = np.zeros((NUM,1))
  sur,ctx = ctxInit()
  pInit(X,Y)

  ctx.set_source_rgba(0,0,0,0.2)

  for i in xrange(0,1000):
    run(ctx,X,Y,SX,SY)

  sur.write_to_png('./'+OUT+'.png')
  return

if __name__ == '__main__' : main()

