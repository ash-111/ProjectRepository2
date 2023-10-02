import json

class SpellChecker(object):
    def __init__(self, lowercaseLetters, dictionary):
        # Opening JSON file
        self.dictionary = dictionary
        self.lowercaseLetters = lowercaseLetters

        totalWordCount = float(sum(self.dictionary.values()))
        self.wordProbabs = {word:self.dictionary[word]/totalWordCount for word in self.dictionary}

    def split(self, word):
        return[(word[:i], word[i:]) for i in range(len(word)+1)]   

    def delete(self, word):
        return([l + r[1:] for l,r in self.split(word) if r])   
    
    def swap(self, word):
        return [l+r[1]+r[0]+r[2:] for l,r in self.split(word) if len(r)>=2] 

    def replace(self, word):
        return [l + c + r[1:] for l,r in self.split(word) if r for c in self.lowercaseLetters]  

    def insert(self, word):
        return [l + c + r for l,r in self.split(word) for c in self.lowercaseLetters] 

    def levelOneEdits(self, word):
        return set(self.delete(word) + self.swap(word) + self.replace(word) + self.insert(word))
 
    def levelTwoEdits(self, word):
        return set(e2 for e1 in self.levelOneEdits(word) for e2 in self.levelOneEdits(e1))

    def levelThreeEdits(self, word):
        return set(e3 for e1 in self.levelOneEdits(word) for e2 in self.levelOneEdits(e1) for e3 in self.levelOneEdits(e2))

    def levelFourEdits(self, word):
        return set(e4 for e1 in self.levelOneEdits(word) for e2 in self.levelOneEdits(e1) for e3 in self.levelOneEdits(e2) for e4 in self.levelOneEdits(e3))

    def validWords(self, words):
        return set(w for w in words if w in self.dictionary)


    def correctSpelling(self, word):
        validSuggestions = self.validWords([word]) or self.validWords(self.levelOneEdits(word)) or self.validWords(self.levelTwoEdits(word))# or self.validWords(self.levelThreeEdits(word)) )
        # print(len(self.levelOneEdits(word)), len(self.levelTwoEdits(word)))
        if len(validSuggestions) == 0:
            return word
        else:
            validSuggestionsDict = {w:self.wordProbabs[w] for w in validSuggestions}
            # print(validSuggestions)
            return max(validSuggestionsDict, key = validSuggestionsDict.get)


