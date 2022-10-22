import random


class FiveLetterGame:
    def __init__(self, word_base: list) -> None:
        self.word_base = word_base
        self.symbols_for_exclusion = []
        self.included_in_the_word = []
        self.definitely_not_in_this_place = []
        self.exactly_in_this_place = []
    
    @classmethod
    async def create(cls):
        with open("new_file.txt", "r") as read:
            for line in read.readlines():
                latters = line.split()
                self = cls(latters)
            return self
    
    def any_word(self) -> list:
        words_made_unique_letters = []
        for i in self.word_base:
            if len(set(i)) == 5:
                words_made_unique_letters.append(i)
        random.shuffle(words_made_unique_letters)
        return words_made_unique_letters[:10]
    
    def get_restrictions(self, data: dict) -> None:
        symbols_for_exclusion = data['no_letters']
        self.symbols_for_exclusion = []
        if symbols_for_exclusion[0]:
            for i in symbols_for_exclusion[0]:
                self.symbols_for_exclusion.append(i)

        included_in_the_word = data['are_letters']
        self.included_in_the_word = []
        if included_in_the_word[0]:
            for i in included_in_the_word[0]:
                self.included_in_the_word.append(i)

        definitely_not_in_this_place = data['not_in_place']
        self.definitely_not_in_this_place = []
        for i, el in enumerate(definitely_not_in_this_place):
            if el:
                self.definitely_not_in_this_place.append([int(i), el])
        
        exactly_in_this_place = data['in_place']
        self.exactly_in_this_place = []
        for i, el in enumerate(exactly_in_this_place):
            if el:
                self.exactly_in_this_place.append([int(i), el])
    
    def excluded_chars(self, latter) -> bool:
        x = list(map(lambda x: latter.replace(x, ''), self.symbols_for_exclusion))
        x = [True if len(i) == 5 else False for i in x]
        if not False in x:
            return True
        return False
    
    def existing_symbols(self, latter) -> bool:
        for i in self.included_in_the_word:
            if not i in latter:
                return False
        return True
    
    def exclusion_positional_characters(self, latter) -> bool:
        for i in self.definitely_not_in_this_place:
            if latter[i[0]] == i[1]:
                return False
        return True
    
    def specifying_positional_characters(self, latter) -> bool:
        for i in self.exactly_in_this_place:
            if latter[i[0]] != i[1]:
                return False
        return True
    
    def filtering(self) -> list:
        words = []
        for word in self.word_base:
            if self.symbols_for_exclusion:
                if not self.excluded_chars(word):
                    continue
            if self.included_in_the_word:
                if not self.existing_symbols(word):
                    continue
            if self.definitely_not_in_this_place:
                if not self.exclusion_positional_characters(word):
                    continue
            if self.exactly_in_this_place:
                if not self.specifying_positional_characters(word):
                    continue
            words.append(word)
        random.shuffle(words)
        if len(words) > 10:
            return words[:10]
        return words
    
    def run(self, data) -> None:
        self.get_restrictions(data)
        return self.filtering()
