'''
import tkinter as tk

class CountdownTimer:
    def __init__(self, master, time):
        self.master = master
        self.time = time
        self.paused = False
        
        self.remaining_time = tk.StringVar()
        self.remaining_time.set(self._format_time(self.time))
        
        self.label = tk.Label(master, textvariable=self.remaining_time, font=("Helvetica", 50))
        self.label.pack()
        
        self.pause_button = tk.Button(master, text="Pause", command=self.pause)
        self.pause_button.pack()
        
        self.start()
        
    def _format_time(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes:02d}:{seconds:02d}"
    
    def start(self):
        if self.time <= 0:
            self.label.config(text="Time's up!")
            return
        if not self.paused:
            self.remaining_time.set(self._format_time(self.time))
            self.time -= 1
        self.master.after(1000, self.start)
    
    def pause(self):
        self.paused = not self.paused
        if self.paused:
            self.pause_button.config(text="Resume")
        else:
            self.pause_button.config(text="Pause")

root = tk.Tk()
root.title("Countdown Timer")
timer = CountdownTimer(root, 60)
root.mainloop()
'''
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

#Import Library Section
import chess
import pygame
import pyttsx3 
import speech_recognition as sr
from chessboard import display
#Creating a board object from chess module
board = chess.Board()

#Text To Speech Section
engine = pyttsx3.init()
engine.runAndWait()
engine.setProperty('rate', 185)
voices = engine.getProperty('voices') 
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    
#Speech To Text Input Section
def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold=1
        audio=r.listen(source,timeout=5)
    try:
        print("Recognizing...")
        query=r.recognize_google(audio)
        print("You said: ", query)
        #querys = str(query)
        #print(query)
        return query
        
    except Exception as e:
        print(e)
        speak("Pardon me, can you please say that again...")
        return takeCommand()

#Display GUI board section

def showBoard(str1):
    bat = True
    strShow = str1
    while bat:
        display.start(str1)
        display.check_for_quit()
        bat = False
        exit()
        
#To run the chess game code section
def game():
    
    flagChance=1
    print("Welcome to Speech Chess, let's begin!")
    print()
    print("8 -A8 | B8 | C8 | D8 | E8 | F8 | G8 | H8")
    print("  --------------------------------------")
    print("7 -A7 | B7 | C7 | D7 | E7 | F7 | G7 | H7")
    print("  --------------------------------------")
    print("6 -A6 | B6 | C6 | D6 | E6 | F6 | G6 | H6")
    print("  --------------------------------------")
    print("5 -A5 | B5 | C5 | D5 | E5 | F5 | G5 | H5")
    print("  --------------------------------------")
    print("4 -A4 | B4 | C4 | D4 | E4 | F4 | G4 | H4")
    print("  --------------------------------------")
    print("3 -A3 | B3 | C3 | D3 | E3 | F3 | G3 | H3")
    print("  --------------------------------------")
    print("2 -A2 | B2 | C2 | D2 | E2 | F2 | G2 | H2")
    print("  --------------------------------------")
    print("1 -A1 | B1 | C1 | D1 | E1 | F1 | G1 | H1")
    print("  --------------------------------------")
    print("   A    B    C    D    E    F    G    H ")
    speak("Welcome to Speech Chess, let's begin!")
    speak("Please refer the matrix printed below for your moves")
    #Checks for game conditions section
    checkMate=bool(board.is_checkmate())
    gameOver=bool(board.is_game_over())  
    staleMate=bool(board.is_stalemate()) 
    materialInsufficient=bool(board.is_insufficient_material())
    
    str1 = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    showBoard(str1)

    #To run the game only till game over/checkmate/stalemate etc.
    while checkMate==False and gameOver==False and staleMate==False and materialInsufficient==False:
        print()
        
        #To speak which player's turn it is
        if(flagChance==1):
            speak("White player's turn")
            flagChance-=1
        elif(flagChance==0):
            speak("Black player's turn")
            flagChance+=1
        
        #To take input and compute the initial block 
        def initial():
            speak("Enter the initial block")
            s1=str(takeCommand())
            try:
                initialBlock = s1.lower()
                alphabet = initialBlock[0]
                digit = initialBlock[1]
                digit= int(digit)
                final = 0
                if alphabet == 'a': final = (digit-1)*8
                elif alphabet == 'b':final = ((digit-1)*8) + 1
                elif alphabet == 'c': final = ((digit-1)*8) + 2
                elif alphabet == 'd': final = ((digit-1)*8) + 3
                elif alphabet == 'e': final = ((digit-1)*8) + 4
                elif alphabet == 'f': final = ((digit-1)*8) + 5
                elif alphabet == 'g': final = ((digit-1)*8) + 6
                elif alphabet == 'h': final = ((digit-1)*8) + 7
                pieceFound = str(board.piece_at(final)).upper()

                if(pieceFound=="p" or pieceFound=="P"):
                    speak("Found pawn at" +str(initialBlock))
                    
                elif(pieceFound=="n" or pieceFound=="N"):
                    speak("Found knight at" +str(initialBlock))
                    
                elif(pieceFound=="r" or pieceFound=="R"):
                    speak("Found rook at" +str(initialBlock))
                    
                elif(pieceFound=="Q" or pieceFound=="q"):
                    speak("Found queen at" +str(initialBlock))
                    
                elif(pieceFound=="K" or pieceFound=="k"):
                    speak("Found king at" +str(initialBlock))
                    
                elif(pieceFound=="B" or pieceFound=="b"):
                    speak("Found bishop at" +str(initialBlock))
                    
                return pieceFound
            
            except Exception as e: 
                speak("I didn't get what you said, please try again!")
                print(e)
                return initial()
        
        #To take input and compute the final block
        def finall():
            pieceFound1 = initial()
            speak("Enter the final block")
            s2 = str(takeCommand())
            finalBlock = s2.lower()
            
            if str(pieceFound1)=='P':
                complete=str(finalBlock)
                try:
                    board.push_san(complete)
                    str1 = board.fen()

                except Exception as e:
                    speak("Invalid move, please try again!")
                    print(e)
                    return finall()
            
            else: 
                complete = str(pieceFound1)+str(finalBlock)
                try:
                    board.push_san(complete)
                    str1 = board.fen()

                except Exception as e:
                    speak("Invalid move, please try again!")
                    print(e)
                    return finall()
                
            str1 = board.fen()
            showBoard(str1)
        finall()

    #To check if it is "check"
    check=bool(board.is_check())
    if(check==True):
        speak("Check")
    if(checkMate==True):
        speak("Checkmate")
        
#To restart the game
    speak("Player 1, would you like to play again")
    choice1=takeCommand().lower

    speak("player 2, would you like to play again")
    choice2=takeCommand().lower()

    if choice1=='yes' and choice2=='yes':
        game()



game()