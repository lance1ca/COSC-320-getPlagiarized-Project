import pandas as pd
import os
import unicodedata
import emoji
import time
import traceback
import matplotlib.pyplot as plt
import numpy as np


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
    plagiarizedDF = combinedDF.sample(n=percentOfSize).sort_index()
    plagiarizedDF.to_csv('./data/PLAGIARIZED.csv', index=False)

    return percentage * len(combinedDF)
        



def checkForPlagiarism(version):
    combinedDF = pd.read_csv("./data/COMBINED.csv",encoding='utf-8')
    plagiarizedDF = pd.read_csv("./data/PLAGIARIZED.csv",encoding='utf-8')
    

    global errcount 
    global start_plot_time
    start_plot_time = time.perf_counter()
    
    if version == "rknum":
        cnump = combinedDF.to_numpy()
        pnump = plagiarizedDF.to_numpy()
        # combinedDF = dict(zip(combinedDF.columns, list(range(0,len(combinedDF.columns)))))
        # plagiarizedDF = dict(zip(plagiarizedDF.columns, list(range(0,len(plagiarizedDF.columns)))))
                       
        for crow in cnump:
            for prow in pnump:
                    try:
                        matched = karpAlgo(prow[2],crow[2],13)
                        if(matched):
                            print("og text: "+crow[2])
                            print("stolen text; "+prow[2])
                            print(matched)
                            
                    except Exception as e:
                        # print(e)
                        errcount += 1
    if version == "KMP":
        cnump = combinedDF.to_numpy()
        pnump = plagiarizedDF.to_numpy()
        # combinedDF = dict(zip(combinedDF.columns, list(range(0,len(combinedDF.columns)))))
        # plagiarizedDF = dict(zip(plagiarizedDF.columns, list(range(0,len(plagiarizedDF.columns)))))
                       
        for crow in cnump:
            for prow in pnump:
                    try:
                        # matched = 
                        KMPSearch(prow[2],crow[2])
                        # if(matched):
                        #     print("og text: "+crow[2])
                        #     print("stolen text; "+prow[2])
                        #     print(matched)
                            
                    except Exception as e:
                        # print(e)
                        errcount += 1
                       
    if(version == "rkpan"):
        combinedDF = combinedDF.to_dict('records')
        plagiarizedDF = plagiarizedDF.to_dict('records')
        for plagiarizedRow in plagiarizedDF:
            for originalRow in combinedDF:
                    
                    try:
                        matched = RabinKarpAlgo(plagiarizedRow['content'],originalRow['content'],101)

                        if(matched):
                            print("Original text from \"{}\", \ntext = \"{}: \"".format(originalRow['userName'],originalRow['content']))
                            print("Plagiarized text from \"{}\", \ntext = \"{}: \"".format(plagiarizedRow['userName'],plagiarizedRow['content']))
                            print("\n")
                            
                    except Exception as e:
                        # print(e)
                        errcount += 1
                       
                        
    # if(version == "KMP"):
        
    #     for plagiarizedRow in plagiarizedDF:
    #         for originalRow in combinedDF:
                    
    #                 try:
    #                     # currOriginalUserName = originalRow['userName']
    #                     # currOriginalRequestId = originalRow['reviewId']
    #                     # currOriginalContent = originalRow['content']

    #                     # currPlagiarizedRowUserName = plagiarizedRow['userName']
    #                     # currPlagiarizedRequestId = plagiarizedRow['reviewId']
    #                     # currPlagiarizedContent = plagiarizedRow['content']
                        
    #                     matched = KMPSearch(plagiarizedRow['content'],originalRow['content'])

    #                     if(matched):
    #                         print("Original text from \"{}\", \nwith requestId = \"{}\", \ntext = \"{}: \"".format(originalRow['userName'],originalRow['reviewId'],originalRow['content']))
    #                         print("Plagiarized text from \"{}\", \nwith requestId = \"{}\", \ntext = \"{}: \"".format(plagiarizedRow['userName'],plagiarizedRow['reviewId'],plagiarizedRow['content']))
    #                         print("\n")

    #                 except Exception as e:
    #                     print("An Error Occurred :(")
    #                     print(e)
    #                     #traceback.print_exc()
                        
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

#rabin karp algorthirm
def RabinKarpAlgo(pattern, text, primeNum):
    numOfInputChars = 256
    M = len(pattern)
    N = len(text)
    patternHashValue = 0    
    textHashValue = 0   
    h = 1
    j = 0
    i = 0
 
    for i in range(M-1):
        h = (h*numOfInputChars) % primeNum
 
    for i in range(M):
        patternHashValue = (numOfInputChars*patternHashValue + ord(pattern[i])) % primeNum
        textHashValue = (numOfInputChars*textHashValue + ord(text[i])) % primeNum
 
    for i in range(N-M+1):
        if patternHashValue == textHashValue:
            for j in range(M):
                if text[i+j] != pattern[j]:
                    break
                else:
                    j += 1
            if j == M:
                print("A Pattern has been found at index " + str(i))
                global count 
                count += 1
                print("DETECTION #", count)
                return True
        if i < N-M:
            textHashValue = (numOfInputChars*(textHashValue-ord(text[i])*h) + ord(text[i+M])) % primeNum
            if textHashValue < 0:
                textHashValue = textHashValue + primeNum



d = 10
def karpAlgo(pattern, text, q):
    m = len(pattern)
    n = len(text)
    p = 0
    t = 0
    h = 1
    i = 0
    j = 0

    for i in range(m-1):
        h = (h*d) % q

    # Calculate hash value for pattern and text
    for i in range(m):
        p = (d*p + ord(pattern[i])) % q
        t = (d*t + ord(text[i])) % q

    # Find the match
    for i in range(n-m+1):
        if p == t:
            for j in range(m):
                if text[i+j] != pattern[j]:
                    break

            j += 1
            if j == m:
                print("Pattern is found at position: " + str(i+1))
                global count 
                count += 1
                print("DETECTION #", count)
                return True

        if i < n-m:
            t = (d*(t-ord(text[i])*h) + ord(text[i+m])) % q

            if t < 0:
                t = t+q





if os.path.exists("./data/COMBINED.csv"):
    os.remove("./data/COMBINED.csv")

if os.path.exists("./data/PLAGIARIZED.csv"):
    os.remove("./data/PLAGIARIZED.csv")

start_time = time.time()
initializeData()

n_percent_values = [0.1,0.2,0.3,0.4,0.5]
n_values = []
# version = "rknum"                                                 #change  ***IMPORTANT***
# version = "rkpan"                                                 #change  ***IMPORTANT***
version = "KMP"                                                 #change  ***IMPORTANT***
errcount = 0
for n in n_percent_values:
    n_values.append(initializePlagiarizedData(n))
    checkForPlagiarism(version)                                          
    os.remove("./data/PLAGIARIZED.csv")

end_time = time.time()

print("COUNT IS: ", count)

elapsed_time = end_time - start_time
if version == "rk":
    print("the error count is " + str(errcount))

print("Elapsed time: {:.2f} seconds".format(elapsed_time))
print("avg time per detection is "+ str(elapsed_time/count) + " seconds")
    
# Plot the results
plt.plot(n_values, elapsed_times, 'bo-')
plt.xlabel('Input size n')
plt.ylabel('Runtime (seconds)')
plt.title('Runtime of '+version+' Plagiarism Algorithm')
plt.show()

os.remove("./data/COMBINED.csv")
os.remove("./data/PLAGIARIZED.csv")