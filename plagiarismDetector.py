# COSC 320 - Term Project
# Group Members Chad Lantz (77879460), Prashant Dutt (63565634), Lance Rogan (62708938)

# Imports for pandas, os, time, threading and matplotlib
import pandas as pd
import os
import time
import threading
import matplotlib.pyplot as plt

# Importing Algorithm Classes
from KMP import KMP
from LCSS import LCSS
from RabinKarp import RabinKarp

# Global Variables:

# Dataframe global variables
allDataDF = pd.DataFrame()
sampleDataDF = pd.DataFrame()
kmp_data_df = pd.DataFrame()
lcss_data_df = pd.DataFrame()
rabin_karp_data_df = pd.DataFrame()

# folder path and file name global variables
dataFolderPath = ""
allDataFileName = 'masterData.csv'
sampleDataFileName = 'sampleData.csv'

# algorithm object global variables
kmp = KMP()
lcss = LCSS()
rabinKarp = RabinKarp()

# elapsed times and input size list global variables
inputSizes = []
elapsedTimes = []
KMPElapsedTimes = []
LCSSElapsedTimes = []
RabinKarpElapsedTimes = []


# Function to plot the results of the 3 algorithms for the various input sizes
def plotResults():

    # Define global variables to be used
    global inputSizes
    global elapsedTimes

    # Print the input sizes used, and the KMP elapsed times
    # Then plot the input sizes on x axis, and times on the y axis with x and y labels (use plt.show to plot it)
    print(inputSizes)
    print(KMPElapsedTimes)
    plt.plot(inputSizes, KMPElapsedTimes, 'bo-')
    plt.xlabel('Input size n')
    plt.ylabel('Runtime (seconds)')
    plt.title('Runtime of KMP Algorithm')
    plt.show()

    # Print the input sizes used, and the LCSS elapsed times
    # Then plot the input sizes on x axis, and times on the y axis with x and y labels (use plt.show to plot it)
    print(inputSizes)
    print(LCSSElapsedTimes)
    plt.plot(inputSizes, LCSSElapsedTimes, 'ro-')
    plt.xlabel('Input size n')
    plt.ylabel('Runtime (seconds)')
    plt.title('Runtime of LCSS Algorithm')
    plt.show()

    # Print the input sizes used, and the Rabin-Karp elapsed times
    # Then plot the input sizes on x axis, and times on the y axis with x and y labels (use plt.show to plot it)
    print(inputSizes)
    print(RabinKarpElapsedTimes)
    plt.plot(inputSizes, RabinKarpElapsedTimes, 'go-')
    plt.xlabel('Input size n')
    plt.ylabel('Runtime (seconds)')
    plt.title('Runtime of Rabin-Karp Algorithm')
    plt.show()

    # Set x as the input sizes
    x = inputSizes

    # Set the various y values as the different elapsed times for the 3 algorithms
    y1 = KMPElapsedTimes
    y2 = LCSSElapsedTimes
    y3 = RabinKarpElapsedTimes

    # Plot all algorithms on the same x axis, label them, and make them different colors
    plt.plot(x, y1, 'bo-', label='KMP')
    plt.plot(x, y2, 'ro-', label='LCSS')
    plt.plot(x, y3, 'go-', label='Rabin-Karp')

    # Set title, x and y labels
    plt.xlabel('Input size n')
    plt.ylabel('Runtime (seconds)')
    plt.title('Runtime of All Plagiarism Detection Algorithms')

    # Add a legend for user to know which is which
    plt.legend()

    # Show the plot with all algorithms on it
    plt.show()

# -----------------------------------------------------------------

# These functions iterate over each sample and combined row, and run the KMP algorithm on each sample and combined rows content to check if it matches
# and thus checking for plagiarism. I.e, it compares each sample row to each combined row using KMP

# Function to iterate the combined row for KMP
# We apply the lambda function iterateCombinedRowKMP for each sample row and combined row and we run a KMP search on the content in each of these
# Singular rows passed in to check for plagiarism and see if there is a match


def iterateCombinedRowKMP(sampleRow, combinedRow):
    kmp.KMPSearch(str(sampleRow[2]), str(combinedRow[2]))

# Function to iterate the sampleRow for KMP
# We apply the lambda function iterateCombinedRowKMP for each row in the kmp_data_df (combined dataframe for KMP)


def iterateSampleRowKMP(sampleRow):
    kmp_data_df.apply(lambda combinedRow: iterateCombinedRowKMP(
        sampleRow, combinedRow), axis=1)

# Function to start the plagiarism check using KMP
# We apply the lambda function iterateSampleRowKMP for each row in the sampleDataDF


