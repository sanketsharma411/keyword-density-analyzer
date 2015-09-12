# word-density-analyzer

## Setup
1. Extract everything to a folder named word-density-analyzer referred to as <root>
2. Install Java
3. In <root>/modules/nlp.py Line 42: Put the path to java executable
4. Navigate to <root> 
5. Install Python 2.xx
6. Install python requirements as 
    ``` 
        pip install -r Requirements.txt
    ```
7. Now try a test script
    ```
        python .\scripts\test.py
    ```
    If it shows Some details about College of computing at GaTech, then the setup has been succesful

8. Now try your own url  with the -url flag
    ```
        python .\scripts\word_density_analyze.py -url "http://www.example.com/"
    ```
    
## Sample Output


```
python .\scripts\word_density_analyze.py -url "https://en.wikipedia.org/wiki/Edward_Snowden"    
```
result (takes a few minutes to run)
```
=============================================================================
The Results
=============================================================================
Edward Snowden
Wikipedia


killswitch
Edward Joseph Snowden
National Security Agency
United States
Russiatwo
Moscow
Hong Kong-based
United States District Court
Glenn Greenwald
Central Intelligence Agency
Barack Obama
Vladimir Putin
The Washington Post
Germany
Edward Snowden Story
Laura Poitras
The New York Times
James Clapper
China
Latin America
Brazilian
U.S. Congress
```

CNN News :
```
python .\scripts\word_density_analyze.py -url "http://www.cnn.com/2013/06/10/politics/edward-snowden-profile/"
```
result (takes less time to load)
```
=============================================================================
The Results
=============================================================================
NSA


Edward Snowden
United States
Hawaii
snowden said
told guardian
snowden
said
government
guardian
worked
politics
behind
leak
say
safeguard
privacy
liberty
cnnpolitics
```



For details on how I built the solution see methodology.md