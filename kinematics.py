import math
import matplotlib.pyplot as plt
import random

#-----------Functions------------#

def getEndPosition(ang1, ang2, l1, l2):
    x1 = l1 * math.cos(ang1)
    y1 = l1 * math.sin(ang1)

    x2 = l2 * math.cos(ang1 + ang2)
    y2 = l2 * math.sin(ang1 + ang2)

    x = x1+x2
    y = y1+y2

    return x, y

def getAngles(x, y, l1, l2):
    theta2 = math.atan2(-1* math.sqrt(1-((x*x + y*y - l1*l1 - l2*l2)/(2*l1*l2))*((x*x + y*y - l1*l1 - l2*l2)/(2*l1*l2))), (x*x + y*y - l1*l1 - l2*l2)/(2*l1*l2))
    theta1 = math.atan2(y, x) + math.atan2(math.sqrt(y*y + x*x - (math.cos(theta2)*l2+l1)*(math.cos(theta2)*l2+l1)), math.cos(theta2)*l2 + l1)

    return theta1, theta2

#--------------------------------#

l1 = 160
l2 = 180

fig = plt.figure()
ax = plt.subplot(111)
ax.set_ylim([-350, 350])   # set the bounds to be 10, 10
ax.set_xlim([-350, 350])
ax.spines['left'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['bottom'].set_position('zero')
ax.spines['top'].set_color('none')

while True:
    #Making Random Point
    #while True:
    ang1 = random.randint(0,90)
    ang2 = random.randint(-1*(360-(180+ang1)),0)
    radAng1 = math.radians(ang1)
    radAng2 = math.radians(ang2)

    startX, startY = 0, 0

    link1X = startX + l1 * math.cos(radAng1)
    link1Y = startY + l1 * math.sin(radAng1)

    endX = link1X + l2 * math.cos(radAng1 + radAng2)
    endY = link1Y + l2 * math.sin(radAng1 + radAng2)
    
    #if(endY > -80 and endY < -40 and endX > 65): #defining boundary
    #    break
    

    #ax.plot([startX, link1X], [startY, link1Y], 'r') #Plotting First Link
    #ax.plot([link1X, endX], [link1Y, endY], 'b') #Plotting Second Link

    pointAnn = ax.annotate("Desired", (endX, endY))
    ax.plot(endX, endY, 'ro')

    print("x: %.2f, y: %.2f" % (endX, endY))

    plt.show(block=False)
    plt.pause(1)

    #-------Using inverse kinematics obtained angles-------#
    try:
        radAng1, radAng2 = getAngles(endX, endY, l1, l2)

        if (not(radAng1 < 0 or radAng1 > 180 or radAng2 > 0 or radAng2 < -180)):
            startX, startY = 0, 0

            link1X = startX + l1 * math.cos(radAng1)
            link1Y = startY + l1 * math.sin(radAng1)

            endX = link1X + l2 * math.cos(radAng1 + radAng2)
            endY = link1Y + l2 * math.sin(radAng1 + radAng2)

            ax.plot([startX, link1X], [startY, link1Y], 'g--')
            ax.plot([link1X, endX], [link1Y, endY], 'y--')

        else:
            print("Cannot Reach Position")

        print("Angle 1: %.2f, Angle 2: %.2f" % (math.degrees(radAng1), math.degrees(radAng2)))
    except:
        print("Cannot Reach Position")
    #-------------------------------------------#

    plt.show(block=False)
    plt.pause(1)

    pointAnn.remove()
    for artist in plt.gca().lines + plt.gca().collections:
        artist.remove()

###neededRotation = (90-math.degrees(link2Angle+link1Angle))