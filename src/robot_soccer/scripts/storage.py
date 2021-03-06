import numpy as np
import math

class kalStore():
    def __init__(self):

        self.xhat = 0
        self.xhat_delayed = 0
        self.S = 0
        self.S_delayed = 0

class gameInfo():
    def __init__(self):
        self.score = [0, 0]  # home and away score
        self.reset = False   # Flag for making it return to the home positions
        self.pause = False  # Flag for pausing the game
        self.ballPast = [0, 0]
        self.late = .001        # camera latency - consider making dynamic


class kTimer():
    def __init__(self):
        self.count = 0    # delay timer (cycles through code)
        self.bZ = .11     # buffer zone
        self.kR = .09     # kick range
        self.aA = .05     # angular accuracy
        self.fPs = 20     # field x-position to shoot from
        self.cL = 200    # count limit to reset


class lpf():
    def __init__(self):
        self.position
        self.position_delayed
        self.velocity
        self.old_position_measurement
        self.a1
        self.a2


class param():
    def __init__(self):
        # number of robots per team
        self.num_robots = 2

        # field characteristics
        self.field_length  = 3.2 # meters (8 ft)
        self.field_width   = 1.6 # meters (16 ft)
        self.goal_width = self.field_width/3
        self.display_rate = 0.1
        self.startForward = [0.6, 0]
        self.startDefender = [1.5, 0]
        self.goal = [1.6, 0]

        #self.field_color = [16, 92, 1]/256
        #self.home_team_color = 'b'
        #self.away_team_color = 'g'
        #self.ball_color = 'y'
        #self.goal_color = [252, 148, 3]/256


        # constants that govern ball dynamics
        self.ball_radius = 0.03
        self.ball_mu = 0.05  # coefficient of friction for ball
        self.ball_spring = 500  # spring constant that models wall and robot interactions

        # robot parameters and geometry
        self.wheel_radius = 0.03            # m (this is a guess)
        self.robot_radius = 0.1             # 4 inches
        self.robot_max_vx = .8              # (m/s) max speed in x direction
        self.robot_max_vy = .5              # (m/s) max speed in y direction
        self.robot_max_omega = 2*np.pi      # 360 degrees/sec
        # the geometry assumes 60 degree equally distributed wheels at distance 5cm
        # from center

        phi = 60*np.pi/180
        mx = float(self.robot_radius*math.cos(phi))
        my = float(self.robot_radius*math.sin(phi))
        r1 = ([mx,my])
        r2 = ([-mx,my])#r2 = float(self.robot_radius*[[-math.cos(phi)], [math.sin(phi)]])
        r3 = ([self.robot_radius,self.robot_radius])#r3 = float(self.robot_radius*[[0], [1]])
        s1 = [-my, mx]#s1 = np.matrix([[-math.sin(phi)], [math.cos(phi)]])
        s2 = [-my, -mx]#s2 = np.matrix([[-math.sin(phi)], [-math.cos(phi)]])
        s3 = [self.robot_radius, self.robot_radius] #s3 = np.matrix([[1], [0]])
        # kinematic matrix relating wheel velocity to body velocity

        self.M3 = 1/self.wheel_radius*np.matrix([
            [s1[0], s1[1], (s1[1]*r1[0]-s1[0]*r1[1])],
            [s2[0], s2[1], (s2[1]*r2[0]-s2[0]*r2[1])],
            [s3[0], s3[1], (s3[1]*r3[0]-s3[0]*r3[1])]])

        self.M3inv = np.linalg.inv(self.M3)

        # initial states for robots and ball
        self.home_team_initial_configurations = np.matrix([
            [-self.field_length/6], [0],  [0],              # robot 1, position and orientation
            [-self.field_length/3], [0],  [0]])             # robot 2, position and orientation

        self.away_team_initial_configurations = np.matrix([
            [-self.field_length/6], [0], [0],               # robot 1, position and orientation
            [-self.field_length/3], [0], [0]])              # robot 2, position and orientation

        self.ball_initial_position = np.matrix([[0], [0]])     # in frame of home team

        self.ball_initial_velocity = np.matrix([[0], [0]])     # in frame of home team

        # goal positions
        self.goal = np.matrix([[self.field_length/2], [0]])

        # controller gains
        self.control_sample_rate = 0.01
        self.control_k_vx = 5               # gain for proportional control of x-position
        self.control_k_vy = 5               # gain for proportional control of y-position
        self.control_k_phi = 2              # gain for proportional angle control

        # camera parameters
        self.camera_sample_rate = 10*self.control_sample_rate
        # noise levels on the camera
        self.camera_sigma_ball = 0.01                   # units are meters
        self.camera_sigma_robot_position = 0.01         # units are meters
        self.camera_sigma_robot_angle = 2*np.pi/180   # units are radians

        # parameters for state estimator
        self.lpf_alpha = 0.7
        self.dirty_derivative_gain = self.camera_sample_rate/5

        # parameters for the Kalman filter
        self.Q_ownteam = np.matrix([[1**2, 0, 0],
                               [0, 1**2, 0],
                               [0, 0, (2*np.pi/180)**2]])

        self.R_ownteam = np.matrix([[self.camera_sigma_robot_position**2, 0, 0],
                                 [0, self.camera_sigma_robot_position**2, 0],
                                 [0, 0, self.camera_sigma_robot_angle**2]])

        self.Q_opponent = 1*np.matrix([[.001**2, 0, 0, 0, 0, 0, 0, 0, 0],
                                  [0, .001**2, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, .01**2, 0, 0, 0 ,0 ,0, 0],
                                  [0, 0, 0, .01**2, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, .1**2, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, .1**2, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 1**2, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 1**2, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 0, (2*np.pi/180)**2]])

        self.R_opponent = np.matrix([[self.camera_sigma_robot_position**2, 0, 0],
                                  [0, self.camera_sigma_robot_position**2, 0],
                                  [0, 0, self.camera_sigma_robot_angle**2]])

        self.Q_ball = 1*np.matrix([[.001**2, 0, 0, 0, 0, 0, 0, 0],
                                   [0, .001**2, 0, 0, 0, 0, 0, 0],
                                   [0, 0, .01**2, 0, 0, 0, 0, 0],
                                   [0, 0, 0, .01**2, 0, 0, 0, 0],
                                   [0, 0, 0, 0, .1**2, 0, 0, 0],
                                   [0, 0, 0, 0, 0, .1**2, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 10**2, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 10**2]])

        self.R_ball = np.matrix([[self.camera_sigma_ball**2, 0], [0, self.camera_sigma_ball**2]])


        # parameters for opponent Kalman filter
        self.A_opponent = np.matrix([[0, 0, 0, 1, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 1, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 1, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 1, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 1, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 1],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0]])

        self.C_opponent = np.matrix([[1, 0, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 1, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 1, 0, 0, 0, 0, 0, 0]])

        # parameters for ball Kalman filter
        self.A_ball = np.matrix([[0, 0, 1, 0, 0, 0, 0, 0],
                              [0, 0, 0, 1, 0, 0, 0, 0],
                              [0, 0, 0, 0, 1, 0, 0, 0],
                              [0, 0, 0, 0, 0, 1, 0, 0],
                              [0, 0, 0, 0, 0, 0, 1, 0],
                              [0, 0, 0, 0, 0, 0, 0, 1],
                              [0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0]])

        self.C_ball = np.matrix([[1, 0, 0, 0, 0, 0],
                              [0, 1, 0, 0, 0, 0]])


