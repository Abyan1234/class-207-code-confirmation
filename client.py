#-----------------Boilerplate Code Start-----------
import socket
from tkinter import *
from  threading import Thread
import random
from PIL import ImageTk, Image

screen_width = None
screen_height = None

SERVER = None
PORT = None
IP_ADDRESS = None
playerName = None

canvas1 = None
canvas2 = None

nameEntry = None
nameWindow = None
gameWindow = None

leftBoxes = []
rightBoxes = []
finishingBox = None

playerType = None
playerTurn = None
player1Name = 'joining'
player2Name = 'joining'
player1Label = None
player2Label = None

player1Score = 0
player2Score = 0
player2ScoreLabel = None
player2ScoreLabel = None

dice = None

rollButton = None
resetButton = None

winingMessage = None

winningCall = 0


leftBoxes = []
rightBoxes = []
finishingBox = None

playerType = None
dice = None

def resetGame2():
    global SERVER
    SERVER.send("Reset Game".encode('utf-8'))

def handleReset():
    global canvas2
    global playerType
    global gameWindow
    global rollButton
    global dice
    global screen_width
    global screen_height
    global playerTurn
    global leftBoxes
    global rightBoxes
    global finishingBox
    global resetButton
    global winningMessage
    global winningCall

    canvas2.itemconfigure(dice,text='\u2681')
    if(playerType=='player1'):
        rollButton = Button(gameWindow,text="Roll Dice", fg='black', font=("Chalkboard SE", 15), bg="grey",command=rollDice, width=20, height=5)
        rollButton.place(x=screen_width / 2 - 80, y=screen_height/2  + 250)
        playerTurn=True
    if(playerType=='player2'):
        playerTurn=False
    for box in leftBoxes[1:]:
        box.configure(bg="white")
    for box in rightBoxes[-2::-1]:
        box.configure(bg="white")
    finishingBox.configure(bg='green')
    canvas2.itemconfigure(winningMessage,text="")
    resetButton.destroy()
    winningCall=0

def handleWin(message):
    global canvas2
    global playerType
    global gameWindow
    global rollButton
    global dice
    global screen_width
    global screen_height
    global playerTurn
    global leftBoxes
    global rightBoxes
    global finishingBox
    global resetButton
    global winningMessage
    global winningCall

    if('Red' in message):
        if(playerType=='player1'):
            rollButton.destroy()
    elif('Yellow' in message):
        if(playerType=='player2'):
            rollButton.destroy()
    
    canvas2.itemconfigure(winningMessage,text="Congratulations!!")
    resetButton.place(x=screen_width/2-80,y=screen_height-220)



def checkColorPosition(boxes,color):
    for box in boxes:
        boxColor=box.cget("bg")
        if boxColor==color:
            return boxes.index(box)
    return False


def movePlayer1(steps):
    global leftBoxes
    boxPosition=checkColorPosition(leftBoxes[1:],"red")
    if boxPosition:
        diceValue=steps
        coloredBoxIndex=boxPosition
        totalSteps=10
        remainingSteps=totalSteps-coloredBoxIndex
        if steps==remainingSteps:
            for box in leftBoxes[1:]:
                box.configure(bg="white")
            global finishingBox
            finishingBox.configure(bg="red")
            global SERVER 
            global playerName
            message="Red has won the game!!"
            SERVER.send(message.encode('utf-8'))
        elif steps<remainingSteps:
            for box in leftBoxes[1:]:
                box.configure(bg="white")
            nextStep=coloredBoxIndex+1+diceValue
            leftBoxes[nextStep].configure(bg="red")
        else:
            print("Steps greater than needed")
    else:
        leftBoxes[steps].configure(bg="red")


def movePlayer2(steps):
    global rightBoxes
    boxPosition=checkColorPosition(rightBoxes[-2::-1],"yellow")
    if boxPosition:
        diceValue=steps
        coloredBoxIndex=boxPosition
        totalSteps=10
        remainingSteps=totalSteps-coloredBoxIndex
        if steps==remainingSteps:
            for box in rightBoxes[-2::-1]:
                box.configure(bg="white")
            global finishingBox
            finishingBox.configure(bg="yellow")
            global SERVER 
            global playerName
            message="Yellow has won the game!!"
            SERVER.send(message.encode('utf-8'))
        elif steps<remainingSteps:
            for box in rightBoxes[-2::-1]:
                box.configure(bg="white")
            nextStep=coloredBoxIndex+1+diceValue
            rightBoxes[::-1][nextStep].configure(bg="yellow")
        else:
            print("Steps greater than needed")
    else:
        rightBoxes[steps].configure(bg="yellow")