def startCheckKMP():
    sampleDataDF.apply(
        lambda sampleRow: iterateSampleRowKMP(sampleRow), axis=1)
# -----------------------------------------------------------------
# These functions iterate over each sample and combined row, and run the LCSS algorithm on each sample and combined rows content to check if it matches
# and thus checking for plagiarism. I.e, it compares each sample row to each combined row using LCSS

# Function to iterate the combined row for LCSS
# We apply the lambda function iterateCombinedRowLCSS for each sample row and combined row and we run a LCSS search on the content in each of these
# Singular rows passed in to check for plagiarism and see if there is a match


def iterateCombinedRowLCSS(sampleRow, combinedRow):
    lcss.lcs(str(sampleRow[2]), str(combinedRow[2]))

# Function to iterate the sampleRow for LCSS
# We apply the lambda function iterateCombinedRowLCSS for each row in the lcss_data_df (combined dataframe for LCSS)


def iterateSampleRowLCSS(sampleRow):
    lcss_data_df.apply(lambda combinedRow: iterateCombinedRowLCSS(
        sampleRow, combinedRow), axis=1)

# Function to start the plagiarism check using LCSS
# We apply the lambda function iterateSampleRowLCSS for each row in the sampleDataDF


def startCheckLCSS():
    sampleDataDF.apply(
        lambda sampleRow: iterateSampleRowLCSS(sampleRow), axis=1)


# -----------------------------------------------------------------
# These functions iterate over each sample and combined row, and run the RabinKarp algorithm on each sample and combined rows content to check if it matches
# and thus checking for plagiarism. I.e, it compares each sample row to each combined row using RabinKarp

# Function to iterate the combined row for RabinKarp
# We apply the lambda function iterateCombinedRowRabinKarp for each sample row and combined row and we run a RabinKarp search on the content in each of these
# Singular rows passed in to check for plagiarism and see if there is a match
def iterateCombinedRowRabinKarp(sampleRow, combinedRow):
    rabinKarp.RabinKarpAlgo(str(sampleRow[2]), str(combinedRow[2]), 101)

# Function to iterate the sampleRow for RabinKarp
# We apply the lambda function iterateCombinedRowRabinKarp for each row in the rabin_karp_data_df (combined dataframe for RabinKarp)


def iterateSampleRowRabinKarp(sampleRow):
    rabin_karp_data_df.apply(lambda combinedRow: iterateCombinedRowRabinKarp(
        sampleRow, combinedRow), axis=1)

# Function to start the plagiarism check using RabinKarp
# We apply the lambda function iterateSampleRowRabinKarp for each row in the sampleDataDF


def startCheckRabinKarp():
    sampleDataDF.apply(
        lambda sampleRow: iterateSampleRowRabinKarp(sampleRow), axis=1)

# -----------------------------------------------------------------
# This function is the bulk of the code. It checks for plagiarism using KMP, LCSS, and RabinKarp and runs these functions for comparing each sample row and each combined row
# from the test and master dataset. This function runs these 3 functions on separate threads to optimize performance and on separate dataframes to optimizie performance. It times each run
# of a given input size as well.


def checkForPlagiarism(n):

    # Define global variables to be used
    global KMPElapsedTimes
    global LCSSElapsedTimes
    global RabinKarpElapsedTimes
    global allDataDF
    global kmp_data_df
    global lcss_data_df
    global rabin_karp_data_df

    # Create separate dataframes for each thread as a deep copy
    kmp_data_df = allDataDF.copy(deep=True)
    lcss_data_df = allDataDF.copy(deep=True)
    rabin_karp_data_df = allDataDF.copy(deep=True)

    print("Checking for Plagiarism for n percentage: " + str(n*100) + "%.")

    # Define each thread to target their specific function
    threadOne = threading.Thread(target=startCheckKMP)
    threadTwo = threading.Thread(target=startCheckRabinKarp)
    threadThree = threading.Thread(target=startCheckLCSS)

    # Start thread timers and start each thread
    threadOneStartTime = time.time()
    threadOne.start()

    threadTwoStartTime = time.time()
    threadTwo.start()

    threadThreeStartTime = time.time()
    threadThree.start()

    # Wait for each thread to finish and end the thread timers
    threadOne.join()
    threadOneEndTime = time.time()

    threadTwo.join()
    threadTwoEndTime = time.time()

    threadThree.join()
    threadThreeEndTime = time.time()

    # Calculate each threads elapsed time and add it to the specific algorihms elapsedTimes list
    threadOneElapsedTime = threadOneEndTime - threadOneStartTime
    KMPElapsedTimes.append(threadOneElapsedTime)

    threadTwoElapsedTime = threadTwoEndTime - threadTwoStartTime
    RabinKarpElapsedTimes.append(threadTwoElapsedTime)

    threadThreeElapsedTime = threadThreeEndTime - threadThreeStartTime
    LCSSElapsedTimes.append(threadThreeElapsedTime)

