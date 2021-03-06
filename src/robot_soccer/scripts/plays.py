import velchangers as vel
from strategies import *
from controller import *
import altDrive as ad
import kick


# This is where we store our different plays




def goToBall(r, b):
    g = P.goal
    vx = P.control_k_vx*(r[0]-b[0])
    vy = P.control_k_vy*(r[1]-b[1])
    theta_d = m.atan2(g[1]-r[1], g[0]-r[0])
    omega = P.control_k_phi*(r[2] - theta_d)
    #vel.goXYOmega(vx, vy, omega)
    ad.velDrive(vx, vy, omega, r)


def goToGoal(r):
    g = P.goal
    #vx =
    vx = -P.control_k_vx*(r[0]-g[0])
    vy = -P.control_k_vy*(r[1]-g[1])
    theta_d = m.atan2(g[1]-r[1], g[0]-r[1])
    omega = -P.control_k_phi*(r[2] - theta_d)
    vel.goXYOmega(vx, vy, omega)


def goToStartForward(r):
    pos = P.startForward
    g = P.goal
    vx = -P.control_k_vx*(r[0]-pos[0])
    vy = -P.control_k_vy*(r[1]-pos[1])
    theta_d = m.atan2(g[1]-r[1], g[0]-r[1])
    omega = -P.control_k_phi*(r[2] - theta_d)
    vel.goXYOmega(vx, vy, omega)


def goToStartDefender(r):
    pos = P.startDefender
    g = P.goal
    vx = -P.control_k_vx*(r[0]-pos[0])
    vy = -P.control_k_vy*(r[1]-pos[1])
    theta_d = m.atan2(g[1]-r[1], g[0]-r[1])
    omega = P.control_k_phi*(r[2] - theta_d)
    vel.goXYOmega(vx, vy, omega)

def defendBall(r,b):
    g = P.goal
    vx = -P.control_k_vx*(r[0])
    vy = -P.control_k_vy*(r[1]-b[1])
    theta_d = m.atan2(g[1]-r[1], g[0]-r[1])
    omega = P.control_k_phi*(r[2] - theta_d)
    vel.goXYOmega(vx, vy, omega)

def goToPoint(r, pos):
    g = P.goal
    vx = -P.control_k_vx*(r[0]-pos[0])
    vy = -P.control_k_vy*(r[1]-pos[1])
    theta_d = m.atan2(g[1]-r[1], g[0]-r[0])
    omega = P.control_k_phi*(r[2] - theta_d)
    vel.goXYOmega(vx, vy, omega)

def goStart(bret):
    start = 0.45
    print "info for debugg"
    xposition = float(bret[0]-start)
    #print "ballx,bally,homex,homey, hometheta",-ball[0],ball[1],bret[0],bret[1],bret[2]
    vel.goXYOmega(xposition,bret[1],bret[2])

def goCenter(data):
    xb = data.ball_x
    yb = data.ball_y
    xr = data.home1_x
    yr = data.home1_y
    tr = data.home1_theta
    print "info for debugg"
    print "ballx,bally,homex,homey, hometheta",xb,yb,xr,yr,tr
    vel.goXYOmega(xr,yr,tr)

#here we do homeX - 1.35 we go to home goal
#here we fo homeX + 1.35 we go to away goal
def goToGoal(bret):
    distGoalX = 1.75
    #distGoaly = data.home1_y

    goX = bret[0]+distGoalX#data.home1_x+distGoalX
    goY = bret[1]#data.home1_y
    tg = bret[2]#data.home1_theta
    #goTheta = tg - data.home1_theta
    vel.goXYOmega(goX,goY,tg)


def goHomeGoal(bret):
    distGoalX = 1.56
    #distGoaly = data.home1_y
    goX = bret[0]-distGoalX
    goY = bret[1]
    tg = bret[2]
    #goTheta = tg - data.home1_theta
    vel.goXYOmega(goX,goY,tg)

def goTopoint(x,y,t):
    vel.goXYOmega(x,y,t)



def getBall(bret, ball, field):
    robotX = ball[0]-bret[0]    #has to be balllocation - robotLocation
    robotY = ball[1]-bret[1]
    fieldX = field[0]/2
    fieldY = field[1]/2
    oldPosX = robotX
    oldPosY = robotY

    if robotX == 0:
        robotX = .01

    xgoal = fieldX-bret[0]
    if xgoal == 0:
        xgoal = .01


    toGoal = float(math.acos(float(xgoal)/math.sqrt(float(xgoal)**2+float(fieldY-bret[1])**2))+bret[2])
    #rospy.loginfo("toBall and toGoal : %f, %f" %(toBall,toGoal))
    goalX = fieldX - 0.08
    if ball[0] > goalX or ball[0] < -goalX:
        goStart(bret)
    else:
        vel.goXYOmega(-robotX,-robotY,toGoal)

    kickX = abs(ball[0]-bret[0])
    kickY = abs(ball[1]-bret[1])

    if ((kickX < 0.09 and kickX > 0) and (kickY < 0.045 and kickY > 0)):
        print "Is kicking positive :",kickX,kickY
        kick.kick()
        kickX =0.0
        kickY=0.0

        print "Reseting kicker :",kickX,kickY
    else:
        count =0



def holdPosition():
    ad.stop()


