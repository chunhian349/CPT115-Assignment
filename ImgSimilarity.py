#Import Python Imaging Library 
from PIL import Image
#Import numpy math library
import numpy as np


###############################################################################################
# Data stored is type int8 ranging from (0-255) when convert image into matrix
# Make sure open the folder containing the image 
# so that user can direct input the name of image(.png/others) without specifiying its location
# dotP : dot product
# mag : magnitude
################################################################################################
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



#######################################################################
# Read image file, convert into a matrix then return as a vector
#######################################################################
def imgToVect(img_name) :
    # Read image from opened folder
    img = Image.open(img_name)

    #Convert image into matrices
    pixel_Matrix = np.array(img)

    #Convert matrices into vector
    vect = np.reshape(  pixel_Matrix, ( len(pixel_Matrix) * len(pixel_Matrix[0]) )  )

    return vect



#########################################################################
# Calculate CS and aCS of 2 different images
#########################################################################

def calc_2_Images() : 
    img_name1 = str(input("Enter filename of first image: "))
    vect1 = imgToVect(img_name1)

    img_name2 = str(input("Enter filename of second image: "))
    vect2 = imgToVect(img_name2)

    #Calculation and display result
    CS = cosineSimilarity(vect1, vect2)
    aCS = adjustedCosineSimilarity(vect1, vect2)
    diff = abs( CS - aCS )

    print("\n                Calculation Result                ")
    print("**************************************************")
    print("Cosine similarity: %f" %CS)
    print("Adjusted cosine similarity: %f" %aCS)
    print("Differences between CS and aCS: %f" %diff)
    print("**************************************************")

    input("\nPress any key to continue...")



##########################################################################################
# Demonstrate effectiveness of aCS
##########################################################################################

def aCS_demostration() :
    img_name = str(input("Enter filename of an image: "))

    ori_Vect = imgToVect(img_name)
    
    modified_Vect = ori_Vect.copy()

    # Modified all pixels become range of 0 until 155
    # Kind of standardize the pixel to prevent overflow when add with brightness
    # Real focus is on modified_Vect and brighten_Vect
    for i in range (len(modified_Vect)) :
        if (modified_Vect[i] >= 155) :
            modified_Vect[i] -= 100

    brighten_Vect = modified_Vect.copy()

    brightness = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    CS = np.empty(11)
    aCS = np.empty(11)
    diff = np.empty(11)

    for i in range ( len(brightness) ) :
        #Increase brightness of each pixel 
        for j in range ( len(brighten_Vect) ) :
            brighten_Vect[j] += brightness[i]

        #Calculation
        CS[i] = cosineSimilarity(modified_Vect, brighten_Vect) 
        aCS[i] = adjustedCosineSimilarity(modified_Vect, brighten_Vect)
        diff[i] = abs(CS[i] - aCS[i])

        # After calculation, reset the vector back the original value
        # to prevent accumulation of value
        # Analogy: x+10 change back to x then only proceed to x+20
        if (brightness[i] != 100) :
            for j in range ( len(brighten_Vect) ) :
                brighten_Vect[j] -= brightness[i]

    print("\n                               Table of calculation results                               ")
    print("******************************************************************************************")
    print("Brightness increment\tCosine similarity\tAdjusted cosine similarity\tDifferences")
    print("******************************************************************************************")
    for i in range(len(CS)) :
        print('{:<20}'.format(brightness[i]), end='\t')
        print( '{:.6f}{:>8}'.format(CS[i], " "), end='\t')
        print( '{:.6f}{:>17}'.format(aCS[i], " "), end='\t')
        print( '{:.6f}{:>2}'.format(diff[i], " ")   )

    print("******************************************************************************************")

    print("Notice that aCS always 1, means both images are same regardless of brightness")
    input("Press any key to continue...")



#################################################################################################################
#---------------------------------------------------MAIN---------------------------------------------------------

print("This program will compare images using cosine similarity and adjusted cosine similarity...")

while(True): 
    print("\n--------------Cosine Similarity(CS) and Adjusted Cosine Similarity(aCS) calculator-----------------")
    print("1: Calculate CS and aCS of 2 different images")
    print("2: Demonstrate effectiveness of aCS for an images with different brightness increment")
    print("3: End the program")
    choice = int( input("Please enter number: ") )

    while(choice<1 or choice>3):
        choice = int( input("You entered invalid input, try again: ") )

    if(choice == 1):
        calc_2_Images()

    elif(choice == 2):
        aCS_demostration()

    else:
        break

#End of program
