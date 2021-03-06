#!/usr/bin/python2

from environment import *
from driver import *
from robot import *
from mcl import *
#Plotting requires matplotlib.
import matplotlib
from matplotlib.backends.backend_pdf import PdfPages
import sys
import os

matplotlib.use('GTKAgg') #Feel free to change the backend
#['ps', 'Qt4Agg', 'GTK', 'GTKAgg', 'svg', 'agg', 'cairo', 'MacOSX', 'GTKCairo', 'WXAgg', 'TkAgg', 'QtAgg', 'FltkAgg', 'pdf', 'CocoaAgg', 'emf', 'gdk', 'template', 'WX']
import matplotlib.pyplot as plt
from math import pi
def makeEnviron():
  e = Environment([])
  for x in range(5):
    for y in range(5):
      e.obstacles.append(Rect(2*x,2*y,1,1))
  return e
def makeEnviron2():
  O = []
  O.append(Rect(1,0,1,1))
  O.append(Rect(0,2,1,1))
  O.append(Rect(2,2,1,1))
  O.append(Rect(4,0,1,3))
  O.append(Rect(0,4,1,1))
  O.append(Rect(2,4,3,1))

  B = Boundary(-1,-1,7,7)
  O.append(B)
  e = Environment(B,O)
  return e
def makeEnviron3():
  O = []
  O.append(Rect(1,1,4,2))
  O.append(Rect(1,4,4,2))
  O.append(Rect(6,1,1,5))
  O.append(Rect(8,3,1,1))
  
  B = Boundary(0,0,10,7)
  O.append(B)
  e = Environment(B,O)
  return e

def makePath3():
  P = [(0.5,0.5),(0.5,3.5),(5.5,3.5),(5.5,0.5),(7.5,0.5),(7.5,5),(9,5),(9,6.5),(0.5,6.5),(0.5,0.5),(5.5,0.5),(5.5,6.5)]
  return P
def makeMotion1(v_max=5,w_max=6):
  a1=0.05 #v->vr
  a2=0.05 #w->vr
  a3=0.008#v->wr
  a4=0.01 #w->wr
  a5=0.002#v->gr
  a6=0.005#w->gr
  mot = Robot_Motion_Model(a1,a2,a3,a4,a5,a6, v_max=v_max, w_max=w_max)
  return mot
def makeMotion2(v_max=5,w_max=6):
  a1=0.20 #v->vr
  a2=0.20 #w->vr
  a3=0.01 #v->wr
  a4=0.02 #w->wr
  a5=0.004#v->gr
  a6=0.010#w->gr
  mot = Robot_Motion_Model(a1,a2,a3,a4,a5,a6, v_max=v_max, w_max=w_max)
  return mot

def testdriver1():
  env = makeEnviron2()
  env.plot(plt)
  P = [(0.5,1.5),(2.5,1.5),(2.5,0.5),(3.5,0.5),(3.5,1),(3,1),(3,0.5),(3.25,0),(3.5,0.5),(3.5,3.5),(1.5,3.5),(1.5,1.5),(0.5,1.5)]
  plt.ion()
  plt.show()

  mot = Robot_Motion_Model()
  odom = Robot_Odometry_Model()
  meas = Robot_Measurement_Model(measure_count=0,fov=pi/8)
  start_pose = Pose(0.5,1.5,2.8)

  r = Robot_Sim(env,mot,odom,meas,start_pose)
  #print(r)
  driver = Robot_Driver(r,P,v_max = 20, w_max = 3)
  while (not driver.finished):
    u = driver.next_control()
    #print(u)
    r.tick(u,driver.dt)
    #print(driver.count)
    r.plot(plt)

  plt.ioff()
  plt.show()