# -----------------------------------------------------------------
# This function creates a combined CSV file from a given directory if it doesnt already exist


def createCombinedCSV():

    # Define global variables to be used
    global allDataDF
    global allDataFileName

    print("Creating " + allDataFileName + " now.")

    # For each file in the given directory, if the file ends in csv, load this file into a dataframe, and append this tempDF to our master dataframe
    for currentFile in os.listdir(dataFolderPath):
        if currentFile.endswith('.csv'):
            # Specify the filepath to this specific file
            currentFilePath = os.path.join(dataFolderPath, currentFile)
            try:
                # Read in file to tempDF with only the specific columns (reviewId,userName,content) and utf-8 encoding.
                tempDF = pd.read_csv(currentFilePath, usecols=[
                                     0, 1, 3], encoding='utf-8')
                allDataDF = pd.concat([allDataDF, tempDF], ignore_index=True)
            except:
                # If the file is empty or is missing data skip it and let the user know
                print(currentFile +
                      " has some empty values or columns. Skipping file.")
    # Convert the dataframe with combined data into a csv file with a given name
    allDataDF.to_csv(os.path.join(
        dataFolderPath, allDataFileName), index=False)


# -----------------------------------------------------------------
# This function creates a sample CSV file for a random % of data from the master csv file to run our algorithm
def createSampleCSV(n):

    # Define global variables to be used
    global allDataDF
    global sampleDataDF
    global sampleDataFileName
    global inputSizes
    print("Creating " + sampleDataFileName + " now.")

    # Create a sample dataframe which is a random selection of n (% value) of the master dataframe
    sampleDataDF = allDataDF.sample(frac=n)

    # Append input size (sample dataframe size aka number of rows)
    inputSizes.append(sampleDataDF.shape[0])

    # Convert sample dataframe to csv file
    sampleDataDF.to_csv(os.path.join(
        dataFolderPath, sampleDataFileName), index=False)

# -----------------------------------------------------------------
# Function to initialize the detector and initialize the required files


def plagiarismDetectorInitialization(n):

    print("Starting Plagiarism Detector initialization.")

    # Define global variables to be used
    global dataFolderPath
    global allDataFileName
    global sampleDataFileName
    global allDataDF
    global sampleDataDF

    # Check if the operating system is windows or linux, and specific the dataFolderPath as follows
    if os.name == 'nt':  # Windows
        dataFolderPath = '.\\testData'   # Use backslash for Windows
    else:  # Mac or Linux
        dataFolderPath = './testData'   # Use forward slash for Mac or Linux

    # Create the combined csv file if it does not exist. Otherwise, read the csv file into dataframe
    if (not (os.path.exists(os.path.join(dataFolderPath, allDataFileName)))):
        print("Combined CSV file " + allDataFileName + " does not exist.")
        createCombinedCSV()
    else:
        print(allDataFileName + " exists.")
        print("Reading "+allDataFileName+" into data frame.")
        allDataDF = pd.read_csv(os.path.join(
            dataFolderPath, allDataFileName), encoding='utf-8')

    # If the sample document exists, delete it
    if (os.path.exists(os.path.join(dataFolderPath, sampleDataFileName))):
        os.remove(os.path.join(dataFolderPath, sampleDataFileName))

    # Create a new sample csv file with random n % of master data
    createSampleCSV(n)

    print("Plagiarism Detector initialization complete.")

# -----------------------------------------------------------------
# This function runs the detector


def runPlagiarismDetector():

    # Define global variables to be used
    global dataFolderPath
    global sampleDataFileName
    global elapsedTimes
    print("Starting Plagiarism Detector.")

    # percentages for the sample document to take
    nPercentages = [0.1, 0.2, 0.3, 0.4, 0.5]

    # For each percentage we run the initialization to create the new sample document, check for plagiarism for that input size n%, and then remove the sample document and repeat
    for n in nPercentages:
        plagiarismDetectorInitialization(n)
        checkForPlagiarism(n)
        os.remove(os.path.join(dataFolderPath, sampleDataFileName))

    # After all input sizes are done we plot the results
    plotResults()

# -----------------------------------------------------------------


# Call the runPlagiarismDetector function to start the detector
runPlagiarismDetector()
