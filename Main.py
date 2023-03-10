import pandas as pd
import os
import unicodedata
import emoji
import time
import traceback
import matplotlib.pyplot as plt


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
                        
                        matched = KMPSearch(plagiarizedRow['content'],originalRow['content'])

                        if(matched):
                            print("Original text from \"{}\", \nwith requestId = \"{}\", \ntext = \"{}: \"".format(currOriginalUserName,currOriginalRequestId,currOriginalContent))
                            print("Plagiarized text from \"{}\", \nwith requestId = \"{}\", \ntext = \"{}: \"".format(currPlagiarizedRowUserName,currPlagiarizedRequestId,currPlagiarizedContent))
                            print("\n")

                    except Exception as e:
                        print("An Error Occurred :(")
                        #traceback.print_exc()
                        
        global end_plot_time
        end_plot_time = time.perf_counter()
        global elapsed_times
        elapsed_time = end_plot_time - start_plot_time
        elapsed_times.append(elapsed_time)



count =0
# **** PLEASE READ ****
# Python3 program for KMP Algorithm
# This code is contributed by Bhavya Jain
# https://www.geeksforgeeks.org/kmp-algorithm-for-pattern-searching/
# (We have added additional comments in this code to help explain each step).


#KMP Search Function
def KMPSearch(pat, txt):

    #Initialize M as the length of the pattern we want to check for
    M = len(pat)

    #Initialize N as the length of the text we have taken in that we want to analyze to see if the pattern exists in it
    N = len(txt)
 
    # create lps[] that will hold the longest prefix suffix
    # values for pattern

    #We create an lps variable which is an array of integers that holds the values for the LONGEST proper prefix which is also a suffix
    #for the pattern. The length of this array is of size M (length of pattern), and initialized to all zeros.
    lps = [0]*M

    #Initialize the index for pattern as j = ZERO
    j = 0  # index for pat[]
 
    # Preprocess the pattern (calculate lps[] array)
    #This is our function to INITIALIZE the LPS array
    computeLPSArray(pat, M, lps)
 
    i = 0  # index for txt[]

    isMatched = False

    #While the length of the text being scanned minus i is greater than or equal to the length of the pattern minus j
    #Do this.
    while (N - i) >= (M - j):

        #If the pattern at index j and i match, simply increment both i and j by 1 and check if the next characters match
        if pat[j] == txt[i]:
            i += 1
            j += 1
 
        #If j has reached the size of M (i.e, j has continually been incremented such that it has reached the entire pattern)
        #Then we print out the pattern found at index (i-j), and set j to be lps[j-1]
        if j == M:
            #print("Found pattern at index " + str(i-j))
            #ADD PRINT STATEMENTS AND COUNT
            global count 
            count += 1
            print("DETECTION #", count)
            j = lps[j-1]
            isMatched = True
 
        # mismatch after j matches
        #OTHERWISE, if i is LESS than the size of the text being scanned (not done yet) AND the pattern at index j and text at index i DO NOT match
        #Then we do this
        elif i < N and pat[j] != txt[i]:
            # Do not match lps[0..lps[j-1]] characters,
            # they will match anyway

            #If j!=0, then set j to be lps[j-1] to skip to that spot
            if j != 0:
                j = lps[j-1]
            #Otherwise, increment i and repeat
            else:
                i += 1
    
    return isMatched
 


#Function to initialize LPS array
def computeLPSArray(pat, M, lps):

    #Set length to be zero
    len = 0  # length of the previous longest prefix suffix
 
    #Set lps at index 0 to be zero (this will always be case I believe)
    lps[0] = 0 # lps[0] is always 0

    #Set i = 1 to start
    i = 1
 
    # the loop calculates lps[i] for i = 1 to M-1 (length of pattern -1)
    #While i is less than M, do this
    while i < M:

        #If the pattern at index i EQUALS the pattern at length (i-1 in most cases), then 
            #LPS [i] = len, where length has been incremented by one. So LPS[i] = len +1
            #Then we increment i to move to the next character in pattern 
        if pat[i] == pat[len]:
            len += 1
            lps[i] = len
            i += 1
        #IF NO MATCH
            #We check if length is NOT zero. If it is not zero, we continually iterate on the same i (character) with len = lps[len-1], and recheck until len=0
        else:
            # This is tricky. Consider the example.
            # AAACAAAA and i = 7. The idea is similar
            # to search step.
            if len != 0:
                len = lps[len-1]
 
                # Also, note that we do not increment i here
            #If len is zero, then we simply set lps[i] = 0. and increment i and start again
            else:
                lps[i] = 0
                i += 1

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