def testdriver2():
  env = makeEnviron2()

  P = [(0.5,1.5),(2.5,1.5),(2.5,0.5),(3.5,0.5),(3.5,3.5),(1.5,3.5),(1.5,1.5),(0.5,1.5)]
  plt.ion()
  env.plot(plt)
  plt.draw()
  mot = makeMotion1()
  odom = Robot_Odometry_Model()
  meas = Robot_Measurement_Model(measure_count=4,fov=pi/8)
  start_pose = Pose(0.5,1.5,0)

  r = Robot_Sim(env,mot,odom,meas,start_pose)
  #print(r)
  driver = Robot_Driver(r,P,v_max = 5, w_max = 6)
  while (not driver.finished):
    u = driver.next_control()
    #print(u)
    r.tick(u,driver.dt)
    r.plot(plt)    
    plt.draw()
    #print(driver.count)
  


  plt.ioff()
  plt.show()
def testlaser1():
  #env = Environment(Boundary(-1,-1,10,10),[Rect(1,0,1,1),Boundary(-1,-1,10,10)])
  env = makeEnviron2()
  env.plot(plt)
  plt.ion()
  plt.show()
  #plt.ioff()
  mot = makeMotion1()
  odom = Robot_Odometry_Model()
  meas = Robot_Measurement_Model(measure_count=48,fov=2*pi,sd_hit=0)
  start_pose = Pose(3,0.5,-0.83*pi)

  r = Robot_Sim(env,mot,odom,meas,start_pose)
  r.tick((0,0),0.1)
  #print(r)
  #plt.show()
  r.plot(plt)
  plt.draw()
  
  plt.ioff()
  #plt.draw()
  plt.show()
def testmotion1():
  env = makeEnviron2()
  env.plot(plt)
  plt.ion()
  plt.show()

  mot = makeMotion()
  odom = Robot_Odometry_Model()
  meas = Robot_Measurement_Model(measure_count=0,fov=pi/8)
  start_pose = Pose(0.5,1.5,0)

  r = Robot_Sim(env,mot,odom,meas,start_pose)
  r.tick((0,0),0.1)
  r.plot(plt)
  path = [(0.5,1.5),(2.5,1.5),(2.5,0.5),(3.5,0.5),(3.5,3.5),(1.5,3.5),(1.5,1.5),(0.5,1.5)]

  P0 = []
  for i in range(100):
    p_temp = Particle(env,mot,meas,start_pose)
    #p_temp.plot(plt)
    P0.append(p_temp)

  P = [P0]
  i = 0

  driver = Robot_Driver(r,path,v_max = 5, w_max = 6)
  while (not driver.finished):
    u_command = driver.next_control()
    P_temp = []
    for p in P[i]:
      p_temp = p.sample_mov(u_command,0.1)
      p_temp.plot(plt)
      P_temp.append(p_temp)
    P.append(P_temp)
    i = i + 1
      
    #u = r.mot.sample_motion(u_command,r.x,0.1)
    #plt.plot(u.x,u.y,'b.')
    r.tick(u_command,driver.dt)
    r.plot(plt)


  plt.ioff()
  plt.show()

def testmotion2(u = (5,3)):
  env = Environment([Rect(-10,-10,20,20)])#for reference
  env.plot(plt)
  mot = makeMotion1()
  odom = Robot_Odometry_Model()
  meas = Robot_Measurement_Model(measure_count=0,fov=pi/8)
  start_pose = Pose(0.5,1.5,0.5)

  p1 = Particle(env,mot,meas,start_pose)
  p1.plot(plt)
  P0 = []
  for i in range(10):
    p_temp = p1.sample_mov(u,0.2)
    p_temp.plot(plt)
    P0.append(p_temp)
  P = [P0]
  for i in range(10):
    P_temp = []
    for p in P[i]:
      p_temp = p.sample_mov(u,0.1)
      p_temp.plot(plt)
      P_temp.append(p_temp)
    P.append(P_temp)
  plt.ioff()
  plt.show()

def test_random_particle():
  env = makeEnviron2()
  env.plot(plt)
  plt.ion()
  plt.show()
  for i in range(1000):
    x = env.B.x + uniform(-1,env.B.width+2)
    y = env.B.y + uniform(-1,env.B.height+2)
    if (not env.inside(x,y)):
      plt.plot(x,y,"g.")
    else:
      plt.plot(x,y,"r.")
    plt.draw()
  plt.ioff()
