from Models.Card import Card, CardSymbol, CardValue
import random

class Deck:
    def __init__(self):
        self.cards = []
        for x in CardSymbol.__members__.keys():
            for y in CardValue.__members__.keys():
                self.cards.append(Card(x,y))
                
    def shuffle(self):
        print("Shuffling Cards...")
        random.shuffle(self.cards)
        print("Cards Shuffled!")
        
    def pop(self):
        return self.cards.pop()
        
    def __str__(self):
        return f"{self.cards}"
    
    def __repr__(self):
        return f"{self.cards}"
        