from Models.Deck import Deck
import os
import sys

class Game:
    # Terminal Info
    terminalSize = os.get_terminal_size().columns
    if sys.platform.startswith("linux"):
        clearCommand = "clear"
    elif sys.platform.startswith("win32"):
        clearCommand = "cls"
    else:
        clearCommand = "clear"
        
    # Communication
    eofChar = "\0"
    # Servers
    serverCount:int = 0
    host:str = "localhost"
    serverPorts:list[int] = [3003,3004,3005]
    # Players
    maxPlayers = 3
    playerCount:int = 0
    players = []
    # Dealers
    maxDealers:int = 3
    dealerCount:int = 0
    dealers:list = []
    dealerCards = []
    
    # Game Constants
    deckCount = 1
    deck = [Deck() for x in range(deckCount)]
    
    # Game Messages
    turn = "TURN"
    stand = "STAND"
    hit = "HIT"
    gameover = "GAMEOVER"
    gamestart = "GAMESTART"
    restart = "RESTART"
    
    def sumCards(cards:list)->int:
        """
        Calculate the total sum of all the cards
        """
        total = 0
        for card in cards:
            total += card.getValue()
        return total
    
    def __init__(self):
        pass
