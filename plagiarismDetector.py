import pandas as pd
import os

#Global Variables:
allDataDF = pd.DataFrame()
sampleDataDF = pd.DataFrame()

dataFolderPath = ""
allDataFileName = 'masterData.csv'

def plotResults():
    print("print results")

def createSampleCSV():
    print("create sample csv")


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

    # Get the current operating system
    if os.name == 'nt':  # Windows
        dataFolderPath = '.\\data'   # Use backslash for Windows
    else:  # Mac or Linux
        dataFolderPath = './data'   # Use forward slash for Mac or Linux

    print(os.path.join(dataFolderPath,allDataFileName))

    #Create the combined csv file if it does not exist
    if (not (os.path.exists(os.path.join(dataFolderPath,allDataFileName)))):
        createCombinedCSV()
    
    #Create the temporary csv to check fo plagiarism
    createSampleCSV()
    checkForPlagiarism()
    plotResults()


#Run Detector
runPlagiarismDetector()