def rollDice():
    global SERVER
    global rollButton
    global playerType
    global playerTurn

    diceChoices=['\u2680','\u2681','\u2682','\u2683','\u2684','\u2685']
    value=random.choice(diceChoices)
    rollButton.destroy()
    playerTurn=False
    if playerType=='player1':
        SERVER.send(f'{value}player2turn'.encode('utf-8'))
    elif playerType=='player2':
        SERVER.send(f'{value}player1turn'.encode('utf-8'))







def leftBoard():
    global gameWindow
    global leftBoxes
    global screen_height

    xPos = 30
    for box in range(0,11):
        if(box == 0):
            boxLabel = Label(gameWindow, font=("Helvetica",30), width=2, height=1, relief='ridge', borderwidth=0, bg="red")
            boxLabel.place(x=xPos, y=screen_height/2 - 100)
            leftBoxes.append(boxLabel)
            xPos +=50
        else:
            boxLabel = Label(gameWindow, font=("Helvetica",30), width=2, height=1, relief='ridge', borderwidth=0, bg="white")
            boxLabel.place(x=xPos, y=screen_height/2- 100)
            leftBoxes.append(boxLabel)
            xPos +=50


def rightBoard():
    global gameWindow
    global rightBoxes
    global screen_height

    xPos = 830
    for box in range(0,11):
        if(box == 10):
            boxLabel = Label(gameWindow, font=("Helvetica",30), width=2, height=1, relief='ridge', borderwidth=0, bg="yellow")
            boxLabel.place(x=xPos, y=screen_height/2-100)
            rightBoxes.append(boxLabel)
            xPos +=50
        else:
            boxLabel = Label(gameWindow, font=("Helvetica",30), width=2, height=1, relief='ridge', borderwidth=0, bg="white")
            boxLabel.place(x=xPos, y=screen_height/2 - 100)
            rightBoxes.append(boxLabel)
            xPos +=50


def finishingBox():
    global gameWindow
    global finishingBox
    global screen_width
    global screen_height

    finishingBox = Label(gameWindow, text="Home", font=("Chalkboard SE", 32), width=8, height=4, borderwidth=0, bg="green", fg="white")
    finishingBox.place(x=screen_width/2 - 80, y=screen_height/2 -160)



def gameWindow():

    global gameWindow
    global canvas2
    global screen_width
    global screen_height
    global dice



    gameWindow = Tk()
    gameWindow.title("Ludo Ladder")
    gameWindow.attributes('-fullscreen',True)

    screen_width = gameWindow.winfo_screenwidth()
    screen_height = gameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file = "./assets/background.png")

    canvas2 = Canvas( gameWindow, width = 500,height = 500)
    canvas2.pack(fill = "both", expand = True)

    # Display image
    canvas2.create_image( 0, 0, image = bg, anchor = "nw")

    # Add Text
    canvas2.create_text( screen_width/2, screen_height/5, text = "Ludo Ladder", font=("Chalkboard SE",100), fill="white")

    winningMessage=canvas2.create_text(screen_width/2,screen_height/2+250,text="",font=("Chalkboard SE",100),fill='#fff176')  

    resetButton=Button(gameWindow,text="reset game",fg='black',font=("Chalkboard SE",100),bg="grey",command=resetGame2,width=15,height=5)

    # Teacher Activity
    leftBoard()
    rightBoard()

   
    finishingBox()
    

    global rollButton 
    rollButton = Button(gameWindow,text="Roll Dice", fg='black', font=("Chalkboard SE", 15), bg="grey",command=rollDice, width=16, height=5)
    
    global playerTurn
    global playerType
    global playerName


    if(playerType == 'player1' and playerTurn):
        rollButton.place(x=screen_width / 2 - 80, y=screen_height/2  + 250)
    else:
        rollButton.pack_forget()


    

    # Creating Dice with value 1
    dice = canvas2.create_text(screen_width/2 + 10, screen_height/2 + 100, text = "\u2680", font=("Chalkboard SE",250), fill="white")

    gameWindow.resizable(True, True)
    gameWindow.mainloop()

    



