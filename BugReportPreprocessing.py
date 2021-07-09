import string
import re
import nltk
import inflection
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer


class BugReportPreprocessing:

    def __init__(self, bugReport):
        self.bugReport = bugReport

    # part of speech tagging to identify its category
    def tagPOS(self):

        for report in self.bugReport:
            summaryTokens = nltk.word_tokenize(report["summary"])
            descriptionTokens = nltk.word_tokenize(report["description"])
            filesTokens = nltk.word_tokenize(report["files"])
            posTaggedSummary = nltk.pos_tag(summaryTokens)
            posTaggedDescription = nltk.pos_tag(descriptionTokens)
            posTaggedFiles = nltk.pos_tag(filesTokens)
            report["pos_tagged_summary"] = [token for token, pos in posTaggedSummary if 'NN' in pos or 'VB' in pos]
            report["pos_tagged_description"] = [token for token, pos in posTaggedDescription if 'NN' in pos or 'VB' in pos or 'DT']
            report["pos_tagged_files"] = [token for token, pos in posTaggedFiles if 'NN' in pos or 'VB' in pos]
# print(report.pos_tagged_description);

    # Splitting the bug report into tokens
    def tokenize(self):

        for report in self.bugReport:
            report["summary"] = nltk.wordpunct_tokenize(report["summary"])
            report["description"] = nltk.wordpunct_tokenize(report["description"])
            report["files"] = nltk.wordpunct_tokenize(report["files"])

    # Splitting camelcase to different words
    def splitCamelcase(self, tokens):

        # Copy tokens
        returningTokens = tokens[:]

        for token in tokens:
            splitTokens = re.split(fr'[{string.punctuation}]+', token)

            # If token is split into some other tokens
            if len(splitTokens) > 1:
                # Remove the old Camel case Token to be split
                returningTokens.remove(token)
                for st in splitTokens:
                    # Turning the camelcase into "_" then split them
                    camelCaseSplit = inflection.underscore(st).split('_')

                    if len(camelCaseSplit) > 1:
                        returningTokens.append(st)
                        returningTokens += camelCaseSplit

                    else:
                        returningTokens.append(st)

            else:
                camelCaseSplit = inflection.underscore(token).split('_')
                if len(camelCaseSplit) > 1:
                    returningTokens += camelCaseSplit

        return returningTokens
