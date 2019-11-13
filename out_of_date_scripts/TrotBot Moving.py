"""
Created on Sun Nov 12Aug 14 15:08:10 2017

@author: Sam Korman

Diagrams of TrotBot's linkage are here:
https://www.diywalkers.com/trotbot-linkage-plans.html

NOTE: to animate the plot in Anaconda I needed to 
run "%matplotlib qt" in the console before running this code 
"""
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation


#NOTE: to animate the plot in Anaconda I needed to run "%matplotlib qt" in the console before running this code 
 
#rotationIncrements is the amount of increments that the simulation creates, the greater the number,
#the smoother the animation will be.  The lesser the number, the faster the animation will be.
rotationIncrements = 200

#footSweepIncrements is the fraction of rotationIncrements that the simulation will use in the foot-sweep
#animation.  rotationIncrements must be divisible by footSweepIncrements. The greater the number, the fewer
#the foot sweep points will be created, and the lesser the number, more points will be created.
footSweepIncrements =int( rotationIncrements/100)

#moving controlls whether trotBot is moving or if it is static.  Notice that you will want to change the position of axleCenter[0]
#if you are switching between true or false.  The sim will be created a lot faster if moving == False, but making it true will
#not change the speed and smoothness of the sim itself.
moving = True

#trotBotSpeed is the speed at which trot bot moves across the screen when moving == True.
#Notice that you can change the direction of trotbot by making this number positive or negative, 
#and this will work even if moving == False.
scale_trotbot=2
trotBotSpeed = -0.075
trotBotSpeed=trotBotSpeed*400/rotationIncrements
trotBotSpeed=trotBotSpeed*scale_trotbot
#totalRotations is the amount of rotations that the sim will run before it repeats itself.  This number, combined with trotBotSpeed
#will determine how far across the screen trot bot moves when moving == True.  This number does not matter when moving == False. 
totalRotations = 4

crank = 4*scale_trotbot
bar1 = 6*scale_trotbot
bar2 = 8*scale_trotbot
bar3 = 2*scale_trotbot
bar4 = 6*scale_trotbot
bar5 = 2*scale_trotbot
bar6 = 11*scale_trotbot
bar7 = 3*scale_trotbot
bar8 = 9*scale_trotbot
bar9 = 8*scale_trotbot
bar10 = 1*scale_trotbot
oldP = 1*scale_trotbot
bar11 = -2.64*scale_trotbot #this bar is negative because we use the line extension to extend back into the bar.
bar12 = 2.55*scale_trotbot
bar13 =7.2*scale_trotbot
bar14 = 1*scale_trotbot
bar15 = 7.55*scale_trotbot
barW = 2*scale_trotbot
axleCenter = [100.0, 20.0]
joint_3 = [axleCenter[0] - 7.0*scale_trotbot, axleCenter[1]+ 6.0*scale_trotbot]
j_0 = {}
j_1 = {}
j_2 = {}
j_3 = {}
j_4 = {}
j_5 = {}
j_6 = {}
j_7 = {}
j_8 = {}
j_9 = {}
j_10 = {}
j_11 = {}
j_12 = {}
j_13 = {}
j_14 = {}   
xVals = {}
yVals = {}
xRightLegVals = {}
yRightLegVals = {}
    
#this is the function that determines where most of the joints are.
#It finds the two intersection points of two bars, A and B, with joints
#jointA and jointB respectively. It returns one of two solutions.
#The solutions are determined by whether the intersectionNum parameter
#is 0, 1, 2, or 3.  Each number corresponds to high, low, left, or right solution,
#as shown by the variables below.
high = 0
low = 1
left = 2
right = 3

def circIntersection(jointA, jointB, lengthA, lengthB, intersectionNum):
    xPos_a = jointA[0]
    yPos_a = jointA[1]
    xPos_b = jointB[0]
    yPos_b = jointB[1]
    Lc = math.sqrt(((xPos_a - xPos_b) ** 2) + ((yPos_a - yPos_b) ** 2))
    bb = ((lengthB ** 2) - (lengthA ** 2) + (Lc ** 2)) / (Lc * 2)
    h = math.sqrt((((lengthB) ** 2) - (bb ** 2)))
    Xp = xPos_b + ((bb * (xPos_a - xPos_b)) / Lc)
    Yp = yPos_b + ((bb * (yPos_a - yPos_b)) / Lc)
    Xsolution1 = Xp + ((h * (yPos_b - yPos_a)) / Lc)
    Ysolution1 = Yp - ((h * (xPos_b - xPos_a)) / Lc)
    Xsolution2 = Xp - ((h * (yPos_b - yPos_a)) / Lc)
    Ysolution2 = Yp + ((h * (xPos_b - xPos_a)) / Lc)
    solution1 = [Xsolution1, Ysolution1]
    solution2 = [Xsolution2, Ysolution2]
    if intersectionNum == 0 :
        if (Ysolution1 > Ysolution2):
            return solution1
        else:
            return solution2
    elif intersectionNum == 1:
        if (Ysolution1 < Ysolution2):
            return solution1
        else:
            return solution2
    elif intersectionNum == 2:
        if (Xsolution1 < Xsolution2):
            return solution1
        else:
            return solution2
    else:
        if (Xsolution1 > Xsolution2):
            return solution1
        else:
            return solution2

