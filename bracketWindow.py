from tkinter import *
import math
import random
import bracketDB
import messagebox
import startwindow
#Author - Dan Rabinowitz
class window:
    def __init__(self, table, teams, teamList, tournamentExists, openPos):
        #Set the positions of the teams and the tournament database as instance variables
        self.openPos=openPos
        self.tournament = bracketDB.tournamentDB()
        self.main = Tk()
        self.main.title (table)
        self.table = table
        #Add the number of buyTeams to the total number of teams to make the number of teams 2^x
        self.team =[]
        self.roundLabel = []
        if math.log(teams, 2)==int(math.log(teams, 2)):
            self.rounds = int(math.log(teams, 2)*2)
            buyTeams = 0
        else:
            buyTeams = abs((2**math.ceil(math.log(teams, 2))) - teams)
            self.rounds = int(math.ceil(math.log(teams, 2))*2)
            teams +=buyTeams
        #Label the top row with round numbers
        for roundNum in range(self.rounds+1):
            if roundNum < math.ceil(self.rounds/2):
                self.roundLabel.append(Label(self.main, text="Round "+str(roundNum+1)))
                self.roundLabel[roundNum].pack()
                self.roundLabel[roundNum].grid(row=0, column=roundNum)
            elif roundNum == math.ceil(self.rounds/2):
                self.roundLabel.append(Label(self.main, text="Champion"))
                self.roundLabel[roundNum].pack()
                self.roundLabel[roundNum].grid(row=0, column=roundNum)
            elif roundNum > math.ceil(self.rounds/2):
                self.roundLabel.append(Label(self.main, text="Round "+str(self.rounds - roundNum+1)))
                self.roundLabel[roundNum].pack()
                self.roundLabel[roundNum].grid(row=0, column=roundNum)
        #Set up lists for canvases and team names that go in the bracket
        self.canvases = []
        count=[]
        self.teamNames = teamList
        buyTeam = []
        self.button_name = []
        lineXStart= 0
        #Set the teams list to include the buys
        for i in range(teams):
            if i>=(teams-buyTeams):
                self.teamNames.append("Buy")
        #Order the teams list so that the self.teamNames are correct
        for flips in range(1, self.rounds):
            flipstep = int(2**flips)
            for x in range(len(self.teamNames)//flipstep):
                for i in range(1, (flipstep//2) + 1):
                    folds = -i + (flipstep//2) +1
                    self.teamNames.insert((flipstep*x)+(flipstep-folds), self.teamNames[len(self.teamNames)-(((flipstep//2)*x)+folds)])
            self.teamNames=self.teamNames[:teams]
        #Update the database of the new positions
        if tournamentExists==False:
            for i in range(len(self.teamNames)):
                self.tournament.saveTourney(table, self.teamNames[i], 0, i)
        #Set up the lists necessary to create the bracket
        for i in range(int(self.rounds/2)):
            count.append(0)
            self.team.append([])
            self.button_name.append([])
        #Set up the bracket
        for side in range(0,self.rounds+1,self.rounds):
            if side>0:
                lineXStart=60
            #First and last column, with no lines and arrows
            for i in range(1,int(teams+1),2):
                self.button_name[0].append(StringVar())
                self.team[0].append(Button(self.main, width = "10", relief="flat", textvariable=self.button_name[0][count[0]], command=(lambda x = count[0], z = 0: self.teamWin(x, z))))
                team=self.teamNames[count[0]]
                self.button_name[0][count[0]].set(team)
                if self.teamNames[count[0]]=="Buy":
                    self.team[0][count[0]].config(state="disabled")
                self.team[0][count[0]].pack()
                self.team[0][count[0]].grid(row = i, column = side)
                count[0]+=1
            #Creates the team buttons, lines and arrows for every other column
            for roundNum in range(1,self.rounds//2):
                startRow = int(2**(roundNum))
                rowInterval = int(2**(roundNum+1))
                endRow = int((teams+1) - (2**roundNum))
                canvasesHeight = int(20*(2**(roundNum-1)))
                for i in range(startRow,endRow,rowInterval):
                    #Create the remaining elements in the button_name string variable list
                    self.button_name[roundNum].append(StringVar())
                    #Top arrow
                    self.canvases.append([])
                    self.canvases[roundNum-1].append(Canvas(width=60, height=canvasesHeight))
                    self.canvases[roundNum-1][2*count[roundNum]].pack()
                    self.canvases[roundNum-1][2*count[roundNum]].grid(row = (i-(2**(roundNum-1))), column = abs(side-roundNum) , rowspan=2**(roundNum-1))
                    self.canvases[roundNum-1][2*count[roundNum]].create_line(lineXStart,5,30,5)
                    self.canvases[roundNum-1][2*count[roundNum]].create_line(30,5,30,canvasesHeight, arrow="last")
                    #Team button
                    self.team[roundNum].append(Button(self.main, width = "10", relief="flat", state="disabled",textvariable=self.button_name[roundNum][count[roundNum]], command=(lambda x = count[roundNum], y = roundNum: self.teamWin(x, y))))
                    self.team[roundNum][count[roundNum]].pack()
                    self.team[roundNum][count[roundNum]].grid(row = i, column = abs(side-roundNum))
                    #Bottom arrow
                    self.canvases[roundNum-1].append(Canvas(width=60, height=canvasesHeight))
                    self.canvases[roundNum-1][2*count[roundNum] + 1].pack()
                    self.canvases[roundNum-1][2*count[roundNum] + 1].grid(row = i+1, column =abs(side-roundNum) , rowspan=2**(roundNum-1))
                    self.canvases[roundNum-1][2*count[roundNum] + 1].create_line(lineXStart,(canvasesHeight-5),30,(canvasesHeight-5))
                    self.canvases[roundNum-1][2*count[roundNum] + 1].create_line(30,(canvasesHeight-5),30,0, arrow="last")
                    count[roundNum]+=1
        #Advance the teams that have a buy the first round
        for i in range(len(self.button_name[0])):
            if self.button_name[0][i].get()=="Buy" and tournamentExists==False:
                self.teamWin(i-1,0)
        #Set the undo instance variables to 0, as there is nothing yet to undo
        self.lastRoundChanged=0
        self.lastPosChanged=0
        #Create the champion label
        self.champion = StringVar()
        self.championLabel = Label(self.main, textvariable=self.champion)
        self.championLabel.pack()
        self.championLabel.grid(row=(teams+1)//2, column=(self.rounds+1)//2)
        #Create the restart button
        self.restartButton = Button(self.main, text="Restart", command=self.restart)
        self.restartButton.pack()
        if teams>8:
            self.restartButton.grid(row=(teams-2), column=((self.rounds+1)//2)+1)
        else:
            self.restartButton.grid(row=8, column=((self.rounds+1)//2)+1)
        #Create the quit button
        self.quitButton = Button(self.main, text="Quit", command=self.quitProgram)
        self.quitButton.pack()
        if teams>8:
            self.quitButton.grid(row=(teams-2), column=(self.rounds+1)//2)
        else:
            self.quitButton.grid(row=8, column=(self.rounds+1)//2)
        #Create the undo button
        self.undoButton = Button(self.main, text="Undo", command=self.undo)
        self.undoButton.pack()
        if teams>8:
            self.undoButton.grid(row=(teams-2), column=((self.rounds+1)//2)-1)
        else:
            self.undoButton.grid(row=8, column=((self.rounds+1)//2)-1)
        if tournamentExists:
            self.openChanges()
        self.main.mainloop()

    #Move a team on to the next round and update the database
    def teamWin(self, num, roundpos):
        #Make sure there is an opponent before a team advances
        if roundpos!=0:
            if num%2==0:
                opponentPos = num+1
            else:
                opponentPos = num-1
            opponentExists = self.button_name[roundpos][opponentPos].get()!=""
        else:
            opponentExists=True
        if opponentExists:
            #Activate the button in the next round, and set the button text as the team name
            current_team = self.button_name[roundpos][num].get()
            if roundpos==(self.rounds//2)-1:
                self.champion.set(current_team)
            else:
                self.button_name[roundpos+1][math.floor(num/2)].set(current_team)                        
                self.team[roundpos+1][math.floor(num/2)].config(state="active")
            #Disable the buttons from the previous round
            top_team = math.floor(num/2)*2
            bottom_team = top_team+1
            self.team[roundpos][top_team].config(state="disabled")
            self.team[roundpos][bottom_team].config(state="disabled")
            #Send the data to the bracketDB
            self.tournament.saveTourney(self.table, current_team, (roundpos+1), math.floor(num/2))
            self.lastRoundChanged = roundpos+1
            self.lastPosChanged = math.floor(num/2)
        else:
            #Display an error is no opponent exists
            error = messagebox.showerror("Error", "No opponent exists.")

    #Apply changes to the bracket if the user is opening an existing tournament
    def openChanges(self):
        for i in range(len(self.openPos)):
            #Set the champion label, if a champion has been set
            if self.openPos[i][2]==self.rounds/2:
                self.champion.set(self.openPos[i][0])
            else:
                #Set the other buttons as active, and set the button names as team names according to the database
                for roundCount in range(self.openPos[i][2]+1):
                    roundIndex = roundCount
                    roundPos = math.floor(self.openPos[i][1]/(2**roundCount))
                    self.button_name[roundIndex][roundPos].set(self.openPos[i][0])
                self.team[self.openPos[i][2]][self.openPos[i][3]].config(state="active")
        #Disable the buttons in the rounds that have already been decided
        for roundNum in range((self.rounds//2)-1):
            for pos in range(len(self.team[roundNum])):
                if self.button_name[roundNum+1][math.floor(pos/2)].get()!="":
                    self.team[roundNum][pos].config(state="disabled")

    #Restart function
    def restart(self):
        self.main.destroy()
        tournament = bracketDB.tournamentDB()
        start = startwindow.startWindow(tournament)

    #Quit function
    def quitProgram(self):
        self.main.destroy()

    #Undo function
    def undo(self):
        roundpos = self.lastRoundChanged
        num = self.lastPosChanged
        if roundpos>0:
            #Reset the database to exclude the last win
            #Reset the database to exclude the last win
            if self.champion.get()=="":
                self.tournament.undoLastSave(self.table, self.button_name[roundpos][num].get())
                #Erase the button name and disable the team button that just won
                self.button_name[roundpos][num].set("")
                self.team[roundpos][num].config(state="disabled")
            else:
                self.tournament.undoLastSave(self.table, self.champion.get())
                #Erase the button name and disable the team button that just won
                self.champion.set("") 
            previousRoundTeamPos = num*2
            previousRoundOpponentPos = num*2 +1
            #Reactivate the matchup that had just been decided
            if self.button_name[roundpos-1][previousRoundTeamPos].get()!="Buy":
                self.team[roundpos-1][previousRoundTeamPos].config(state="active")
            if self.button_name[roundpos-1][previousRoundOpponentPos].get()!="Buy":
                self.team[roundpos-1][previousRoundOpponentPos].config(state="active")
            #Disable the undo button
            self.lastRoundChanged = 0
            self.lastPosChanged = 0
        else:
            error = messagebox.showerror("Error", "Nothing to undo.")
 
