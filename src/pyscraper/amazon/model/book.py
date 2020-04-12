
class AmazonBook:
    def __init__(self, data):
        self.asin = data['ASIN']
        self.type = data['type']
        self.title = data['title']
        self.price = self.parsePrice(data['buyingPrice'])
        self.thumb = data['thumbnailImage']
        self.hasKindleEdition = data['hasKindleEdition']
        if self.hasKindleEdition:
            self.kindleAsin = data['kindleAsin']
        else:
            self.kindleAsin = ''
        self.usedAndNewLowestPrice = self.parsePrice(data['usedAndNewLowestPrice'])

    @staticmethod
    def parsePrice(price):
        return float(price[1:])

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
