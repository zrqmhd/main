from Models.Dealer import Dealer
from Models.Game import Game
import os
import time
import copy

import argparse

def chooseLeader(dealers):
    leader = max(dealers, key=lambda d: d.serverID)
    return leader


def main():
    
    parser = argparse.ArgumentParser(prog="BlackJack")
    parser.add_argument("port")
    args = parser.parse_args()
    
    dealers = []
    
    for x in range(Game.maxDealers):
        dealers.append(Dealer(int(args.port)+x))
        
    dealer = chooseLeader(dealers)
        
    dealer.startServer()
    dealer.accept_connections()
    while len(Game.players) > 0:
        dealer.broadcastMessage(f"\033[32mAll Players Joined:\033[0m\n{dealer.getPlayerInformation()}")
        dealer.broadcastMessage("GAMESTART")
        dealer.dealCards()
        print("Cards Dealt!")
        time.sleep(1)
        
        for player in Game.players:
            # Send information to players
            conn, addr, name, money, cards = player
            dealer.sendMessage(player, dealer.messageFormatterUnicast(player))
        
        for player in Game.players:
            # Show information to dealer
            print(dealer.messageFormatter())
            # Send player information
            conn, addr, name, money, cards = player
            print(f"Player: {name}'s Turn")
            # Ask each player for Turn
            dealer.sendMessage(player, "TURN")
            _, msg = dealer.receiveMessageUnicast(player)
            print(msg)
            match msg:
                case "STAND":
                    pass
                case "HIT":
                    dealer.sendMessage(player,"RESET")
                    dealer.dealCardUnicast(addr)
                    dealer.sendMessage(player,dealer.messageFormatterUnicast(player))
            os.system(Game.clearCommand)
        
        
        dealerSum = Game.sumCards(Game.dealerCards)
        while dealerSum < 17 :
            # Get another card
            dealer.showDealerCards()
            dealerSum = Game.sumCards(Game.dealerCards)
            dealer.broadcastMessage("RESET")
            os.system(Game.clearCommand)
            print(dealer.messageFormatter())
            dealer.broadcastMessage(dealer.messageFormatter())
            
        dealer.broadcastMessage("RESET")
        os.system(Game.clearCommand)
        print(dealer.messageFormatter())
        dealer.broadcastMessage(dealer.messageFormatter())
        
        for player in Game.players:
            playerSum = Game.sumCards(player[4])
            if playerSum > 21:
                dealer.sendMessage(player, "LOSE")
            elif playerSum < dealerSum and dealerSum <= 21:
                dealer.sendMessage(player, "LOSE")
            elif playerSum == dealerSum:
                dealer.sendMessage(player, "DRAW")
            else:
                dealer.sendMessage(player, "WIN")
                           
        print("Status Sent!")
        time.sleep(1)
        
        print("\n")
        temp = copy.copy(Game.players)
        for player in temp:
            print(f"Asking {player[2]}")
            # ask for restarting
            dealer.sendMessage(player,"RESTART")
            _,reply = dealer.receiveMessageUnicast(player)
            if reply != "n":
                print(f"Player: {player[2]} wants to play again!")
            else:
                print(f"Player: {player[2]} left")
                Game.players.remove(player)
            time.sleep(1)
                
        dealer.clearTerminal()
        if len(Game.players) == 0: break
        for x in range(Game.playerCount):
            player = list(Game.players.pop())
            player[-1].clear()
            player[-2] = 0
            Game.players.append(tuple(player))
            
        print()
                
    
    
main()