def p_rgb(p):
  p_inv = 1.0-p
  g = max([1 - p/0.1,0.0]) * 255
  if (p < 0.1):
    b = (1-(0.1-p)/0.1) * 255
  else:
    b = max([0,1 - (p-0.1)/0.7]) * 255
  r = p * 255 
  #print("r",r,"g",g,"b",b)
  return "#%.2X%.2X%.2X" % (r,g,b)

def test_measurement_prob():
  env = makeEnviron2()
  env.plot(plt)

  meas = Robot_Measurement_Model(measure_count=2,fov=pi/8, sd_hit = 0.2)
  pos = Pose(0.5,1.5,0)
  pos.plot(plt)
  plt.ion()
  plt.show()
  Z = meas.sample_measurement(env,pos)
  x_count = 100
  y_count = 100
  for i in range(x_count):
    for j in range(y_count):
      x = env.B.x + env.B.width * i * 1.0/x_count
      y = env.B.y + env.B.height * j* 1.0/y_count
      X = Pose(x,y,pos.th)
      p = meas.measure_prob(env,X,Z)
      #print(x,y,p,p_rgb(p))
      plt.plot(x,y,'.',color=p_rgb(p))
      plt.draw()
  plt.ioff()
  plt.show()

def test_measurement_prob_2():
  env = makeEnviron2()
  env.plot(plt)

  meas = Robot_Measurement_Model(measure_count=1,fov=pi/8, sd_hit = 0.2)
  pos = Pose(0.5,1.5,0)
  pos.plot(plt)
  plt.ion()
  plt.show()
  Z = meas.sample_measurement(env,pos)
  P = Particle_Collection([],env,None,meas)
  for i in range(2000):
    p = P.draw_random()
    z = p.measure_prob(Z)
    p.plot(plt,p_rgb)
    plt.draw()
  plt.ioff()
  plt.show()

def test_measurement_prob_3():
  env=makeEnviron3()
  path=makePath3()
  mot=makeMotion1(5,6)
  meas=Robot_Measurement_Model(measure_count=6,fov=pi/3,sd_hit=0.02)
  start_pose = Pose(path[0][0],path[0][1],atan2(path[1][1]-path[0][1],path[1][0]-path[0][0]))

  r = Robot_Sim(env,mot,Robot_Odometry_Model(),meas,start_pose)
  r.tick((0,0),0.1)
  plt.figure(0)
  plt.clf()
  env.plot(plt)
  r.plot(plt,True)
  plt.draw()
  pp = PdfPages("measurement.pdf")
  pp.savefig()
  pp.close()

def test_p_rgb():
  P = [x/1000.0 for x in list(range(0,1000))]
  pp = PdfPages("prgb.pdf")
  plt.ion()
  plt.show()
  plt.figure(0)
  for p in P:
    col = p_rgb(p)
    plt.plot([p,p],[0,0.2],"-",color=col)
    plt.draw()
  pp.savefig()
  pp.close()
  plt.ioff()
  plt.show()
  
def test_KLD(epsilon,z_delta):
  k = list(range(2,10000))
  M = map(lambda k: ((k-1)/(2*epsilon)) * (1 - 2/(9*(k-1)) + sqrt(2/(9*(k-1)))*z_delta)**3, k)
  plt.ion()
  plt.plot(k,M,'-k')
  plt.plot(k,k,'-b')
  plt.ioff()
  plt.show()


