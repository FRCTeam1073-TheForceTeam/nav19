"""

Particle Filter localization sample

author: Atsushi Sakai (@Atsushi_twi)

"""
# All comments denoted Cam were written by Cam, and represent his observations. They are likely not perfect
LIDAR_DEVICE = '/dev/cu.SLAB_USBtoUART' #Cam - where is LiDAR, change to COM5 on most Windows Machines, "/dev/ttyUSB0" on Raspberry Pi, Mac, and Ubuntu
import sys
from multiprocessing import Process
import numpy as np
import math
import matplotlib.pyplot as plt
from rplidar import RPLidar as Lidar #Cam - import RPLidar
import fieldScanner #Katherine - import the scanner methods
# Estimation parameter of PF
Q = np.diag([0.1])**2  # range error #Cam - how tightly packed the particles are around the "robot"
R = np.diag([1.0, np.deg2rad(40.0)])**2  # input error #Cam - deviation allowed 
lidar = Lidar(LIDAR_DEVICE)
#  Simulation parameter
#np.diag: creates a daigonal array like this
Qsim = np.diag([0.2])**2 #Cam - determines how closely the lines follow each other- Simulation Purposes Only

Rsim = np.diag([1.0, np.deg2rad(30.0)])**2 # Cam - Changes the correlation between dead reckoning and actual posiitoning

DT = 0.1  # time tick [s] #Cam - how many times it updates over the course of the simulation, but also changes the simulation time by a predictable about (multiply DT by 9 = divide sim time by 9)
SIM_TIME = 50.0  # simulation time [s] # Cam - how many "seconds", partially relative to DT (see comment above), in the simulation
MAX_RANGE = 20.0  # maximum observation range # Cam - maximum domain and range of the simulation coordinate plane

# Particle filter parameter
NP = 100  # Number of Particle # Cam - exactly what they said
NTh = NP / 2.0  # Number of particle for re-sampling # Cam - how many points seem reasonable to the program

show_animation = True #Cam - determines if the animation will be shown
lidar.start_motor()
#lidar.connect()

def scan(path):

    '''Main function'''
    for measurment in lidar.iter_measurments():
        print(measurment[2])
            
def calc_input():
    print("running calc")
    #print(lidar.measurment[0])
    v = 1.0  # [m/s] #Cam - velocity of the simulated robot
    yawrate = 0.1  # [rad/s] #Cam- rotational rate of the robot
    u = np.array([[v, yawrate]]).T #Cam - an array storing the velocity and rotational rate
    # Katherine - yawrate > 0.1 makes circle smaller. yawrate < 0.1 makes circle wider.
    return u #Cam - an array
    



def observation(xTrue, xd, u, RFID):
    print("running observation")
    xTrue = motion_model(xTrue, u)

    # add noise to gps x-y
    z = np.zeros((0, 3)) #Cam - creates an empty array 

    for i in range(len(RFID[:, 0])):

        dx = xTrue[0, 0] - RFID[i, 0] #Cam - This outputs three values. All three are the x distance from one of the rockets on the field.
        dy = xTrue[1, 0] - RFID[i, 1] #Cam - This outputs three values. All three are the y distance from one of the rockets on the field.
        d = math.sqrt(dx**2 + dy**2) #Cam - This outputs the total distance from the rockets on the field. Not sure how they are serialized, but they do work.

        if d <= MAX_RANGE:
            dn = d + np.random.randn() * Qsim[0, 0]  # add noise #Cam- Places additonal possible points on the field within a reasonable range as difined earlier
            zi = np.array([[dn, RFID[i, 0], RFID[i, 1]]])
            z = np.vstack((z, zi))

    # add noise to input
    ud1 = u[0, 0] + np.random.randn() * Rsim[0, 0]
    ud2 = u[1, 0] + np.random.randn() * Rsim[1, 1]
    ud = np.array([[ud1, ud2]]).T

    xd = motion_model(xd, ud)

    return xTrue, z, xd, ud


def motion_model(x, u):

    F = np.array([[1.0, 0, 0, 0],
                  [0, 1.0, 0, 0],
                  [0, 0, 1.0, 0],
                  [0, 0, 0, 0]])

    B = np.array([[DT * math.cos(x[2, 0]), 0],
                  [DT * math.sin(x[2, 0]), 0],
                  [0.0, DT],
                  [1.0, 0.0]])

    x = F.dot(x) + B.dot(u)

    return x


def gauss_likelihood(x, sigma):
    p = 1.0 / math.sqrt(2.0 * math.pi * sigma ** 2) * \
        math.exp(-x ** 2 / (2 * sigma ** 2))

    return p


def calc_covariance(xEst, px, pw):
    cov = np.zeros((3, 3))

    for i in range(px.shape[1]):
        dx = (px[:, i] - xEst)[0:3]
        cov += pw[0, i] * dx.dot(dx.T)

    return cov


