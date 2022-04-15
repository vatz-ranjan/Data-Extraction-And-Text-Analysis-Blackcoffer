from warnings import filterwarnings
from os import makedirs, path
# import nltk
from pandas import read_excel, DataFrame, ExcelWriter
from web_scraper import WebScrapper
from text_analyser import TextAnalyser


def task():
    inputDataset = read_excel('Input.xlsx')
    totalDataset = []
    folderName = "Text File"
    makedirs(folderName, exist_ok=True)
    master_dictionary = 'Loughran-McDonald_MasterDictionary_1993-2021.csv'
    chrome_driver_path = 'E:/Application/ChromeDriver/chromedriver.exe'
    TextAnalyser.define_master_dictionary(master_dictionary)
    for index in range(inputDataset.shape[0]):
        fileName = str(inputDataset.loc[index, 'URL_ID']) + '.txt'
        fileLoc = path.join(folderName, fileName)
        curEntryInfo = {'URL_ID': inputDataset.loc[index, 'URL_ID'], 'URL': inputDataset.loc[index, 'URL'], 'File Loc': fileLoc}
        web_scrape = WebScrapper()
        web_scrape.scrape(cur_entry_info=curEntryInfo, chrome_driver_path=chrome_driver_path)

        text_analysis = TextAnalyser()
        text_analysis.analyze(cur_entry_info=curEntryInfo)
        curDataset = text_analysis.get_cur_dataset()
        totalDataset.append(curDataset)

    outputDataset = DataFrame(totalDataset, columns=['URL_ID', 'URL', 'POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE', 'SUBJECTIVITY SCORE', 'AVG SENTENCE LENGTH', 'PERCENTAGE OF COMPLEX WORDS', 'FOG INDEX', 'AVG NUMBER OF WORDS PER SENTENCE', 'COMPLEX WORD COUNT', 'WORD COUNT', 'SYLLABLE PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH'])
    writer = ExcelWriter('Output Data Structure.xlsx', engine='xlsxwriter')
    outputDataset.to_excel(writer, sheet_name='Sheet1', index=False, na_rep='NaN', float_format="%.2f")

    for column in outputDataset:
        column_width = int(max(outputDataset[column].astype(str).map(len).max(), len(column)))
        col_idx = outputDataset.columns.get_loc(column)
        writer.sheets['Sheet1'].set_column(col_idx, col_idx, column_width)

    writer.save()


if __name__ == '__main__':
    filterwarnings('ignore')
    # nltk.download(["names", "stopwords"])
    task()

'''
End
'''