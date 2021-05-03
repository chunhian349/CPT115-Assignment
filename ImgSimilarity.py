###############################################################################################
# The program is implemented using Visual Studio Code
# Please make sure open the folder containing the images so that user can direct input the name
# of image(.png/others) without specifiying its location.
# The program designed for 2 images with same size for cosine similarity calculation.
###############################################################################################

#Import Python Imaging Library 
from PIL import Image
#Import numpy math library
import numpy as np

###############################################################################################
# Function that calculate cosine similarity.
# dotP : dot product
# mag : magnitude
################################################################################################
def cosineSimilarity(vect1, vect2):
    dotP = 0
    mag1 = 0.0
    mag2 = 0.0

    for i in range (len(vect1)) : 
        dotP += vect1[i] * vect2[i]   
        mag1 += vect1[i] ** 2 
        mag2 += vect2[i] ** 2

    mag1 = np.sqrt(mag1) 
    mag2 = np.sqrt(mag2) 

    return ( dotP / (mag1 * mag2) )



################################################################################################
# Function that calculate adjusted cosine similarity.
# avg : Average pixels in the vector
# sqrt1 : First square root part of denominator in the formula
# sqrt2 : Second square root part of denominator in the formula
################################################################################################
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
        dotP += ( vect1[i] - avg1 ) * ( vect2[i] - avg2 )
        sqrt1 += ( vect1[i] - avg1 ) ** 2 
        sqrt2 += ( vect2[i] - avg2 ) ** 2

    sqrt1 =  np.sqrt(sqrt1) 
    sqrt2 =  np.sqrt(sqrt2) 

    return ( dotP / (sqrt1 * sqrt2) )



################################################################################################
# Read image file, convert into a matrix then return as a vector.
################################################################################################
def imgToVect(img_name) :
    # Read image from opened folder
    img = Image.open(img_name)

    # Convert image into matrices of pixels
    # Need convert into int64 since pixel are stored in int8
    # If not, overflow may occur and affect the calculation
    pixel_Matrices = np.array(img, dtype='int64')

    # Convert matrices into a vector (from 2d array to 1d array)
    vect = np.reshape( pixel_Matrices,  pixel_Matrices.size )

    return vect



#########################################################################
# Calculate CS and aCS of 2 different images then display it.
# Ask user to enter names of 2 images to be compared.
# Error will occur if the image was not found.
#########################################################################

def calc_2_Images() : 
    img_name1 = str(input("Enter filename of first image: "))
    vect1 = imgToVect(img_name1)

    img_name2 = str(input("Enter filename of second image: "))
    vect2 = imgToVect(img_name2)

    if (vect1.size == vect2.size):
        #Calculation and display result
        CS = cosineSimilarity(vect1, vect2)
        aCS = adjustedCosineSimilarity(vect1, vect2)
        diff = abs( CS - aCS )

        print("\n                Calculation Result                ")
        print("***************************************************")
        print("Cosine similarity:                        %f" %CS)
        print("Adjusted cosine similarity:               %f" %aCS)
        print("Differences between CS and aCS:           %f" %diff)
        print("***************************************************")

    else:
        print("\nBoth images should have same size, try again later.")

    input("\nPress any key to continue...")



##########################################################################################
# Demonstrate effectiveness of aCS.
# Modify all pixels become range 0 until 155 and store it in a new copy of vector.
# Another copy of the modified vector will be used to increase brightness then compare the
# CS and aCS (between modified vector and brighten vector).
# Brightness increment from 0 to 100 to show aCS is 1 for every brightness increment.
##########################################################################################

def aCS_Demostration() :
    #User enter name of an image, then read the file and get its vector
    img_name = str(input("Enter filename of an image: "))

    ori_Vect = imgToVect(img_name)
    
    modified_Vect = ori_Vect.copy()

    # Modified all pixels become range of 0 until 155
    # Prevent overflow when add with brightness
    for i in range (len(modified_Vect)) :
        if (modified_Vect[i] >= 155) :
            modified_Vect[i] -= 100

    # The pixel of this vector will increse by brightness array 
    # then compare back with modified vector 
    brighten_Vect = modified_Vect.copy()

    # Value of pixel to be added on brighten vector
    brightness = np.array([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])

    # To store the calculation result for each brightness increment
    CS = np.linspace(0, 0, 11)
    aCS = np.linspace(0, 0, 11)
    diff = np.linspace(0, 0, 11)

    for i in range ( len(brightness) ) :
        #Increase brightness of each pixel based on value of brightness[i]
        for j in range ( len(brighten_Vect) ) :
            brighten_Vect[j] += brightness[i]

        #Calculation
        CS[i] = cosineSimilarity(modified_Vect, brighten_Vect) 
        aCS[i] = adjustedCosineSimilarity(modified_Vect, brighten_Vect)
        diff[i] = abs(CS[i] - aCS[i])

        # After calculation, restore the vector back the original value
        # to prevent accumulation of value
        # Analogy: x+10 change back to x then only proceed to x+20
        for j in range ( len(brighten_Vect) ) :
            brighten_Vect[j] -= brightness[i]

    # Display all the calculation result 
    print("\n                                    Calculation results                                   ")
    print("*******************************************************************************************")
    print("Brightness increment\tCosine similarity\tAdjusted cosine similarity\tDifferences")
    print("*******************************************************************************************")
    for i in range(len(CS)) :
        print('{:<20}'.format(brightness[i]), end='\t')
        print( '{:.6f}{:>8}'.format(CS[i], " "), end='\t')
        print( '{:.6f}{:>17}'.format(aCS[i], " "), end='\t')
        print( '{:.6f}{:>2}'.format(diff[i], " ")   )

    print("*******************************************************************************************")

    input("\nPress any key to continue...")

#################################################################################################################



#----------------------------------------------MAIN PROGRAM------------------------------------------------------
# Menu loop allow user to compare similarity as many times as desired
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
        aCS_Demostration()

    else:
        break

#End of program
