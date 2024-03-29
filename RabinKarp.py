# COSC 320 - Term Project
# Group Members Chad Lantz (77879460), Prashant Dutt (63565634), Lance Rogan (62708938)
# Note: We have also added our own code / print statements to adjust the provided code taken from GeeksForGeeks to our usage.

# **** PLEASE READ ****
# Python3 program for Rabin Karp Algorithm
# Following program is the python implementation of
# Rabin Karp Algorithm given in CLRS book
# This code is contributed by Bhavya Jain
#https://www.geeksforgeeks.org/rabin-karp-algorithm-for-pattern-searching/
# This code is contributed by Bhavya Jain

class RabinKarp:
    count = 0
    def __init__(self):
        pass
    
    def RabinKarpAlgo(self, pattern, text, primeNum):
        numOfInputChars = 256
        M = len(pattern)
        N = len(text)
        patternHashValue = 0    
        textHashValue = 0   
        h = 1
        j = 0
        i = 0

        if M > N:
            patternSubstring = pattern[0:N]
            pattern = patternSubstring
            M = N

    
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
                    print("--------------------------------------\n")
                    self.count += 1
                    print("Rabin-Karp Detection #", self.count)
                    print("Original Text: " + text + "\n")
                    print("Plagiarized Text: " + pattern + "\n")
                    print("--------------------------------------")
            if i < N-M:
                textHashValue = (numOfInputChars*(textHashValue-ord(text[i])*h) + ord(text[i+M])) % primeNum
                if textHashValue < 0:
                    textHashValue = textHashValue + primeNum