#print("/n" + returningTokens)

    # Removing punctuations and return the tokens in lower case
    def removePunctuation(self):

        # This var hod all the punctuations and numbers

        punctuationTable = str.maketrans({c: None for c in string.punctuation + string.digits})


        for report in self.bugReport:
            # remove the digits and punctuations using the punctuation table
            summaryNoPunc = [token.translate(punctuationTable) for token in report["summary"]]
            descriptionNoPunc = [token.translate(punctuationTable) for token in report["description"]]
            filesNoPunc = [token.translate(punctuationTable) for token in report["files"]]
            pos_sum_NoPunc = [token.translate(punctuationTable) for token in report["pos_tagged_summary"]]
            pos_desc_NoPunc = [token.translate(punctuationTable) for token in report["pos_tagged_description"]]
            pos_file_NoPunc = [token.translate(punctuationTable) for token in report["pos_tagged_files"]]

            # Transforming the upper case letters to lower case
            report["summary"] = [token.lower() for token in summaryNoPunc if token]
            report["description"] = [token.lower() for token in descriptionNoPunc if token]
            report["files"] = [token.lower() for token in filesNoPunc if token]
            report["pos_tagged_summary"] = [token.lower() for token in pos_sum_NoPunc if token]
            report["pos_tagged_description"] = [token.lower() for token in pos_desc_NoPunc if token]
            report["pos_tagged_files"] = [token.lower() for token in pos_file_NoPunc if token]

    # Removing stop word
    print("before stp")
    def removeStopword(self):

        stopwords = nltk.corpus.stopwords.words('english')
        print(stopwords)

        # Iterating and filtering the stop words from tokens
        for report in self.bugReport:
            report["summary"] = [token for token in report["summary"] if token not in stopwords]
            report["description"] = [token for token in report["description"] if token not in stopwords]
            report["files"] = [token for token in report["files"] if token not in stopwords]
            report["pos_tagged_summary"] = [token for token in report["pos_tagged_summary"] if token not in stopwords]
            report["pos_tagged_description"] = [token for token in report["pos_tagged_description"] if token not in stopwords]
            report["pos_tagged_files"] = [token for token in report["pos_tagged_files"] if token not in stopwords]
    # Removing java Keywords
    print("before jvkeywords")
    def removeJavaKeyword(self):

        # All the java keywords (   Reference Geeks for Geeks)
        java_keywords = {'abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch', 'char', 'class', 'const',
                         'continue', 'default', 'do', 'double', 'else', 'enum', 'extends', 'final', 'finally',
                         'float', 'for', 'goto', 'if', 'implements', 'import', 'instanceof', 'int', 'interface', 'long',
                         'native', 'new', 'package', 'private', 'protected', 'public', 'return', 'short',
                         'static', 'strictfp', 'super', 'switch', 'synchronized', 'this', 'throw', 'throws',
                         'transient', 'try', 'void', 'volatile', 'while'}

        for report in self.bugReport:
            report["summary"] = [token for token in report["summary"] if token not in java_keywords]
            report["description"] = [token for token in report["description"] if token not in java_keywords]
            report["files"] = [token for token in report["files"] if token not in java_keywords]
            report["pos_tagged_summary"] = [token for token in report["pos_tagged_summary"] if token not in java_keywords]
            report["pos_tagged_description"] = [token for token in report["pos_tagged_description"] if
                                             token not in java_keywords]
            report["pos_tagged_files"] = [token for token in report["pos_tagged_files"] if token not in java_keywords]

    # stem the tokens ( return the words to its origin )
    print("before stemming")
    def stem(self):

        # Stemmer instance (snow ball)
        sbs = PorterStemmer()
        lemmatizer = WordNetLemmatizer()
        for report in self.bugReport:
            report["summary"] = dict(zip(['stemmed', 'unstemmed', 'lemma'],
                                      [[sbs.stem(token) for token in report["summary"]], report["summary"],
                                       [lemmatizer.lemmatize(token) for token in report["summary"]]]))
            report["description"] = dict(zip(['stemmed', 'unstemmed', 'lemma'],
                                          [[sbs.stem(token) for token in report["description"]], report["description"],
                                           [lemmatizer.lemmatize(token) for token in report["description"]]]))
            report["files"] = dict(zip(['stemmed', 'unstemmed', 'lemma'],
                                          [[sbs.stem(token) for token in report["files"]], report["files"],
                                           [lemmatizer.lemmatize(token) for token in report["files"]]]))
            report["pos_tagged_summary"] = dict(zip(['stemmed', 'unstemmed', 'lemma'],
                                                 [[sbs.stem(token) for token in report["pos_tagged_summary"]],
                                                  report["pos_tagged_summary"], [lemmatizer.lemmatize(token) for token in
                                                                              report["pos_tagged_summary"]]]))
            report["pos_tagged_description"] = dict(zip(['stemmed', 'unstemmed', 'lemma'],
                                                     [[sbs.stem(token) for token in report["pos_tagged_description"]],
                                                      report["pos_tagged_description"],
                                                      [lemmatizer.lemmatize(token) for token in
                                                       report["pos_tagged_description"]]]))
            report["pos_tagged_files"] = dict(zip(['stemmed', 'unstemmed', 'lemma'],
                                                 [[sbs.stem(token) for token in report["pos_tagged_files"]],
                                                  report["pos_tagged_files"], [lemmatizer.lemmatize(token) for token in
                                                                            report["pos_tagged_files"]]]))

    def preprocess(self):

        self.tagPOS()
        self.tokenize()
        # Running camelcase function for all report sections needed
        for report in self.bugReport:
            report["summary"] = self.splitCamelcase(report["summary"])
            report["description"] = self.splitCamelcase(report["description"])
            report["files"] = self.splitCamelcase(report["files"])
            report["pos_tagged_summary"] = self.splitCamelcase(report["pos_tagged_summary"])
            report["pos_tagged_description"] = self.splitCamelcase(report["pos_tagged_description"])
            report["pos_tagged_files"] = self.splitCamelcase(report["pos_tagged_files"])
        self.removePunctuation()
        self.removeStopword()
        self.removeJavaKeyword()
        self.stem()


def startpreprocess(dataset):

    print("Bug report preprocessing started")
    preprocessedReports = BugReportPreprocessing(dataset)
    preprocessedReports.preprocess()

    return preprocessedReports.bugReport

    print("Bug report preprocessed successfully")