#This function finds the joint that is in a straight line from jointA to jointB,
#with the length of the bar Lb.
def lineExtension(jointA, jointB, Lb):
    xPos_a = jointA[0]
    yPos_a = jointA[1]
    xPos_b = jointB[0]
    yPos_b = jointB[1]
    theta = math.atan2((yPos_b - yPos_a) , (xPos_b - xPos_a))
    X3 = (xPos_b + (Lb * math.cos(theta)))
    Y3 = (yPos_b + (Lb * math.sin(theta)))
    solution = [X3, Y3]
    return solution
    
#This function is used in special cases to find the joint at a
#certain angle away from the line jointA to jointB, with bar
#length Lb
def lineExtensionAngle(jointA, jointB, Lb, angle):
    xPos_a = jointA[0]
    yPos_a = jointA[1]
    xPos_b = jointB[0]
    yPos_b = jointB[1]
    theta = math.atan2((yPos_b - yPos_a) , (xPos_b - xPos_a)) + angle
    X3 = (xPos_b + (Lb * math.cos(theta)))
    Y3 = (yPos_b + (Lb * math.sin(theta)))
    solution = [X3, Y3]
    return solution
    
#Order of joints to be created:
#1-2-3-4-5-1-9-8-2-9-11-12-13-10-7-14-7-6-5
#This order was created by looking at the mechanism specs and 
#determining an efficient way to draw the linkage

#NOTE: this does not have to be the only order, it can change as long as all
#of the bars are created from the connections between the joints
drawOrder = [j_0, j_1, j_2, j_3, j_4, j_5, j_6, j_7, j_8, j_1, j_5, j_1, j_8, j_2, j_1, j_9, j_11, j_12, j_10]

#This function is for splitting the calculated drawOrder array of joints
#into x values and y values, in order to plot them.
def splitXY(i):
    xValues = []
    yValues = []
    for j in range(len(drawOrder)):
        xValues.append(drawOrder[j][str(i)][0])
        yValues.append(drawOrder[j][str(i)][1])
    vals = [xValues, yValues]
    return vals
    
endIncrement = trotBotSpeed * rotationIncrements + axleCenter[0]
    
def createRightLegXY(i, vals):
    xRightLegValues =[]
    yRightLegValues = []
    for j in range(len(vals[0])):
        xRightLegValues.append((axleCenter[0] - vals[0][j]) + axleCenter[0])
        yRightLegValues.append(vals[1][j])
    xRightLegVals[str(rotationIncrements - i - 1)] = xRightLegValues
    yRightLegVals[str(rotationIncrements - i - 1)] = yRightLegValues

               
#This for loop calculates every joint at every increment. It then stores these
#joints in a dictionary to be used later during animation.
for i in range(rotationIncrements):
    if trotBotSpeed < 0 :
        theta = (i / (rotationIncrements - 0.0)) * 2 * math.pi #creates rotationIncrements angles from 0 - 2pi
    else :
        theta = (-i / (rotationIncrements - 0.0)) * 2 * math.pi #creates rotationIncrements angles from 0 - 2pi
    crankX = math.cos(theta) * crank + axleCenter[0]
    crankY = math.sin(theta) * crank + axleCenter[1]
    joint_1_at_theta = [crankX, crankY]
    counter = str(i)
    j_0[counter] = [axleCenter[0], axleCenter[1]]
    j_3[counter] = [joint_3[0], joint_3[1]]
    j_1[counter] = joint_1_at_theta
    j_2[counter] = circIntersection(j_1[counter], j_3[counter], bar1, bar2, high)
    j_4[counter] = lineExtension(j_2[counter], j_3[counter], bar3)
    j_5[counter] = circIntersection(j_1[counter], j_4[counter], bar6, bar4, low)
    j_6[counter] = lineExtension(j_4[counter], j_5[counter], bar5)
    j_9[counter] = lineExtension(j_2[counter], j_1[counter], bar10)
    j_8[counter] = circIntersection(j_1[counter], j_2[counter], bar7, bar15, left)
    j_7[counter] = circIntersection(j_6[counter], j_8[counter], bar9, bar8, low)
    j_10[counter] = lineExtension(j_8[counter], j_7[counter], bar11)
    j_11[counter] = circIntersection(j_10[counter], j_9[counter], bar12, bar13, low)
    j_12[counter] = lineExtension(j_10[counter], j_11[counter], bar14)
    vals = splitXY(i)
    xVals[counter] = vals[0]
    yVals[counter] = vals[1]
    #createRightLegXY creates TrotBot's right leg
    createRightLegXY(int(math.fmod(i+rotationIncrements/2,rotationIncrements)), vals)

    

