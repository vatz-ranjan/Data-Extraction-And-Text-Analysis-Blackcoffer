from string import punctuation
from pandas import DataFrame, read_csv
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag


class TextAnalyser:
    __masterDataset = DataFrame()
    __positiveWords = []
    __negativeWords = []

    def __init__(self):
        self.__curEntryInfo = None
        self.__text = None
        self.__wordTokens = []
        self.__sentTokens = []
        self.__stopWords = []
        self.__wordsWithoutPunctuations = []
        self.__cleanWords = []
        self.__positiveScore = 0
        self.__negativeScore = 0
        self.__polarityScore = 0
        self.__subjectivityScore = 0
        self.__avgSentenceLength = 0
        self.__percentOfComplexWords = 0
        self.__fogIndex = 0
        self.__avgWordsPerSentence = 0
        self.__complexWordCount = 0
        self.__wordCount = 0
        self.__syllablePerWord = 0
        self.__personalPronouns = 0
        self.__avgWordLength = 0
        self.__curDataset = []

    @staticmethod
    def define_master_dictionary(master_dictionary):
        TextAnalyser.__masterDataset = read_csv(master_dictionary, header=0)
        TextAnalyser.__positiveWords = [word for word in TextAnalyser.__masterDataset[TextAnalyser.__masterDataset['Positive'] != 0][
                                            'Word']]
        TextAnalyser.__negativeWords = [word for word in TextAnalyser.__masterDataset[TextAnalyser.__masterDataset['Negative'] != 0][
                                            'Word']]

    def __extract_text(self):
        fileLoc = self.__curEntryInfo['File Loc']
        try:
            file = open(fileLoc, 'r')
            self.__text = file.read()
        except:
            file = open(fileLoc, 'rb')
            self.__text = file.read().decode('utf-8')
        file.close()

    def __cal_tokens(self):
        self.__wordTokens = word_tokenize(self.__text)
        self.__sentTokens = sent_tokenize(self.__text)
        self.__stopWords = set(stopwords.words('english'))
        self.__wordsWithoutPunctuations = [word for word in self.__wordTokens if not (word in punctuation)]
        self.__cleanWords = [word for word in self.__wordsWithoutPunctuations if not (word.lower() in self.__stopWords)]

    def __sentiment_analysis(self):
        positiveScore = 0
        negativeScore = 0

        for word in self.__cleanWords:
            word = word.upper()
            if word in self.__positiveWords:
                positiveScore += 1
        for word in self.__cleanWords:
            word = word.upper()
            if word in self.__negativeWords:
                negativeScore += 1

        self.__positiveScore = positiveScore
        self.__negativeScore = negativeScore
        sumPositiveNegative = self.__positiveScore + self.__negativeScore
        self.__polarityScore = (self.__positiveScore - self.__negativeScore) / (sumPositiveNegative + 0.000001)
        self.__subjectivityScore = sumPositiveNegative / (len(self.__cleanWords) + 0.000001)

    def __analysis_of_readability(self):
        self.__avgSentenceLength = len(self.__wordsWithoutPunctuations) / len(self.__sentTokens)
        self.__percentOfComplexWords = self.__complexWordCount / len(self.__wordsWithoutPunctuations)
        self.__fogIndex = 0.4 * (self.__avgSentenceLength + self.__percentOfComplexWords)

    def __average_words_per_sentence(self):
        self.__avgWordsPerSentence = len(self.__wordsWithoutPunctuations) / len(self.__sentTokens)

    def __complex_word_count(self):
        complex_word = 0
        for word in self.__wordsWithoutPunctuations:
            if self.__count_syllable(word) > 2:
                complex_word += 1

        self.__complexWordCount = complex_word

    def __word_count(self):
        self.__wordCount = len(self.__cleanWords)

    def __syllable_count_per_word(self):
        total_syllable = 0
        for word in self.__wordsWithoutPunctuations:
            total_syllable += self.__count_syllable(word)

        self.__syllablePerWord = total_syllable / len(self.__wordsWithoutPunctuations)

    @staticmethod
    def __count_syllable(word):
        vowels = ['a', 'e', 'i', 'o', 'u']
        cur_syllable = 0
        word = word.lower()
        for char in word:
            if char in vowels:
                cur_syllable += 1

        if word.endswith('ed') or word.endswith('es'):
            cur_syllable -= 1

        cur_syllable = max(0, cur_syllable)
        return cur_syllable

    def __personal_pronouns(self):
        wordsWithTags = pos_tag(self.__wordsWithoutPunctuations)
        personalPronouns = []
        for words in wordsWithTags:
            if words[1] in ['PRP']:
                personalPronouns.append(words[0])
        self.__personalPronouns = len(personalPronouns)

    def __average_word_length(self):
        total = 0
        for word in self.__wordsWithoutPunctuations:
            total += len(word)

        self.__avgWordLength = total / len(self.__wordsWithoutPunctuations)

    def analyze(self, cur_entry_info):
        self.__curEntryInfo = cur_entry_info
        self.__extract_text()
        if len(self.__text) > 1:
            self.__cal_tokens()
            self.__sentiment_analysis()
            self.__syllable_count_per_word()
            self.__complex_word_count()
            self.__analysis_of_readability()
            self.__average_words_per_sentence()
            self.__word_count()
            self.__personal_pronouns()
            self.__average_word_length()

    def get_cur_dataset(self):
        self.__curDataset = [self.__curEntryInfo['URL_ID'],
                             self.__curEntryInfo['URL'],
                             self.__positiveScore,
                             self.__negativeScore,
                             self.__polarityScore,
                             self.__subjectivityScore,
                             self.__avgSentenceLength,
                             self.__percentOfComplexWords,
                             self.__fogIndex,
                             self.__avgWordsPerSentence,
                             self.__complexWordCount,
                             self.__wordCount,
                             self.__syllablePerWord,
                             self.__personalPronouns,
                             self.__avgWordLength
                             ]
        return self.__curDataset
