#Import Python Imaging Library 
from PIL import Image
#Import numpy math library
import numpy as np


#######################################################################################
# Data stored is type int8 ranging from (0-255) when convert image into matrix
# Process the pixel in integer to avoid overflow/underflow which affect the calculation
# dotP : dot product
# mag : magnitude
#######################################################################################
def cosineSimilarity(vect1, vect2):
    dotP = 0
    mag1 = 0.0
    mag2 = 0.0

    for i in range (len(vect1)) : 
        dotP += int(vect1[i]) * vect2[i]   
        mag1 += vect1[i] ** 2 
        mag2 += vect2[i] ** 2

    mag1 = np.sqrt(mag1) 
    mag2 = np.sqrt(mag2) 

    return ( dotP / (mag1 * mag2) )

###################################################################
# Using the formula from the article
###################################################################
def adjustedCosineSimilarity(vect1, vect2):
    avg1 = 0.0
    avg2 = 0.0

    for i in range (len(vect1)):
        avg1 += vect1[i]
        avg2 += vect2[i]

    avg1 = avg1 / len(vect1)
    avg2 = avg2 / len(vect2)

    dotP = 0
    sqrt1 = 0.0
    sqrt2 = 0.0

    for i in range (len(vect1)) : 
        dotP += ( int(vect1[i]) - avg1 ) * ( int(vect2[i]) - avg2 )
        sqrt1 += ( (vect1[i] - avg1) ) ** 2 
        sqrt2 += ( (vect2[i] - avg2) ) ** 2

    sqrt1 =  np.sqrt(sqrt1) 
    sqrt2 =  np.sqrt(sqrt2) 

    return ( dotP / (sqrt1 * sqrt2) )

#########################################################################

#-------------------------MAIN-------------------------------------------
# Need insert correct location of image, use '/' not '\'
image1 = Image.open("C:/Users/chunh/Desktop/Python practice/3.png")
image2 = Image.open("C:/Users/chunh/Desktop/Python practice/7.png")

pixel_Matrices1 = np.array( image1 )

#Convert matrix into vector
ori_Vect = np.reshape(  pixel_Matrices1, ( len(pixel_Matrices1) * len(pixel_Matrices1[0]) )  )

modified_Vect = ori_Vect.copy()

# Modified all pixels become range of 0 until 155
# Kind of standardize the pixel to prevent overflow when add with brightness
# Real focus is on modified_Vect and brighten_Vect
for i in range (len(modified_Vect)) :
    if (modified_Vect[i] >= 155) :
        modified_Vect[i] -= 100

#print("Calculating CS and aCS of 2 different image")





print("Calculating CS and aCS of 2 similar image with different brightness")

brighten_Vect = modified_Vect.copy()

brightness = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

for i in range ( len(brightness) ) :
    #Increase brightness of each pixel 
    for j in range ( len(brighten_Vect) ) :
        brighten_Vect[j] += brightness[i]


    similar2 = cosineSimilarity(modified_Vect, brighten_Vect)
    a_similar2 = adjustedCosineSimilarity(modified_Vect, brighten_Vect)

    difference = abs(a_similar2 - similar2)

    print("Difference of brightness: %i" %brightness[i])
    print("Cosine similarity: %f" %similar2)
    print("Adjusted cosine similarity: %f" %a_similar2)
    print("Differences between CS and aCS: %f" %difference)
    print()

    # After CS calculation, reset the vector back the original value
    # to prevent accumulation of value
    # Analogy: x+10 change back to x then only proceed to x+20
    if (brightness[i] != 100) :
        for j in range ( len(brighten_Vect) ) :
            brighten_Vect[j] -= brightness[i]

# Change back to matrix first, then convert back to image
modified_Vect = np.reshape(modified_Vect, ( len(pixel_Matrices1), len(pixel_Matrices1[0]) )  )
img1 = Image.fromarray(modified_Vect, image1.mode)

brighten_Vect = np.reshape(brighten_Vect, ( len(pixel_Matrices1), len(pixel_Matrices1[0])) )
img2 = Image.fromarray(brighten_Vect, image1.mode)

img1.show()
img2.show()