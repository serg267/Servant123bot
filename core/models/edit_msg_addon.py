

class TextAddon:
    texts = ['Попробуй еще', 'Еще раз', 'Ну еще разок', 'Может быть в этот раз']

    def __init__(self):
        self.__next = 0

    def __str__(self):
        text = self.texts[self.__next]
        if self.__next + 1 < len(self.texts):
            self.__next += 1
        else:
            self.__next = 0
        return text
