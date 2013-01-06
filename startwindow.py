from tkinter import *
import messagebox
import sqlite3
import bracketWindow
import bracketDB
#Author - Dan Rabinowitz
class startWindow:
    #Create the window
    def __init__(self, tournament):
        #Set the tournament database as an instance variable
        self.tournament = tournament
        #Create the start window
        self.window = Tk()
        self.window.title("Start")
        #Create the new bracket option frame
        self.newFrameName = Frame(self.window, bd = "2", relief = "groove")
        self.newLabel = Label(self.newFrameName, text="Enter the name of a new tournament (no spaces): ")
        self.newTourneyName = Entry(self.newFrameName, width = "15")
        self.newSubmit = Button(self.newFrameName, text="Create", command = self.newTournament)
        self.newFrameName.pack()
        self.newLabel.pack(side="left")
        self.newTourneyName.pack(side="left")
        self.newSubmit.pack(side="left")        

        #Create the open frame
        self.openFrame = Frame(self.window, bd = "2", relief = "groove")
        self.openLabel = Label(self.openFrame, text="Enter the name of the tournament you want to open: ")
        self.openTourneyName = Entry(self.openFrame, width = "15")
        self.openSubmit = Button(self.openFrame, text="Open", command=self.openTournament)
        self.openFrame.pack()
        self.openLabel.pack(side="left")
        self.openTourneyName.pack(side="left")
        self.openSubmit.pack(side="left")

        #Quit button
        self.quitFrame = Frame(self.window)
        self.quitButton = Button(self.quitFrame, text="Quit", command = self.exitWindow)
        self.quitFrame.pack()
        self.quitButton.pack()

        #Loop the window
        self.window.mainloop()

    #Validate the name of the new tournament, and open the next window
    def newTournament(self):
        #Get the name of the new tournament, and connect to the database
        self.tourneyName = self.newTourneyName.get()
        connection = sqlite3.connect("tournament")
        cursor = connection.cursor()
        validName = True
        #Check to see if a name is entered
        if self.tourneyName=="":
            error = messagebox.showerror("Error", "Please enter a name for the self.tournament.")
            validName = False
        #Check the name for spaces
        for char in self.tourneyName:
            if char.isspace():
                error = messagebox.showerror("Error", "Please enter a name without spaces.")
                validName = False
        #Check to see if the tournament doesn't already exist
        if validName:
            try:
                cursor.execute("select * from "+self.tourneyName)
                error = messagebox.showerror("Error", "Please enter a name that doesn't already exist.")
            except:
                #Move on to the next window
                self.window.destroy()
                self.createNewTourneyWindow()
                
    #Set up the names window
    def createNewTourneyWindow(self):
        #Start the names window
        self.teamListWindow = Tk()
        self.teamListWindow.title("New Tournament")
        self.teams = [] #A list of a list of elements that will be in the add teams frame
        self.topLabel = Label(self.teamListWindow, text="Please enter the team names in order from best to worst.")
        self.topLabel.pack()
        #Create the first five add stats frame
        self.addTeamFrame = Frame(self.teamListWindow)
        self.addTeamFrame.pack()
        #Check to see if the demo is entered as a team name
        if self.tourneyName=="Demo":
            self.demoStrings =[]
            self.MLBTeams = ["Phillies", "Rays", "Yankees", "Twins", "Giants", "Reds", "Braves", "Rangers", "Padres", "Red Sox", "White Sox", "Cardinals", "Blue Jays", "Rockies", "A's", "Tigers", "Marlins", "Dodgers", "Angels", "Mets", "Brewers", "Astros", "Cubs", "Indians", "Nationals", "Royals", "Orioles", "Diamondbacks", "Mariners", "Pirates"]
            #Set up the demo team names in the add teams frame
            for i in range(len(self.MLBTeams)):
                self.teams.append(newTeamName(self.addTeamFrame, self.teams))
                self.demoStrings.append(StringVar())
                self.demoStrings[i].set(self.MLBTeams[i])
                self.teams[i].newTeamEntry.config(textvariable=self.demoStrings[i])
        else:
            #Make sure that the first 5 teams cannot be deleted, so a tournament will have at least 5 teams
            for i in range(5):
                self.teams.append(newTeamName(self.addTeamFrame, self.teams))
        #Create the second frame, with the submit button
        self.submitTeamsFrame = Frame(self.teamListWindow)
        self.submitTeamsButton = Button(self.submitTeamsFrame, text="Submit", command=self.submitTeams)
        self.submitTeamsFrame.pack()
        self.submitTeamsButton.pack()
        self.teamListWindow.mainloop()
        
    #Open an existing tournament
    def openTournament(self):
        tourn = self.openTourneyName.get()
        #Make sure the tournament name isn't blank
        if tourn!="":
            self.tournament.openDatabase(tourn, self.window)
        elif tourn=="":
            error = messagebox.showerror("Error", "Please enter the name of the tournament you want to open.")

    #Exit the window
    def exitWindow(self):
        self.window.destroy()

    #Submit the teams, and open the bracket
    def submitTeams(self):
        self.teamList = []
        submit = True
        #Check to make sure that no team's name is blank, or "Buy"
        for i in range(len(self.teams)):
            self.teamList.append(self.teams[i].newTeamEntry.get())
            if self.teamList[i]=="":
                submit = False
                error = messagebox.showerror("Error", "Please enter the name of the teams.")
            elif self.teamList[i]=="Buy":
                submit = False
                error = messagebox.showerror("Error", "Enter a different team name other than 'Buy.'")
        #Create a new table in the tournament database
        if submit:
            self.teamListWindow.destroy()
            if self.tourneyName=="Demo":
                self.tournament.createTournament ("Demo", len(self.MLBTeams), self.MLBTeams)
            else:
                self.tournament.createTournament (self.tourneyName, len(self.teamList), self.teamList)
            
#Object containing the entry field for another team
class newTeamName:
    #Create the frame where the user names the new team
    def __init__(self, frame, teamList):
        self.topFrame = frame
        self.teamList = teamList
        self.teamFrame = Frame(self.topFrame)
        self.newTeamEntry = Entry(self.teamFrame, width="15")
        self.addTeam = Button(self.teamFrame, text="Add Team", command = self.addTeamFrame)    
        self.teamFrame.pack()
        self.newTeamEntry.pack(side="left")
        self.addTeam.pack(side="left")
        #Don't include a delete button if this is less than the 5th team entry field
        if len(teamList)>4:
            self.deleteTeam = Button(self.teamFrame, text="Delete Team", command = self.deleteTeam)
            self.deleteTeam.pack(side="left")
        
    #Add another team
    def addTeamFrame(self):
        self.teamList.append(newTeamName(self.topFrame, self.teamList))

    #Delete the team
    def deleteTeam(self):
        self.teamFrame.pack_forget()
        self.teamFrame.destroy()
        self.teamList.remove(self.teamList[-1])