def pf_localization(px, pw, xEst, PEst, z, u):
    """
    Localization with Particle filter
    """

    for ip in range(NP):
        x = np.array([px[:, ip]]).T
        w = pw[0, ip]
        #  Predict with random input sampling
        ud1 = u[0, 0] + np.random.randn() * Rsim[0, 0]
        ud2 = u[1, 0] + np.random.randn() * Rsim[1, 1]
        ud = np.array([[ud1, ud2]]).T
        x = motion_model(x, ud)

        #  Calc Importance Weight
        for i in range(len(z[:, 0])):
            dx = x[0, 0] - z[i, 1]
            dy = x[1, 0] - z[i, 2]
            prez = math.sqrt(dx**2 + dy**2)
            dz = prez - z[i, 0]
            w = w * gauss_likelihood(dz, math.sqrt(Q[0, 0]))

        px[:, ip] = x[:, 0]
        pw[0, ip] = w

    pw = pw / pw.sum()  # normalize

    xEst = px.dot(pw.T)
    PEst = calc_covariance(xEst, px, pw)

    px, pw = resampling(px, pw)

    return xEst, PEst, px, pw


def resampling(px, pw):
    """
    low variance re-sampling
    """

    Neff = 1.0 / (pw.dot(pw.T))[0, 0]  # Effective particle number
    if Neff < NTh:
        wcum = np.cumsum(pw)
        base = np.cumsum(pw * 0.0 + 1 / NP) - 1 / NP
        resampleid = base + np.random.rand(base.shape[0]) / NP

        inds = []
        ind = 0
        for ip in range(NP):
            while resampleid[ip] > wcum[ind]:
                ind += 1
            inds.append(ind)

        px = px[:, inds]
        pw = np.zeros((1, NP)) + 1.0 / NP  # init weight

    return px, pw


def plot_covariance_ellipse(xEst, PEst):  # pragma: no cover
    Pxy = PEst[0:2, 0:2]
    eigval, eigvec = np.linalg.eig(Pxy)

    if eigval[0] >= eigval[1]:
        bigind = 0
        smallind = 1
    else:
        bigind = 1
        smallind = 0

    t = np.arange(0, 2 * math.pi + 0.1, 0.1)

    # eigval[bigind] or eiqval[smallind] were occassionally negative numbers extremely
    # close to 0 (~10^-20), catch these cases and set the respective variable to 0
    try:
        a = math.sqrt(eigval[bigind])
    except ValueError:
        a = 0

    try:
        b = math.sqrt(eigval[smallind])
    except ValueError:
        b = 0

    x = [a * math.cos(it) for it in t]
    y = [b * math.sin(it) for it in t]
    angle = math.atan2(eigvec[bigind, 1], eigvec[bigind, 0])
    R = np.array([[math.cos(angle), math.sin(angle)],
                  [-math.sin(angle), math.cos(angle)]])
    fx = R.dot(np.array([[x, y]]))
    px = np.array(fx[0, :] + xEst[0, 0]).flatten()
    py = np.array(fx[1, :] + xEst[1, 0]).flatten()
    plt.plot(px, py, "--r")

def main():
    print(__file__ + " start!!")

    time = 0.0

    # RFID positions [x, y]
    RFID = np.array([[0.0, 10.67],
                     [8.23, 10.67],
                     [0.0, 5.79],
                     [8.23, 5.79]])

    # State Vector [x y yaw v]'
    xEst = np.zeros((4, 1))
    xTrue = np.zeros((4, 1))
    PEst = np.eye(4)

    px = np.zeros((4, NP))  # Particle store
    pw = np.zeros((1, NP)) + 1.0 / NP  # Particle weight
    xDR = np.zeros((4, 1))  # Dead reckoning

    # history
    hxEst = xEst
    hxTrue = xTrue
    hxDR = xTrue

    while SIM_TIME >= time:
        time += DT
        u = calc_input()

        xTrue, z, xDR, ud = observation(xTrue, xDR, u, RFID)

        xEst, PEst, px, pw = pf_localization(px, pw, xEst, PEst, z, ud)

        # store data history
        hxEst = np.hstack((hxEst, xEst))
        hxDR = np.hstack((hxDR, xDR))
        hxTrue = np.hstack((hxTrue, xTrue))

        if show_animation:
            plt.cla()

            for i in range(len(z[:, 0])):
                plt.plot([xTrue[0, 0], z[i, 1]], [xTrue[1, 0], z[i, 2]], "-k")
            plt.plot(RFID[:, 0], RFID[:, 1], "*k")
            plt.plot(px[0, :], px[1, :], ".r")
            plt.plot(np.array(hxTrue[0, :]).flatten(),
                     np.array(hxTrue[1, :]).flatten(), "-b")
            plt.plot(np.array(hxDR[0, :]).flatten(),
                     np.array(hxDR[1, :]).flatten(), "-k")
            plt.plot(np.array(hxEst[0, :]).flatten(),
                     np.array(hxEst[1, :]).flatten(), "-r")
            plot_covariance_ellipse(xEst, PEst)
            plt.axis("equal")
            plt.grid(True)
            plt.pause(0.001)


if __name__ == '__main__':
    try:
        p = Process(target=main)
        p.start()
        p2 = Process(target=scan, args=sys.argv[1])
        p2.start()
        p.join()
        p2.join()
    except:
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()
        