import pandas as pd
import os
import time
import threading

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



def plotResults():
    print("Printing results")

def createSampleCSV():
    global allDataDF
    global sampleDataDF
    global sampleDataFileName
    print("Creating "+ sampleDataFileName +" now.")
    sampleDataDF = allDataDF.sample(frac=0.2)
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
        rabinKarp.RabinKarpAlgo(str(sampleRow[2]), str(combinedRow[2]))
    else:
        print("Algorithm type passed was invalid")

def iterateSampleRow(sampleRow,algorithmType):
    allDataDF.apply(lambda combinedRow: iterateCombinedRow(sampleRow,combinedRow,algorithmType),axis=1)

def startCheck(algorithmType):
    sampleDataDF.apply(lambda sampleRow: iterateSampleRow(sampleRow,algorithmType),axis=1)

def checkForPlagiarism():
    print("Checking for Plagiarism.")
    threadOne = threading.Thread(target=startCheck, args=("KMP",))
    threadTwo = threading.Thread(target=startCheck, args=("LCSS",))
    threadThree = threading.Thread(target=startCheck, args=("Rabin-Karp",))

    threadOne.start()
    threadTwo.start()
    threadThree.start()

    threadOne.join()
    threadTwo.join()
    threadThree.join()

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

def plagiarismDetectorInitialization():

    print("Starting Plagiarism Detector initialization.")
    global dataFolderPath
    global allDataFileName
    global sampleDataFileName

    global allDataDF
    global sampleDataDF

    if os.name == 'nt':  # Windows
        dataFolderPath = '.\\data'   # Use backslash for Windows
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

    if (not (os.path.exists(os.path.join(dataFolderPath,sampleDataFileName)))):
        print("Sample CSV file "+ sampleDataFileName + " does not exist.")
        createSampleCSV()
    else:
        print(sampleDataFileName + " exists.")
        print("Reading " + sampleDataFileName + " into data frame.")
        sampleDataDF = pd.read_csv(os.path.join(dataFolderPath,sampleDataFileName),encoding='utf-8')
    
    print("Plagiarism Detector initialization complete.")


def runPlagiarismDetector():
    print("Starting Plagiarism Detector.")
    plagiarismDetectorInitialization()
    checkForPlagiarism()
    plotResults()


#Run Detector
runPlagiarismDetector()