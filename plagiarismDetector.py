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
sampleDataFileName = 'sampleDataa.csv'

kmp = KMP()
lcss = LCSS()
rabinKarp = RabinKarp()

inputSizes = []
elapsedTimes = []




def plotResults():
    global inputSizes
    global elapsedTimes
    print(inputSizes)
    print(elapsedTimes)
    plt.plot(inputSizes, elapsedTimes, 'bo-')
    plt.xlabel('Input size n')
    plt.ylabel('Runtime (seconds)')
    plt.title('Runtime of Plagiarism Algorithm')
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
        lcss.LCSS(str(sampleRow[2]), str(combinedRow[2]))
    elif algorithmType == "Rabin-Karp":
        rabinKarp.RabinKarpAlgo(str(sampleRow[2]), str(combinedRow[2]),101)
    else:
        print("Algorithm type passed was invalid")

def iterateSampleRow(sampleRow,algorithmType):
    allDataDF.apply(lambda combinedRow: iterateCombinedRow(sampleRow,combinedRow,algorithmType),axis=1)

def startCheck(algorithmType):
    sampleDataDF.apply(lambda sampleRow: iterateSampleRow(sampleRow,algorithmType),axis=1)

def checkForPlagiarism(n):
    print("Checking for Plagiarism for n percentage: " + str(n*100) +"%.")
    threadOne = threading.Thread(target=startCheck, args=("KMP",))
    #threadTwo = threading.Thread(target=startCheck, args=("LCSS",))
    #threadThree = threading.Thread(target=startCheck, args=("Rabin-Karp",))

    threadOne.start()
    #threadTwo.start()
    #threadThree.start()

    
    threadOne.join()
    #threadTwo.join()
    #threadThree.join()

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
        #print("Sample CSV file "+ sampleDataFileName + " does not exist.")
    createSampleCSV(n)
    # else:
    #     print(sampleDataFileName + " exists.")
    #     print("Reading " + sampleDataFileName + " into data frame.")
    #     sampleDataDF = pd.read_csv(os.path.join(dataFolderPath,sampleDataFileName),encoding='utf-8')
    
    print("Plagiarism Detector initialization complete.")


def runPlagiarismDetector():
    global dataFolderPath
    global sampleDataFileName
    global elapsedTimes
    print("Starting Plagiarism Detector.")

    nPercentages = [0.1,0.2,0.3,0.4,0.5]

    for n in nPercentages:
        start_time = time.time()
        plagiarismDetectorInitialization(n)
        checkForPlagiarism(n)
        end_time = time.time()
        elapsed_time = end_time - start_time
        elapsedTimes.append(elapsed_time)
        os.remove(os.path.join(dataFolderPath,sampleDataFileName))
    
    

    plotResults()


#Run Detector
runPlagiarismDetector()