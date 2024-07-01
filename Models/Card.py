from enum import Enum, StrEnum

class CardSymbol(StrEnum):
    diamond = "Diamonds"
    spades = "Spades"
    heart = "Hearts"
    clubs = "Clubs"

class CardValue(Enum):
    ace = ("Ace", 1)
    two = ("Two", 2)
    three = ("Three", 3)
    four = ("Four", 4)
    five = ("Five", 5)
    six = ("Six",6)
    seven = ("Seven", 7)
    eight = ("Eight", 8)
    nine = ("Nine", 9)
    ten = ("Ten", 10)
    jack = ("Jack", 10)
    queen = ("Queen", 10)
    king = ("King", 10)
    

class Card:
    def __init__(self, cardSymbol:CardSymbol, cardValue:CardValue)->None:        
        self.symbol = CardSymbol[cardSymbol]
        self.info = CardValue[cardValue]
        
    def getValue(self):
        return self.info.value[1]
    def getSymbol(self):
        return self.symbol.value
        
    def __str__(self):
        return f"{self.info.value[0].capitalize()} of {self.symbol.value}"
    def __repr__(self):
        return f"{self.info.value[0].capitalize()} of {self.symbol.value}"
    
    def __gt__(self,otherCard):
        return self.info.value[1] > otherCard.info.value[1]
    def __lt__(self,otherCard):
        return self.info.value[1] < otherCard.info.value[1]
    def __eq__(self,otherCard):
        return self.info.value[1] == otherCard.info.value[1]
    def __add__(self,othercard):
        return self.info.value[1] + othercard.info.value[1]
        
