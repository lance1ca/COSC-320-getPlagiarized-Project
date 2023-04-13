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
kmp_data_df = pd.DataFrame()
lcss_data_df = pd.DataFrame()
rabin_karp_data_df = pd.DataFrame()

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
    plt.plot(inputSizes, LCSSElapsedTimes, 'ro-')
    plt.xlabel('Input size n')
    plt.ylabel('Runtime (seconds)')
    plt.title('Runtime of LCSS Algorithm')
    plt.show()


    print(inputSizes)
    print(RabinKarpElapsedTimes)
    plt.plot(inputSizes, RabinKarpElapsedTimes, 'go-')
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


#KMP
def iterateCombinedRowKMP(sampleRow, combinedRow):
        kmp.KMPSearch(str(sampleRow[2]), str(combinedRow[2]))
    

def iterateSampleRowKMP(sampleRow):
    kmp_data_df.apply(lambda combinedRow: iterateCombinedRowKMP(sampleRow,combinedRow),axis=1)

def startCheckKMP():
    sampleDataDF.apply(lambda sampleRow: iterateSampleRowKMP(sampleRow),axis=1)

#LCSS

def iterateCombinedRowLCSS(sampleRow, combinedRow):
        lcss.lcs(str(sampleRow[2]), str(combinedRow[2]))
    

def iterateSampleRowLCSS(sampleRow):
    lcss_data_df.apply(lambda combinedRow: iterateCombinedRowLCSS(sampleRow,combinedRow),axis=1)

def startCheckLCSS():
    sampleDataDF.apply(lambda sampleRow: iterateSampleRowLCSS(sampleRow),axis=1)

#Rabin Karp
def iterateCombinedRowRabinKarp(sampleRow, combinedRow):
        rabinKarp.RabinKarpAlgo(str(sampleRow[2]), str(combinedRow[2]),101)
    

def iterateSampleRowRabinKarp(sampleRow):
    rabin_karp_data_df.apply(lambda combinedRow: iterateCombinedRowRabinKarp(sampleRow,combinedRow),axis=1)

def startCheckRabinKarp():
    sampleDataDF.apply(lambda sampleRow: iterateSampleRowRabinKarp(sampleRow),axis=1)


def checkForPlagiarism(n):
    global KMPElapsedTimes
    global LCSSElapsedTimes
    global RabinKarpElapsedTimes
    global allDataDF

    global kmp_data_df
    global lcss_data_df
    global rabin_karp_data_df

    # Create separate dataframes for each thread
    kmp_data_df = allDataDF.copy(deep=True)
    lcss_data_df = allDataDF.copy(deep=True)
    rabin_karp_data_df = allDataDF.copy(deep=True)

    print("Checking for Plagiarism for n percentage: " + str(n*100) +"%.")
    threadOne = threading.Thread(target=startCheckKMP)
    threadTwo = threading.Thread(target=startCheckRabinKarp)
    threadThree = threading.Thread(target=startCheckLCSS)

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
    RabinKarpElapsedTimes.append(threadTwoElapsedTime)

    threadThreeElapsedTime = threadThreeEndTime - threadThreeStartTime
    LCSSElapsedTimes.append(threadThreeElapsedTime)



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
        dataFolderPath = '.\\testData'   # Use backslash for Windows
    else:  # Mac or Linux
        dataFolderPath = './testData'   # Use forward slash for Mac or Linux

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