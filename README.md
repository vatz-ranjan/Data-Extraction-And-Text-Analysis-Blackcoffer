# Data-Extraction-And-Text-Analysis-Blackcofferr

This task contains 3 python files
1. main.py - Contains the main function
2. web_scraper.py - Contains the WebScrapper class which will extract the textual data for the given url and save it into text file.
3. text_analyzer.py - Contains the TextAnalyser class which will read the textual data and performing text analysis on it.

Output:
1. "Text File" Folder - This folder will be created which will contain all the text file
2. "Output Data Structure.xlsx" - This Excel file will be generated having all the required text analysis

Some important python packages need to be installed before running the main file
1. pip install pandas
2. pip install nltk (Also download stopwords using nltk.download(["names", "stopwords"]) or uncommenting 2nd line of main function in main.py file)
3. pip install requests
4. pip install beautifulsoup4
5. pip install xlsxwriter
6. pip install openpyxl


Some additional stuff need to be installed
1. MasterDictionary (Loughran-McDonald_MasterDictionary_1993-2021.csv) - https://sraf.nd.edu/loughranmcdonald-master-dictionary/
Update the file location for these in the task function in the main.py file
