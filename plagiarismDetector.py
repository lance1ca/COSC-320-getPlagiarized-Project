import pandas as pd
import os
import time

#Global Variables:
allDataDF = pd.DataFrame()
sampleDataDF = pd.DataFrame()

dataFolderPath = ""
allDataFileName = 'masterData.csv'
sampleDataFileName = 'sampleData.csv'

def plotResults():
    print("print results")

def createSampleCSV():
    global allDataDF
    global sampleDataDF
    print("creating sample csv")
    sampleDataDF = allDataDF.sample(frac=0.2)
    sampleDataDF.to_csv(os.path.join(dataFolderPath,sampleDataFileName), index=False)


def checkForPlagiarism():
    print("going to check now")


def createCombinedCSV():
    global allDataDF
    for currentFile in os.listdir(dataFolderPath):
            if currentFile.endswith('.csv'):


                currentFilePath = os.path.join(dataFolderPath,currentFile)

                try:
                    tempDF = pd.read_csv(currentFilePath,usecols=[0,1,3],encoding='utf-8')
                    allDataDF = pd.concat([allDataDF,tempDF],ignore_index=True)
                except:
                    print(currentFile + " has some empty values or columns. Skipping file.")
    allDataDF.to_csv(os.path.join(dataFolderPath,allDataFileName), index=False)


def runPlagiarismDetector():
    global dataFolderPath
    global allDataFileName
    global sampleDataFileName

    global allDataDF
    global sampleDataDF

    # Get the current operating system
    if os.name == 'nt':  # Windows
        dataFolderPath = '.\\data'   # Use backslash for Windows
    else:  # Mac or Linux
        dataFolderPath = './data'   # Use forward slash for Mac or Linux

    print(os.path.join(dataFolderPath,allDataFileName))

    #Create the combined csv file if it does not exist
    if (not (os.path.exists(os.path.join(dataFolderPath,allDataFileName)))):
        createCombinedCSV()
    else:
        print("Reading "+allDataFileName+" into data frame.")
        allDataDF = pd.read_csv(os.path.join(dataFolderPath,allDataFileName),encoding='utf-8')

    if (not (os.path.exists(os.path.join(dataFolderPath,sampleDataFileName)))):
        createSampleCSV()
    else:
        print("Reading " + sampleDataFileName + " into data frame.")
        sampleDataDF = pd.read_csv(os.path.join(dataFolderPath,sampleDataFileName),encoding='utf-8')
    
    
    checkForPlagiarism()
    plotResults()


#Run Detector
runPlagiarismDetector()
print(allDataDF)