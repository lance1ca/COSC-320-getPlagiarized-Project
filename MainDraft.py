import pandas as pd
import os
import unicodedata
import emoji
import time
import traceback
import matplotlib.pyplot as plt

#Creating a KMP object
from KMP import KMP

kmp = KMP()

elapsed_times = []

def initializeData():
    cwd = os.getcwd()

    # Print the current working directory
    print("Current working directory:", cwd)

    # Set the folder path
    folder_path = './test'

    # Get a list of all CSV files in the folder
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    # Initialize an empty dataframe
    df = pd.DataFrame()

    # Loop through the CSV files and read them into temporary dataframes
    for csv_file in csv_files:
        try:
            temp_df = pd.read_csv(os.path.join(folder_path, csv_file),usecols=[0,1,3],encoding='utf-8')
            df = pd.concat([df, temp_df], ignore_index=True)
        except Exception as e:
            print("File might be empty. There was an issue reading file with name: ", csv_file)
            #traceback.print_exc()
   

   #TO DO: ADD IN ERROR CHECKING IN CASE WE FORGET TO DELETE FILE
    df.to_csv('./data/COMBINED.csv', index=False)
   

def initializePlagiarizedData(percentage):

   
    combinedDF = pd.read_csv("./data/COMBINED.csv",encoding='utf-8')
    percentOfSize = (int) (percentage * len(combinedDF))
    plagiarizedDF = combinedDF.sample(n=percentOfSize)
    plagiarizedDF.to_csv('./data/PLAGIARIZED.csv', index=False)

    return percentage * len(combinedDF)
        



def checkForPlagiarism(version):
    combinedDF = pd.read_csv("./data/COMBINED.csv",encoding='utf-8')
    plagiarizedDF = pd.read_csv("./data/PLAGIARIZED.csv",encoding='utf-8')


    if(version == "KMP"):
        global start_plot_time
        start_plot_time = time.perf_counter()
        for index, plagiarizedRow in plagiarizedDF.iterrows():
            for index, originalRow in combinedDF.iterrows():
                    
                    try:
                        currOriginalUserName = originalRow['userName']
                        currOriginalRequestId = originalRow['reviewId']
                        currOriginalContent = originalRow['content']

                        currPlagiarizedRowUserName = plagiarizedRow['userName']
                        currPlagiarizedRequestId = plagiarizedRow['reviewId']
                        currPlagiarizedContent = plagiarizedRow['content']
                        
                        matched = kmp.KMPSearch(plagiarizedRow['content'],originalRow['content'])

                        if(matched):
                            print("Original text from \"{}\", \nwith requestId = \"{}\", \ntext = \"{}: \"".format(currOriginalUserName,currOriginalRequestId,currOriginalContent))
                            print("Plagiarized text from \"{}\", \nwith requestId = \"{}\", \ntext = \"{}: \"".format(currPlagiarizedRowUserName,currPlagiarizedRequestId,currPlagiarizedContent))
                            print("\n")

                    except Exception as e:
                        #print("An Error Occurred :(")
                        traceback.print_exc()
                        
        global end_plot_time
        end_plot_time = time.perf_counter()
        global elapsed_times
        elapsed_time = end_plot_time - start_plot_time
        elapsed_times.append(elapsed_time)






if os.path.exists("./data/COMBINED.csv"):
    os.remove("./data/COMBINED.csv")

if os.path.exists("./data/PLAGIARIZED.csv"):
    os.remove("./data/PLAGIARIZED.csv")

start_time = time.time()
initializeData()

n_percent_values = [0.1,0.2,0.3,0.4,0.5]
n_values = []

for n in n_percent_values:
    n_values.append(initializePlagiarizedData(n))
    checkForPlagiarism("KMP")
    os.remove("./data/PLAGIARIZED.csv")

end_time = time.time()

print("COUNT IS: ", count)

elapsed_time = end_time - start_time

print("Elapsed time: {:.2f} seconds".format(elapsed_time))

    
# Plot the results
plt.plot(n_values, elapsed_times, 'bo-')
plt.xlabel('Input size n')
plt.ylabel('Runtime (seconds)')
plt.title('Runtime of Plagiarism Algorithm')
plt.show()

os.remove("./data/COMBINED.csv")
os.remove("./data/PLAGIARIZED.csv")