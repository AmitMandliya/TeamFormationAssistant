from mysql.connector import connect
import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np
import scipy
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import mysql.connector
import sys
import math

connection = mysql.connector.connect(
    host="database",
    database='teamformationassistant',
    user="dbuser",
    password="dbuserpwd"
)

# connection = mysql.connector.connect(
# host="sefall2021.cosnmrdyk6wi.us-east-2.rds.amazonaws.com",
# database='teamformationassistant',
# user="root",
# password="SEFall2021"
# )

def persistTeamData(teamData, conn):
    if conn.is_connected():
        cursor = conn.cursor()
        for row in teamData.index:
            sql = "INSERT INTO Team(ProjectId, ProjectName, MemberId, MemberName)VALUES(%s,%s,%s,%s);"
            cursor.execute(sql,(str(teamData.loc[row, 'ProjectId']),str(teamData.loc[row, 'ProjectName']),str(teamData.loc[row, 'MemberId']),str(teamData.loc[row, 'MemberName'])))
        conn.commit()

def setEmployeeAssignement(employ, conn):
    if conn.is_connected():
        cursor = conn.cursor()
        sql ="UPDATE Member SET IsAssigned= %s WHERE MemberId = %s ;"
        cursor.execute(sql,(1,employ))
        conn.commit()

def memberToTeamMapping(MemberData,ProjectData,RequirementsData):
    jobIDs = RequirementsData['JobId'].tolist()
    employee = MemberData.loc[MemberData['IsAssigned'] == 0]
    employee = employee['MemberId'].tolist()
    teamData = pd.DataFrame(columns = ['ProjectId', 'ProjectName', 'MemberId', 'MemberName']) 

    for jobID in jobIDs:
        Req         = RequirementsData.loc[RequirementsData['JobId'] == jobID]
        reqLanguage = Req['LanguagePreferred'].tolist()[0]
        skillweight = float(Req['SkillWeight'])
        experienceWeight = float(Req['ExperienceWeight'])
        hoursWeight = float(Req['HoursWeight'])
        languageWeight =  float(Req['LanguageWeight'])
        budgetWeight =  float(Req['BudgetWeight'])
        ProjectId = Req['ProjectId'].tolist()[0]
        Project = ProjectData.loc[ProjectData['ProjectId'] == ProjectId]
        ProjectName = Project['ProjectName'].tolist()
        if(len(ProjectName) == 0):
            ProjectName = 'Not Provided'
        else:
            ProjectName = Project['ProjectName'].tolist()[0]
        
        highScore = 0
        selectedEmploy = ''
        for employ in employee:
            employData = MemberData.loc[MemberData['MemberId'] == employ]
            skillScore = float(employData['SkillScore'])
            expScore = float(employData['Experience'])
            availableHours = float(employData['AvailableHoursPerWeek'])
            hourlyRate = float(employData['HourlyRate'])
            languageScore = 0

            if reqLanguage in employData['Languages'].tolist()[0].split(","):
                languageScore = 1
            memscore = (skillweight*skillScore)/100+(experienceWeight*expScore)/10+(hoursWeight*availableHours)/40+(languageWeight*languageScore)/5+(budgetWeight*hourlyRate)/100
            if (memscore > highScore):
                selectedEmploy = employ
                highScore = memscore
        
        if (selectedEmploy not in employee):
            continue
        employee.remove(selectedEmploy)
        setEmployeeAssignement(int(selectedEmploy), connection)
        Member = MemberData.loc[MemberData['MemberId'] == selectedEmploy]
        MemberName = Member['MemberName'].tolist()[0]
        teamData = teamData.append({'ProjectId' :  ProjectId , 'ProjectName' : ProjectName, 'MemberId' : selectedEmploy, 'MemberName' : MemberName},  
                ignore_index = True)
    return teamData
        
       

def assignTeam():
    if connection.is_connected():
        Member_Query = pd.read_sql_query(
        '''select * from Member''', connection)
        Project_Query = pd.read_sql_query(
        '''select * from Project''', connection)
        Requirements_Query = pd.read_sql_query(
        '''select * from Requirements''', connection)
        MemberData = pd.DataFrame(Member_Query, columns=['MemberId','MemberName','DOB','Languages','IsAssigned',
        'HourlyRate','MemberRole','Experience','SkillScore','AvailableHoursPerWeek'])
        ProjectData = pd.DataFrame(Project_Query, columns=['ProjectId','ProjectName','ProjectEndDate','ProjectTeamSize','Budget',
        'Tools','IsAssignmentComplete','Priority'])
        RequirementsData = pd.DataFrame(Requirements_Query, columns=['JobId','ProjectId','LanguagePreferred','Skill','MemberRole',
        'AvailableHoursPerWeek','SkillWeight','ExperienceWeight','HoursWeight','LanguageWeight','BudgetWeight'])
        teamData = memberToTeamMapping(MemberData,ProjectData,RequirementsData)
        persistTeamData(teamData, connection)