def saveName():
    global SERVER
    global playerName
    global nameWindow
    global nameEntry

    playerName = nameEntry.get()
    nameEntry.delete(0, END)
    nameWindow.destroy()

    SERVER.send(playerName.encode())

    # Boilerplate Code
    gameWindow()



def askPlayerName():
    global playerName
    global nameEntry
    global nameWindow
    global canvas1

    nameWindow  = Tk()
    nameWindow.title("Ludo Ladder")
    nameWindow.attributes('-fullscreen',True)


    screen_width = nameWindow.winfo_screenwidth()
    screen_height = nameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file = "./assets/background.png")

    canvas1 = Canvas( nameWindow, width = 500,height = 500)
    canvas1.pack(fill = "both", expand = True)
    # Display image
    canvas1.create_image( 0, 0, image = bg, anchor = "nw")
    canvas1.create_text( screen_width/2, screen_height/5, text = "Enter Name", font=("Chalkboard SE",100), fill="white")

    nameEntry = Entry(nameWindow, width=15, justify='center', font=('Chalkboard SE', 50), bd=5, bg='white')
    nameEntry.place(x = screen_width/2 - 220, y=screen_height/4 + 100)


    button = Button(nameWindow, text="Save", font=("Chalkboard SE", 30),width=15, command=saveName, height=2, bg="#80deea", bd=3)
    button.place(x = screen_width/2 - 130, y=screen_height/2 - 30)

    nameWindow.resizable(True, True)
    nameWindow.mainloop()



# Boilerplate Code
def recivedMsg():
    
    global SERVER
    global playerType
    global playerTurn
    global rollButton
    global screen_width
    global screen_height
    global canvas2
    global dice
    global gameWindow


    while True:
        message = SERVER.recv(2048).decode()

        if('player_type' in message):
            recvMsg = eval(message)
            playerType = recvMsg['player_type']
            playerTurn = recvMsg['turn']
        elif('player_names' in message):
            players=eval(message)
            players=players["player_names"]
            for i in players:
                if(i["type"]=='player1'):
                    player1Name=i['name']
                elif(i["type"]=='player2'):
                    player2Name=i['name']

        elif('⚀' in message):
            # Dice with value 1
            canvas2.itemconfigure(dice, text='\u2680')
        elif('⚁' in message):
            # Dice with value 2
            canvas2.itemconfigure(dice, text='\u2681')
        elif('⚂' in message):
            # Dice with value 3
            canvas2.itemconfigure(dice, text='\u2682')
        elif('⚃' in message):
            # Dice with value 4
            canvas2.itemconfigure(dice, text='\u2683')
        elif('⚄' in message):
            # Dice with value 5
            canvas2.itemconfigure(dice, text='\u2684')
        elif('⚅' in message):
            # Dice with value 6
            canvas2.itemconfigure(dice, text='\u2685')

        elif('won the game' in message and winningCall==0):
            winningCall+=1
            handleWin(message)

        elif('reset game' in message):
            handleReset()

        if('player1Turn' in message and playerType == 'player1'):
            playerTurn = True
            rollButton = Button(gameWindow,text="Roll Dice", fg='black', font=("Chalkboard SE", 15), bg="grey",command=rollDice, width=20, height=5)
            rollButton.place(x=screen_width / 2 - 80, y=screen_height/2  + 250)

        elif('player2Turn' in message and playerType == 'player2'):
            playerTurn = True
            rollButton = Button(gameWindow,text="Roll Dice", fg='black', font=("Chalkboard SE", 15), bg="grey",command=rollDice, width=20, height=5)
            rollButton.place(x=screen_width / 2 - 80, y=screen_height/2  + 260)

        if('player1Turn' in message or 'player2Turn' in message):
            diceChoices=['⚀','⚁','⚂','⚃','⚄','⚅']
            diceValue=diceChoices.index(message[0])+1
            if('player1Turn' in message):
                movePlayer2(diceValue)
            elif('player2Turn' in message):
                movePlayer1(diceValue)






def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    PORT  = 6000
    IP_ADDRESS = '127.0.0.1'

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))

    # Boilerplate Code
    thread = Thread(target=recivedMsg)
    thread.start()

    askPlayerName()




setup()
