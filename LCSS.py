# COSC 320 - Term Project
# Group Members Chad Lantz (77879460), Prashant Dutt (63565634), Lance Rogan (62708938)
# Note: We have also added our own code / print statements to adjust the provided code taken from GeeksForGeeks to our usage.

# **** PLEASE READ ****
# Python3 program for LCSS Algorithm
# Dynamic Programming implementation of LCS problem
# https://www.geeksforgeeks.org/longest-common-subsequence-dp-4/
# This code is contributed by Nikhil Kumar Singh(nickzuck_007)

#Creating a class for LCSS to run algorithm
class LCSS:
    count = 0
    def __init__(self):
        pass
 
    def lcs(self, X , Y):  
        m = len(X)
        n = len(Y)   
    
        # Declaring the array for storing the dp values
        L = [[None]*(n+1) for i in range(m+1)]
    
        # Following steps build L[m+1][n+1] in bottom up fashion
        # Note: L[i][j] contains length of LCS of X[0..i-1]
        # and Y[0..j-1]
        for i in range(m+1):
            for j in range(n+1):
                if i == 0 or j == 0 :
                    L[i][j] = 0
                elif X[i-1] == Y[j-1]:
                    L[i][j] = L[i-1][j-1]+1
                else:
                    L[i][j] = max(L[i-1][j] , L[i][j-1])
    
        # L[m][n] contains the length of LCS of X[0..n-1] & Y[0..m-1]
        if L[m][n] == 0:
            print("LCSS Detection: There were no similarities. I.e, there was no common subsequence.")
        elif L[m][n] == m and L[m][n] == n:
            pass
            print("--------------------------------------\n")
            self.count += 1
            print("LCSS Detection #", self.count)
            print("Longest Common Subsequence: " + str(L[m][n]))
            print("Original Text: " + X + "\n")
            print("Plagiarized Text: " + Y + "\n")
            print("--------------------------------------")
    
