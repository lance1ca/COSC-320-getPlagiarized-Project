import pandas as pd
import os
import time
import threading
import matplotlib.pyplot as plt

#Importing Algorithm Classes
from KMP import KMP
from LCSS import LCSS
from RabinKarp import RabinKarp

#Global Variables:
allDataDF = pd.DataFrame()
sampleDataDF = pd.DataFrame()

dataFolderPath = ""
allDataFileName = 'masterData.csv'
sampleDataFileName = 'sampleData.csv'

kmp = KMP()
lcss = LCSS()
rabinKarp = RabinKarp()

inputSizes = []
elapsedTimes = []
KMPElapsedTimes = []
LCSSElapsedTimes = []
RabinKarpElapsedTimes = []




def plotResults():
    global inputSizes
    global elapsedTimes


    print(inputSizes)
    print(KMPElapsedTimes)
    plt.plot(inputSizes, KMPElapsedTimes, 'bo-')
    plt.xlabel('Input size n')
    plt.ylabel('Runtime (seconds)')
    plt.title('Runtime of KMP Algorithm')
    plt.show()


    print(inputSizes)
    print(LCSSElapsedTimes)
    plt.plot(inputSizes, LCSSElapsedTimes, 'bo-')
    plt.xlabel('Input size n')
    plt.ylabel('Runtime (seconds)')
    plt.title('Runtime of LCSS Algorithm')
    plt.show()


    print(inputSizes)
    print(RabinKarpElapsedTimes)
    plt.plot(inputSizes, RabinKarpElapsedTimes, 'bo-')
    plt.xlabel('Input size n')
    plt.ylabel('Runtime (seconds)')
    plt.title('Runtime of Rabin-Karp Algorithm')
    plt.show()


    # Create data for plot 1
    x = inputSizes
    y1 = KMPElapsedTimes

    # Create data for plot 2
    y2 = LCSSElapsedTimes

    # Create data for plot 3
    y3 = RabinKarpElapsedTimes

    # Plot all three plots on the same axes
    plt.plot(x, y1, 'bo-', label='KMP')
    plt.plot(x, y2, 'ro-', label='LCSS')
    plt.plot(x, y3, 'go-', label='Rabin-Karp')

    # Set x and y axis labels and title
    plt.xlabel('Input size n')
    plt.ylabel('Runtime (seconds)')
    plt.title('Runtime of All Plagiarism Detection Algorithms')

    # Add a legend
    plt.legend()

    # Show the merged plot
    plt.show()


def createSampleCSV(n):
    global allDataDF
    global sampleDataDF
    global sampleDataFileName
    global inputSizes
    print("Creating "+ sampleDataFileName +" now.")
    sampleDataDF = allDataDF.sample(frac=n)
    inputSizes.append(sampleDataDF.shape[0])
    sampleDataDF.to_csv(os.path.join(dataFolderPath,sampleDataFileName), index=False)

def iterateCombinedRow(sampleRow, combinedRow,algorithmType):
    # print("-------------------------------------")
    # print(algorithmType +": \n")
    # print(sampleRow)
    # print(combinedRow)
    # print("-------------------------------------")
    
    if algorithmType == "KMP":
        kmp.KMPSearch(str(sampleRow[2]), str(combinedRow[2]))
    elif algorithmType == "LCSS":
        lcss.lcs(str(sampleRow[2]), str(combinedRow[2]))
    elif algorithmType == "Rabin-Karp":
        rabinKarp.RabinKarpAlgo(str(sampleRow[2]), str(combinedRow[2]),101)
    else:
        print("Algorithm type passed was invalid")

def iterateSampleRow(sampleRow,algorithmType):
    allDataDF.apply(lambda combinedRow: iterateCombinedRow(sampleRow,combinedRow,algorithmType),axis=1)

def startCheck(algorithmType):
    sampleDataDF.apply(lambda sampleRow: iterateSampleRow(sampleRow,algorithmType),axis=1)

def checkForPlagiarism(n):
    global KMPElapsedTimes
    global LCSSElapsedTimes
    global RabinKarpElapsedTimes

    print("Checking for Plagiarism for n percentage: " + str(n*100) +"%.")
    threadOne = threading.Thread(target=startCheck, args=("KMP",))
    threadTwo = threading.Thread(target=startCheck, args=("LCSS",))
    threadThree = threading.Thread(target=startCheck, args=("Rabin-Karp",))

    threadOneStartTime = time.time()
    threadOne.start()

    threadTwoStartTime = time.time()
    threadTwo.start()

    threadThreeStartTime = time.time()
    threadThree.start()

    
    threadOne.join()
    threadOneEndTime = time.time()

    threadTwo.join()
    threadTwoEndTime = time.time()

    threadThree.join()
    threadThreeEndTime = time.time()

    threadOneElapsedTime = threadOneEndTime - threadOneStartTime
    KMPElapsedTimes.append(threadOneElapsedTime)

    threadTwoElapsedTime = threadTwoEndTime - threadTwoStartTime
    LCSSElapsedTimes.append(threadTwoElapsedTime)

    threadThreeElapsedTime = threadThreeEndTime - threadThreeStartTime
    RabinKarpElapsedTimes.append(threadThreeElapsedTime)



def createCombinedCSV():
    global allDataDF
    global allDataFileName

    print("Creating "+ allDataFileName +" now.")
    for currentFile in os.listdir(dataFolderPath):
            if currentFile.endswith('.csv'):
                currentFilePath = os.path.join(dataFolderPath,currentFile)
                try:
                    tempDF = pd.read_csv(currentFilePath,usecols=[0,1,3],encoding='utf-8')
                    allDataDF = pd.concat([allDataDF,tempDF],ignore_index=True)
                except:
                    print(currentFile + " has some empty values or columns. Skipping file.")
    allDataDF.to_csv(os.path.join(dataFolderPath,allDataFileName), index=False)

def plagiarismDetectorInitialization(n):

    print("Starting Plagiarism Detector initialization.")
    global dataFolderPath
    global allDataFileName
    global sampleDataFileName

    global allDataDF
    global sampleDataDF

    if os.name == 'nt':  # Windows
        dataFolderPath = '.\\test'   # Use backslash for Windows
    else:  # Mac or Linux
        dataFolderPath = './data'   # Use forward slash for Mac or Linux

    #Create the combined csv file if it does not exist
    if (not (os.path.exists(os.path.join(dataFolderPath,allDataFileName)))):
        print("Combined CSV file "+ allDataFileName + " does not exist.")
        createCombinedCSV()
    else:
        print(allDataFileName + " exists.")
        print("Reading "+allDataFileName+" into data frame.")
        allDataDF = pd.read_csv(os.path.join(dataFolderPath,allDataFileName),encoding='utf-8')

    if (os.path.exists(os.path.join(dataFolderPath,sampleDataFileName))):
        os.remove(os.path.join(dataFolderPath,sampleDataFileName))
    
    
    
    createSampleCSV(n)

    
    print("Plagiarism Detector initialization complete.")


def runPlagiarismDetector():
    global dataFolderPath
    global sampleDataFileName
    global elapsedTimes
    print("Starting Plagiarism Detector.")

    nPercentages = [0.1,0.2,0.3,0.4,0.5]

    for n in nPercentages:
        plagiarismDetectorInitialization(n)
        checkForPlagiarism(n)
        os.remove(os.path.join(dataFolderPath,sampleDataFileName))
    

    plotResults()





#Run Detector
runPlagiarismDetector()