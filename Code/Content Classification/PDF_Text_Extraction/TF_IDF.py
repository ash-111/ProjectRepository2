import pdfplumber
import re
import os
import numpy as np
import json
import sys


def GetAllPDFsPaths(docsPath):
    documentPathsList = np.array([])
    y_label = np.array([])

    for root, dirs, files in os.walk(docsPath):
        for file in files:
            #append the file name to the list
            if(file.endswith(".pdf")):
                documentPathsList = np.append(documentPathsList, os.path.join(root,file))

                # Converts folder name: "\6) Doctor Referal Letters" to -> "6" to extract y_label.
                # https://note.nkmk.me/en/python-os-basename-dirname-split-splitext/#:~:text=dirname()-,Use%20os.,name)%20from%20a%20path%20string.&text=If%20you%20want%20to%20get,above%20the%20file%2C%20use%20os.
                folderName = os.path.basename(os.path.dirname(os.path.join(root,file)))
                y_label = np.append(y_label, int(folderName[0]))

    return documentPathsList, y_label.astype(np.int)


def Get_Text_from_PDF(pathname):
    pdf = pdfplumber.open(pathname)

    # creating a pdf reader object
    pdf = pdfplumber.open(pathname)

    # Getting First page of pdf
    page = pdf.pages[0]

    text = page.extract_text()
    pdf.close()

    text = re.sub(r'[/]', ' ', text) # Replace all '/' with spaces 
    text = re.sub(r'[^\w\s]', '', text) # Removes all other punctuation
    text = re.sub(r"[_]+", '', text) # Removes underscores
    text = re.sub(r"[0-9]", '', text) # Removes numbers

    text = text.lower()
    textlist = text.split()

    return(textlist)

class TF_IDF:
    #Constructor
    def __init__(self, trainDocsPath, languageDictionaryPath):
        
        """ 
        Constructor simply obtains all the training documents' file paths 
        and puts them in self.documentPathsList and also generates the corresponding y_label array by checking 
        the folderName that the document is stored in e.g.

        y_labels also generated within constructor

        Converts folder name: "\6) Doctor Referal Letters" to -> "6" to extract y_label.
        
        """

        with open(languageDictionaryPath) as json_file:
            dictionary = json.load(json_file)

        self.dictionarySet = set(dictionary.keys())
        self.documentPathsList, self.y_labels_train = GetAllPDFsPaths(trainDocsPath)
        self.numOfDocuments = len(self.documentPathsList)

        np.set_printoptions(threshold=sys.maxsize)

    

    def CalculateVocabList(self):
        vocabSet = set()
        for i in range(0, self.numOfDocuments):
            
            pathname = self.documentPathsList[i]
            print(i, pathname)
            textlist = Get_Text_from_PDF(pathname)

            # Add new words ot vocabulary set:
            textSet = set(textlist)
            vocabSet = vocabSet | textSet

        print(vocabSet)
        print(len(vocabSet))

        # Remove Non-Existent words or spelling errors:
        vocabSet = vocabSet & self.dictionarySet

        self.vocabList = list(vocabSet)
        print(self.vocabList)
        print(len(self.vocabList))



    def CalculateTermFreqTable(self):
        self.termFreqTable = np.zeros((self.numOfDocuments, (len(self.vocabList))))

        print(self.termFreqTable.shape)

        for i in range(0,self.numOfDocuments):
            pathname = self.documentPathsList[i]
            print(i, pathname)
            textlist = Get_Text_from_PDF(pathname)      
            
            for j in range(0,len(self.vocabList)):
                word = self.vocabList[j]
                if word in textlist:
                    self.termFreqTable[i][j] = textlist.count(word)    

            # for j in range(0,len(textlist)):
            #     word = textlist[j]
            #     termFreqTable[i][vocabList.index(word)] = textlist.count(word)        
                    
    def Calculate_TF_IDF_Train(self):
        totalNumOfDocuments = self.numOfDocuments
        termFreqTableBool = self.termFreqTable > 0
        # self.IDF = np.log2(totalNumOfDocuments/np.sum(termFreqTableBool, axis=0))
        self.IDF = (totalNumOfDocuments/np.sum(termFreqTableBool, axis=0))

        print("np.sum(termFreqTableBool, axis=0)", np.sum(termFreqTableBool, axis=0))
        # print("self.IDF", self.IDF)

        IDF = np.tile(self.IDF, (totalNumOfDocuments, 1))
        TotalNumofTokensInArticles = np.sum(self.termFreqTable, axis=1)

        for i in range(0, len(TotalNumofTokensInArticles)):
            if TotalNumofTokensInArticles[i] == 0:
                print("Warning Doc:", i, "has 0 text")

        TotalNumofTokensInArticles = np.tile(np.array([TotalNumofTokensInArticles]).transpose(), (1, len(self.vocabList)))

        self.TF_IDF_Train = (self.termFreqTable/TotalNumofTokensInArticles)#*IDF

    def Get_TF_IDF_Train(self):
        return self.TF_IDF_Train
    

    def Get_TF_IDF_Text(self, textlist):
        termFreqTable = np.zeros((1, (len(self.vocabList))))

        # print("termFreqTable.shape =", termFreqTable.shape)

        for j in range(0,len(self.vocabList)):
            word = self.vocabList[j]
            if word in textlist:
                termFreqTable[0][j] = textlist.count(word) 

        # print("termFreqTable", termFreqTable)

        TotalNumofTokensInArticle = np.sum(termFreqTable, axis=1)

        # print("TotalNumofTokensInArticle", TotalNumofTokensInArticle)

        TF = termFreqTable/TotalNumofTokensInArticle

        TF_IDF_Test = TF*self.IDF

        # print("TF", TF)
        # print("TF_IDF_Test", TF_IDF_Test)

        return TF_IDF_Test



    def Get_TF_IDF_Single_PDF(self, testFilePath):
        textlist = Get_Text_from_PDF(testFilePath) 
        TF_IDF_Test = self.Get_TF_IDF_Text(textlist)
        return  TF_IDF_Test
        
    

    def Get_Test_TF_IDF_Multiple_PDFs(self, testPath):

        testDocumentPathsList, test_y_label = GetAllPDFsPaths(testPath)

        TF_IDF_Test_List = np.array([]).reshape(0,len(self.vocabList))

        for i in range(len(testDocumentPathsList)):
            linkName = testDocumentPathsList[i]#.replace(" ", "\s")
            print(f"{i}")
            print(linkName)
            TF_IDF_Test_List = np.vstack([TF_IDF_Test_List, self.Get_TF_IDF_Single_PDF(testDocumentPathsList[i])])

        return TF_IDF_Test_List, test_y_label

        
    def Get_TF_IDF_Categories_3D_Table(self):
        numOfCategories = self.Get_y_labels_train
        self.y_label


    # Getters
    
    def Get_y_labels_train(self):
        return self.y_labels_train
    
    def GetVocabList(self):
        return self.vocabList
    
    def PrintDocumentPathsList(self):
        #print all the file names
        for pathname in self.documentPathsList:
            print(pathname)