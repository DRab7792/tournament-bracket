import sqlite3
import messagebox
from tkinter import *
import math
import random
import startwindow
import bracketDB
import bracketWindow
#Author - Dan Rabinowitz
#Create the tournament object that acts as the database, and is called throughout the program
tournament = bracketDB.tournamentDB()
#Initiate the start window
start = startwindow.startWindow(tournament)
