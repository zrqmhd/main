import os
from Models.Game import Game
import socket

class Dealer:
   

    def __init__(self, port):
        
        Game.serverCount += 1
        self.serverID = Game.serverCount
        self.port = port
    
        if self.serverID-1 >= len(Game.serverPorts):
            raise ValueError("Not enough ports available for server instances")
        
        
        
        
    def startServer(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((Game.host, self.port))
            self.socket.listen()
            print(f"Server {self.serverID} listening on port {self.port}")
        except Exception as e:
            print(e)
            print("Failed to listen at "+ f"{self.port}")
            exit(0)

    def accept_connections(self):
       
        while Game.playerCount < Game.maxPlayers:
            print(f"Waiting for players to connect...{Game.maxPlayers - Game.playerCount} remaining...")

            conn, addr = self.socket.accept()

            try:
                (conn,addr,name,money,cards) ,data = self.receiveMessageUnicast((conn,addr,"",0,[]))
                newName, money = data.split(",")
                Game.players.append((conn, addr, newName, int(money),[]))
                print(f"Connected to {addr}\nPlayer Name: {newName}")
                Game.playerCount += 1

                self.broadcastMessage(f"New Player Joined {newName}\n")
            except Exception as e:
                print(e)
                exit(0)
                
    def dealCards(self):
       
        for deck in Game.deck:
            deck.shuffle()
        deck = Game.deck[0]
        if len(Game.dealerCards) == 0:
            Game.dealerCards.append(deck.pop())
        for player in Game.players:
            (conn,_,name,_,cards) = player
            for x in range(2):
                cards.append(deck.pop())
                
    def dealCardUnicast(self, address):
        
        deck = Game.deck[0]
        playerFound = False
        for player in Game.players:
            (conn,addr,name,_,cards) = player
            if address == addr:
                cards.append(deck.pop())
                playerFound=True
        if not playerFound: raise LookupError("No player found!")
        
        
    def checkPlayerCards(self, cards):
        
        if Game.sumCards(cards) > 21:
            return False
        return True
            
    def messageFormatter(self):
      
        msg = "-"*Game.terminalSize+"\n"
        msg += f"Dealer: {Game.dealerCards}\t Total: {Game.sumCards(Game.dealerCards)}" + "\n"
        msg += "-"*Game.terminalSize+"\n"
        for player in Game.players:
            msg += f"Player: {player[2]}\t Cards: {player[-1]}\t Total: {Game.sumCards(player[-1])}\t Chips: {player[-2]}" + "\n"
            msg += "-"*Game.terminalSize+"\n"
        return msg
    
    def messageFormatterUnicast(self, player):
        conn,_,name,money,cards = player
        msg = "-"*Game.terminalSize+"\n"
        msg += f"Dealer: {Game.dealerCards}\t Total: {Game.sumCards(Game.dealerCards)}" + "\n"
        msg += "-"*Game.terminalSize+"\n"
        msg += f"Player: {name}\t Cards: {cards}\t Total: {Game.sumCards(cards)}\t Chips: {money}" + "\n"
        msg += "-"*Game.terminalSize+"\n"
        return msg
                
    def getPlayerInformation(self):
       
        string = ""
        for idx,(_,_,name,money, cards) in enumerate(Game.players):
            if idx != len(Game.players)-1:
                string += f"Player {name} with ${money} and Cards: {cards}\n" 
            else:
                string += f"Player {name} with ${money} and Cards: {cards}"
        return string
            

    def receiveMessageUnicast(self, player):
      
        buffer = ""
        conn, addr, name, money, cards = player

        try:
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    print(f"Connection closed by {name} at {addr}")
                    break
                
                buffer += data
                if Game.eofChar in buffer:
                    message, buffer = buffer.split(Game.eofChar, 1)
                    return player, message.strip()
        except Exception as e:
            print(f"Error receiving message from {name} at {addr}: {e}")
        
        return player, ""
    
    def showDealerCards(self):
        deck = Game.deck[0]
        Game.dealerCards.append(deck.pop())
        

    def broadcastMessage(self, message):
   
        for player in Game.players:
            try:
                player[0].sendall(f"{message}\0".encode())
            except Exception as e:
                print(f"Player {player[2]} encountered an error...Removing them from game")
                Game.players.remove(player)
            
            
    def sendMessage(self, player, message):
   
        try:
            player[0].sendall(f"{message}\0".encode())
        except Exception as e:
            print(f"Exception {e}...Removing Player")
            Game.players.remove(player)
        
    def clearTerminal(self):
        os.system(Game.clearCommand)
        self.broadcastMessage("RESET")


    def close(self):
    
        self.socket.close()
        
    
                



