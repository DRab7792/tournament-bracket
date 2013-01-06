import sqlite3
import bracketWindow
import messagebox
import startwindow
from tkinter import *
import math
#Author - Dan Rabinowitz
class tournamentDB:    
    #Connect to the database
    def __init__(self):
        self.connection = sqlite3.connect("tournament")
        self.cursor = self.connection.cursor()

    #Create a tournament
    def createTournament(self, tourneyName, numTeams, teamList):
        teamData=[]
        #Create a list of tuples that contain the data for each team
        for i in range(numTeams):
            teamData.append((i, teamList[i], i, 0, i))
        #Create and update the table using the list of teams
        self.cursor.execute('''create table '''+tourneyName+'''(
                                teamNum integer,
                                name text,
                                startPos integer,
                                currentRound integer,
                                currentPos integer)''')
        for i in range(len(teamData)):
            self.cursor.execute('''insert into '''+tourneyName+'''(
                                teamNum, name, startPos, currentRound, currentPos)
                                values(?,?,?,?,?)''', teamData[i]
                            )
        self.connection.commit()
        #Create the bracket window with the list of teams
        bracketWindow.window(tourneyName, numTeams, teamList, False, (0,))

    #View the table
    def viewTournamentTable(self, tourneyName):
        self.cursor.execute('''select * from '''+tourneyName)
        bracketTeams = self.cursor.fetchall()
        print('TeamNum   Name      startPos  currentRound  currentPos')
        for row in bracketTeams:
            print('%d         %-12s     %d          %d        %d' % \
                  (row[0], row[1], row[2], row[3], row[4]))

    #Open a tournament
    def openDatabase(self, tourneyName, openwindow):
        #Make sure that the tournament name entered exists
        try:
            self.cursor.execute("select name from "+tourneyName)
            teams = self.cursor.fetchall()
            teamList = []
            #Turn the tuple into a list
            for i in range(len(teams)):
                teamList.append(teams[i][0])
            #Get the list of teams, as well as their information from the database and pass it on to the bracket window
            self.cursor.execute("select name, startPos, currentRound, currentPos from "+tourneyName)
            openteams = self.cursor.fetchall()
            self.connection.close()
            openwindow.destroy()
            bracketWindow.window(tourneyName, len(teams), teamList, True, openteams)
        except:
            #Give an error message if the tournament doesn't exist
            error = messagebox.showerror("Error", "Please enter the name of a tournament that exists.")  
                        
    #Save the tournament
    def saveTourney(self, tourneyName, curTeam, roundNum, pos):
        self.cursor.execute('''select * from '''+tourneyName)
        tournament = self.cursor.fetchall()
        teamData = []
        for i in range(len(tournament)):
            #Update the current team in the database in the case of a team win
            if tournament[i][1] == curTeam and roundNum!=0:
                for teamProp in range(3):
                    teamData.append(tournament[i][teamProp])
                teamData.append(str(roundNum))
                teamData.append(str(pos))
                #Create a tuple to update the database with
                updateData = (teamData[3], teamData[4], str(teamData[0]))
                self.cursor.execute('''update '''+tourneyName+''' set 
                                        currentRound='''+updateData[0]+''', 
                                        currentPos='''+updateData[1]+''' 
                                        where teamNum='''+updateData[2]
                                    )
            #Update the starting positions of the teams based on the shuffling of the teams when the bracket window opens
            elif tournament[i][1]==curTeam and roundNum==0:
                teamData.append(tournament[i][0])
                teamData.append(tournament[i][1])
                teamData.append(str(pos))
                teamData.append(str(roundNum))
                teamData.append(str(pos))
                #Create a tuple to update the database with
                updateData = (teamData[2], teamData[3], teamData[4], str(teamData[0]))
                self.cursor.execute('''update '''+tourneyName+''' set
                                        startPos='''+updateData[0]+''',
                                        currentRound='''+updateData[1]+''', 
                                        currentPos='''+updateData[2]+''' 
                                        where teamNum='''+updateData[3]
                                    )
        self.connection.commit()
        
    #Erase a tournament from the database
    def clearDB(self, tourneyName):
        self.cursor.execute('''drop table '''+tourneyName)

    #Change back the team that just won to the previous round
    def undoLastSave(self, tourneyName, teamChange):
        self.cursor.execute('''select * from '''+tourneyName)
        tournament=self.cursor.fetchall()
        teamData=[]
        #Select the data from the team that needs to be changed back
        for i in range(len(tournament)):
            if tournament[i][1]==teamChange:
                for x in range(5):
                    teamData.append(tournament[i][x])
        #Change back the round number and the position
        oldPos = math.floor(teamData[2])
        for i in range(teamData[3]):
            #Revert the team back to the old position depending on whether or not it was champion
            if (oldPos/2**i) > 0 and (oldPos/2**i)<1:
                oldPos = 1
            else:
                oldPos = math.floor(oldPos/2**i)
        teamData[3]-=1
        teamData[4]=oldPos
        #Send the values to the database
        updateData = (str(teamData[3]), str(teamData[4]), str(teamData[0]))
        self.cursor.execute('''update '''+tourneyName+''' set
                                        currentRound='''+updateData[0]+''', 
                                        currentPos='''+updateData[1]+''' 
                                        where teamNum='''+updateData[2]
                                    )
        self.connection.commit()
        

