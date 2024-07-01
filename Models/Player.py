import select
from Models.Game import Game
import socket 
import os

class Player:

    gameOver = False

    def __init__(self):
        self.retries = 0
        self.name = input("Please enter your name:\t")
        self.money = (input("How much chips do you want to buy? (Enter in multiples of $500)\t"))
        self.money = 500 # Temporary
        while self.money % 500 != 0: self.money = int(input("How much chips do you want to buy? (Enter in multiples of $500)\t"))

        Game.playerCount += 1
        self.serverID = Game.playerCount
        
        while self.retries < Game.maxDealers:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((Game.host, Game.serverPorts[self.retries]))
                self.sendMessage(f"{self.name},{self.money}")
                
                while not Player.gameOver:
                    message = self.receiveMessage()
                    print(f"{message}")
                    
                    match message:
                        case "GAMEOVER":
                            Player.gameOver = True
                            print("Game Ended")
                            self.socket.close()
                            
                        case "GAMESTART":
                            self.receiveCards()
                        
                        case "TURN":
                            self.doAction()
                        
                        case "RESET":
                            os.system(Game.clearCommand)
                            
                        case "RESTART":
                            playAgain = input("Do you want to play again? Y/N").lower()
                            while playAgain != "y" and playAgain != "n":
                                playAgain = input("Do you want to play again? Y/N")
                            if playAgain == "y":
                                self.money = int(input("How much chips do you want to buy? (Enter in multiples of $500)\t"))
                                os.system(Game.clearCommand)
                                self.sendMessage(playAgain)
                                print("Waiting for server...")
                            else:
                                self.sendMessage(playAgain)
                                exit(0)
                        case _:
                            # print("Invalid Command")
                            pass
                self.retries = 0

            except Exception as e:
                self.retries += 1
                print(f"An error occurred: {e}...Retrying with next server")
                self.socket.close()
            
    def receiveCards(self):
        print(self.receiveMessage())

    def doAction(self):
        action = int(input("1. Stand\n2. Hit\n"))
        while action > 2 or action < 1:
            action = input("1. Stand\2. Hit")
        match action:
            case 1:
                self.sendMessage("STAND\0")
            case 2:
                self.sendMessage("HIT\0")
            case _:
                return
                    
    
    def sendMessage(self, message:str):
        try:
            self.socket.sendall((message+Game.eofChar).encode())
        except Exception as e:
            print(f"Failed to send message: {e}")

    def receiveMessage(self):
        try:
            buffer = ""
            while True:
                data = self.socket.recv(1024).decode()
                
                if not data:
                    Player.gameOver = True
                    print("Server closed the connection.")
                    break
                buffer += data
                if Game.eofChar in buffer:
                    message = buffer.split(Game.eofChar, 1)[0]
                    return message.strip()
            return buffer.strip()
        except Exception as e:
            print(f"Failed to receive message: {e}")
            return ""

        