xMovingVals = {}
xMovingRightLeg = {}
yMovingVals = {}
yMovingRightLeg = {}
if moving == True :
    for i in range(rotationIncrements * totalRotations):
        for j in range(len(xVals)):
            increment = j + i * len(xVals)
            xMovingValueArray = []
            xMovingValueRightLegArray = []
            yMovingValueArray = []
            yMovingValueRightLegArray = []   
            for k in range(len(xVals[str(j)])):
                xMovingValueArray.append(xVals[str(j)][k] + trotBotSpeed * increment)
                xMovingValueRightLegArray.append(xRightLegVals[str(j)][k] + trotBotSpeed * increment)
                yMovingValueArray.append(yVals[str(j)][k])
                yMovingValueRightLegArray.append(yRightLegVals[str(j)][k])
            xMovingVals[str(increment)] = xMovingValueArray
            xMovingRightLeg[str(increment)] = xMovingValueRightLegArray
            yMovingVals[str(increment)] = yMovingValueArray
            yMovingRightLeg[str(increment)] = yMovingValueRightLegArray
else :
    xMovingVals = xVals
    xMovingRightLeg = xRightLegVals
    yMovingVals = yVals
    yMovingRightLeg = yRightLegVals
xlow=-60
xhigh=100
ylow=0
yhigh=40
fig = plt.figure(figsize = (24, 6))
fig.set_facecolor('white')
ax = fig.add_subplot(121)
ax = plt.axes(xlim=(xlow, xhigh), ylim=(ylow, yhigh))

ax.set_title("TrotBot", fontsize=18)

line, = ax.plot([], [], '-o', ms=7, lw=3, mfc='blue', color='black') #linkage line
lineRightLeg, = ax.plot([], [], '-o', ms=7, lw=3, mfc='blue', color='black') #RightLeg 2 linkage line
lineJoint7, = ax.plot([], [], '-o', lw=0, ms=3, alpha=1, mfc='red',mec='red') #foot-path line
lineJoint12, = ax.plot([], [], '-o', lw=0, ms=3, alpha=1, mfc='green',mec='green') #foot-path line


xValsLeg7 = {}
yValsLeg7 = {}
xValsLeg12 = {}
yValsLeg12 = {}

#This function is called before the animation runs, and its purpose is to create
#a dictionary of arrays for the foot-path. These arrays are later used to create
#the animation of the foot-path.
 
if moving == False :
    totalRotations = 1
def init():
    for i in range (len(j_7) * totalRotations/footSweepIncrements):
        xLeg7 = []
        yLeg7 = []
        xLeg12 = []
        yLeg12 = []
        for j in range(i + 1):
            xLeg7.append(xMovingVals[str(j * footSweepIncrements)][7])
            yLeg7.append(yMovingVals[str(j * footSweepIncrements)][7])
            xLeg12.append(xMovingVals[str(j * footSweepIncrements)][17])
            yLeg12.append(yMovingVals[str(j * footSweepIncrements)][17])
        xValsLeg7[str(i)] = xLeg7
        yValsLeg7[str(i)] = yLeg7
        xValsLeg12[str(i)] = xLeg12
        yValsLeg12[str(i)] = yLeg12
    
    line.set_data([], [])
    lineRightLeg.set_data([], [])
    return line, lineRightLeg,
    
#This is the animation function, which updates the drawing based off of where it is in the rotation.
def animate(i):
    line.set_data(xMovingVals[str(i)], yMovingVals[str(i)])
    lineRightLeg.set_data(xMovingRightLeg[str(i)], yMovingRightLeg[str(i)])
    lineJoint7.set_data(xValsLeg7[str(i / footSweepIncrements)], yValsLeg7[str(i / footSweepIncrements)])
    lineJoint12.set_data(xValsLeg12[str(i / footSweepIncrements)], yValsLeg12[str(i / footSweepIncrements)])

    return line, lineRightLeg, lineJoint7, lineJoint12,
    #return line,  lineJoint7, lineJoint12,

#This animation variable stores the animation, and notice that having blit=True makes it run a lot faster, and you can control the speed
#by changing the interval, although I reccommend changing the rotationIncrements instead. Right now it is running as fast as possible,
#with an interval of 0.    
ani = animation.FuncAnimation(fig, animate, frames=rotationIncrements * totalRotations, interval=0, blit=True, init_func=init)

plt.show()