# **** PLEASE READ ****
# Python3 program for KMP Algorithm
# This code is contributed by Bhavya Jain
# https://www.geeksforgeeks.org/kmp-algorithm-for-pattern-searching/
# (We have added additional comments in this code to help explain each step).

class KMP:

    #Global Variable
    count =0
    
    def __init__(self):
        pass

    #KMP Search Function
    def KMPSearch(self, pat, txt):

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
        self.computeLPSArray(pat, M, lps)
    
        i = 0  # index for txt[]

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
                print("--------------------------------------\n")
                self.count += 1
                print("KMP Detection #", self.count)
                print("Original Text: " + txt + "\n")
                print("Plagiarized Text: " + pat + "\n")
                print("--------------------------------------")

                j = lps[j-1]
    
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
    


    #Function to initialize LPS array
    def computeLPSArray(self, pat, M, lps):

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