def MCL(env=makeEnviron3(),path=makePath3(),mot=makeMotion1(5,6),meas=Robot_Measurement_Model(measure_count=6,fov=pi/3,sd_hit=0.02),part_meas=Robot_Measurement_Model(measure_count=6,fov= pi/3,sd_hit=0.2),KLD=True,n=200,kidnapped=False,filename="out",epsilon=0.1,quant=1.65):
  if not os.path.exists(filename):
    os.makedirs(filename)
  f = open(filename + "/data.dat",'w')
  start_pose = Pose(path[0][0],path[0][1],atan2(path[1][1]-path[0][1],path[1][0]-path[0][0]))

  r = Robot_Sim(env,mot,Robot_Odometry_Model(),meas,start_pose)
  r.tick((0,0),0.1)
  P0 = Particle_Collection([],env,mot,part_meas)
  if kidnapped:
    P0.draw_n_random(10000)
    P0.w_fast = 0.001
    P0.w_slow = 0.001
  else:
    for i in range(n):
      P0.P.append(Particle(env,mot,part_meas,start_pose))

      
  #P = [P0]
  P_prev = P0
  Out = []
  plt.ion()
  i = 0
  driver = Robot_Driver(r,path,v_max = mot.v_max, w_max = mot.w_max)
  while (not driver.finished):
    u_command = driver.next_control()
    r.tick(u_command,driver.dt)
    Z = r.Z
    P_new = P_prev.sample_mov(u_command,driver.dt)
    #P_new.P.append(Particle(env,mot,meas,r.x)) #(Cheat mode)
    if KLD:
      P_resampled = P_new.KLD_resample(Z,epsilon,quant)
    else:
      P_resampled = P_new.resample(Z)
    #P.append(P_resampled)
    P_prev = P_resampled
    err = P_new.rmse(r.x)
    i = i+1
    
    plt.figure(0)
    plt.clf()
    env.plot(plt)
    r.plot(plt)

    (count,out) = P_new.plot2(plt,p_rgb)
    datstr = "\t".join(map(str,[r.t,count,err])) + "\n"
    print datstr
    f.write(datstr)

    plt.draw()

    pp = PdfPages(filename + "/" + str(r.t) + ".pdf")
    pp.savefig()
    pp.close()

    plt.figure(0).savefig("%s/%03d.png"%(filename,i))

    plt.figure(1)
    plt.clf()
    plt.hist(P_new.W,bins=20)
    plt.draw()
    
    print "rmse:", err
  f.close()
  plt.ioff()
  plt.show()
  os.system("mencoder 'mf://%s/*.png' -mf type=png:fps=1 -ovc lavc -lavcopts vcodec=wmv2 -oac copy -o animation.mpg"%filename)

def save(f,x,Z,P):
  s = ";".join([str(x),str(Z)]+[str(x) + ":" + str(w) for (x,w) in P]) + "\n"
  #print(s)
  f.write(s)

def open_data(env=makeEnviron3(),filename="out.dat"):
  r = Robot_Sim(None,None,None,None,None)
  f = open(filename,'r')
  plt.ion()
  plt.show()
  for line in f:
    if len(line) < 2:
      break
    try:
      parse = line.split(';')
      r.x = pose_from_str(parse[0])
      r.Z = measurement_from_str(parse[1])
    #print(r.x)
    #print(r.Z)
      P = [part_from_str(p) for p in parse[2:]]
    except:
      break
#print([str(p) for p in P])
    plt.clf()
    env.plot(plt)
    r.plot(plt)
    for p in P:
      p.plot(plt,p_rgb)
    plt.draw()

  f.close()
  plt.ioff()
  plt.show()
    
def usage():
  s =     "Usage:\n"
  s = s + "  mcl [filename]\n"
  s = s + "  kidnapped [filename]\n"
  s = s + "  open [filename]\n"
  print s
                
if __name__ == "__main__":
  if (len(sys.argv) == 1):
    usage()
    exit()
  if (sys.argv[1] == "mcl"):
    if (len(sys.argv) >= 3):
      MCL(filename=sys.argv[2])
    else:
      usage()
  elif (sys.argv[1] == "kidnapped"):
    if (len(sys.argv) >= 3):
      MCL(filename=sys.argv[2],kidnapped=True)
    else:
      usage()   
  elif (sys.argv[1] == "open"):
    if (len(sys.argv) >= 3):
      open_data(filename=sys.argv[2])
    else:
      usage()   
  

  #test_gaussian(plt)
  #test_random_particle()
  #test_measurement_prob_2()
  #mcl1()
  #mcl1()
  #testlaser1()
  #testdriver2()
  #MCL(kidnapped=True,filename="kidnapped7.dat")
  #open_data(filename="kidnapped6.dat")
  #test_KLD(0.15,1.3)
  #test_p_rgb()

