# COSC-320 - getPlagiarized-Project
## By Lance Rogan, Prashant Dutt, and Chad Lantz

## Code Overview and Description
This project focuses on the implementation and comparison of three string matching algorithms: Knuth-Morris-Pratt (KMP), Longest Common Substring (LCSS), and Rabin-Karp. These algorithms are used within a plagiarism detector to identify similarities between text documents. The performance comparison is based on the runtime of each algorithm as the input size increases.

## Sample Outputs
Please refer to the output plots that show the runtime of each algorithm (KMP, LCSS, and Rabin-Karp) as the input size grows. Additionally, there is a combined plot displaying the runtime of all three algorithms together for comparison.

## Program Pre-requisites
1. Python 3.x
2. pandas
3. matplotlib.pyplot
4. os
5. time
6. threading

## Build and Execution Instructions
1. Ensure you have Python 3.x installed and the required libraries (pandas, matplotlib.pyplot, os, time, and threading).
2. Place the KMP.py, LCSS.py, RabinKarp.py, and PlagiarismDetector.py files in the same directory.
3. Create a /data folder in the same directory containing the text dataset to be analyzed.
4. Run the PlagiarismDetector.py file to execute the plagiarism detector.
5. The results will be displayed as plots and printed in the console.

![KMP_Detection_Output](https://user-images.githubusercontent.com/113868682/231638970-61eb7f84-418d-48ed-a823-797fbb2e3fed.png)

## Code Overview

![COMBINEDPLOTSECONDS](https://user-images.githubusercontent.com/113868682/231639275-070b55f3-d94e-4863-978a-c07dd71372aa.png)

### KMP.py
This module implements the Knuth-Morris-Pratt algorithm, which is used to search for a pattern in a given text in linear time. The main search function is KMPSearch, which uses the computeLPSArray function to preprocess the pattern and create an LPS (Longest Proper Prefix which is also a suffix) array to optimize the search.

![KMPPLOTSECONDS](https://user-images.githubusercontent.com/113868682/231639209-17b27414-8e80-475f-b50d-0183ff14b68f.png)

### LCSS.py
This module implements the Longest Common Subsequence problem using dynamic programming. The main function is lcs, which takes two strings as input and calculates the longest common subsequence between them. A 2D array L is used to store the lengths of the longest common subsequences for different substrings of the input strings.

![LCSSPLOTSECONDS](https://user-images.githubusercontent.com/113868682/231639161-04fbea03-f05f-47a3-a927-4e341a714a4e.png)

### RabinKarp.py
This module implements the Rabin-Karp algorithm, which is another pattern searching algorithm. The main function is RabinKarpAlgo, which takes the pattern, text, and a prime number as input. It calculates hash values for the pattern and substrings of the text and compares them to find matches. The rolling hash technique is used to efficiently compute the hash values for the text substrings.

![RABINKARPPLOTSECONDS](https://user-images.githubusercontent.com/113868682/231639120-5a930593-044c-48bc-bab0-279e13fbebc8.png)

### PlagiarismDetector.py
This script contains the main implementation of the plagiarism detector, which uses the three different string-matching algorithms: KMP, LCSS, and Rabin-Karp. It compares a sample of text documents against a larger dataset to identify potential plagiarism. The script initializes the plagiarism detector, runs it for different sample sizes, and generates plots to visualize the results.

### /data and /testData
The /data folder contains the text dataset to be analyzed by the plagiarism detector. The /testData folder may be used to store test cases or smaller samples of data for testing purposes.

## Conclusion
The project successfully implemented and compared the performance of three string matching algorithms - Knuth-Morris-Pratt (KMP), Longest Common Substring (LCSS), and Rabin-Karp - in a plagiarism detector. The choice of algorithm depends on the specific use case and the dataset being analyzed. Further optimization and analysis can be conducted to improve the performance and accuracy of the plagiarism detector.

## References
https://www.geeksforgeeks.org/rabin-karp-algorithm-for-pattern-searching/


https://www.geeksforgeeks.org/longest-common-subsequence-dp-4/

https://www.geeksforgeeks.org/kmp-algorithm-for-pattern-searching/