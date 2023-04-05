 
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
        if i < N-M:
            textHashValue = (numOfInputChars*(textHashValue-ord(text[i])*h) + ord(text[i+M])) % primeNum
            if textHashValue < 0:
                textHashValue = textHashValue + primeNum