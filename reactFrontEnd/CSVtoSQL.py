import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np
import scipy
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import mysql.connector

# import sys


connection = mysql.connector.connect(
    host="sefall2021.cosnmrdyk6wi.us-east-2.rds.amazonaws.com",
    database='teamformationassistant',
    user="root",
    password="SEFall2021"
)


def main():
    # verifyDatabaseConnection()
    loadEmployeeDataFromCSV()


def verifyDatabaseConnection():
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        connection.commit()
        cursor.close()
        connection.close()


def loadEmployeeDataFromCSV():
    EmployeeData = pd.read_csv("../DataSet/Employee.csv")
    EmployeeData.columns = ['MemberID', 'Name', 'TeamID',
                            'Languages', 'Role',
                            'HourlyRate', 'DOB', 'Experience',
                            'SkillScore', 'Availibility',
                            'isAssigned']
    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute('DROP TABLE IF EXISTS Employee;')
        cursor.execute(
            'CREATE TABLE Employee(MemberID nvarchar(50), \
             Name nvarchar(50), TeamID nvarchar(50), \
             Languages nvarchar(50), Role nvarchar(50), \
             HourlyRate nvarchar(50), DOB nvarchar(50), \
             Experience nvarchar(50),SkillScore nvarchar(50),\
             Availibility nvarchar(50),isAssigned nvarchar(50))')
        for row in EmployeeData.index:
            sql = "INSERT INTO Employee(MemberID,Name,TeamID,\
            Languages,Role,HourlyRate,DOB,Experience,SkillScore,\
            Availibility,isAssigned)VALUES\
            (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            cursor.execute(sql, (str(EmployeeData.loc[row, 'MemberID']),
                                 str(EmployeeData.loc[row, 'Name']),
                                 str(EmployeeData.loc[row, 'TeamID']),
                                 str(EmployeeData.loc[row, 'Languages']),
                                 str(EmployeeData.loc[row, 'Role']),
                                 str(EmployeeData.loc[row, 'HourlyRate']),
                                 str(EmployeeData.loc[row, 'DOB']),
                                 str(EmployeeData.loc[row, 'Experience']),
                                 str(EmployeeData.loc[row, 'SkillScore']),
                                 str(EmployeeData.loc[row, 'Availibility']),
                                 str(EmployeeData.loc[row, 'isAssigned'])))
        connection.commit()


if __name__ == "__main__":
    main()
