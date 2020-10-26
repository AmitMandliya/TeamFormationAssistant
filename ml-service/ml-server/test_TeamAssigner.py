import warnings
import unittest
import pytest
from unittest.mock import MagicMock, patch
import TeamAssigner
import pandas as pd
import mysql.connector


class testTeamAssigner(unittest.TestCase):
    
  def testSetEmployeeAssignment(self):
    """ Tests the method setEmployeeAssignment of TeamAssigner.py """
    testSQL ="UPDATE Member SET IsAssigned= %s WHERE MemberId = %s ;"
    with patch(target='mysql.connector.connect') as mock:
      TeamAssigner.setEmployeeAssignement(1, mock)
      mockCursor = mock.cursor()

    self.assertIsNotNone(mock)
    self.assertTrue(mock.commit.called)
    mockCursor.execute.assert_called_once_with(testSQL, (1,1))
    self.assertTrue(mockCursor.execute.called)
    self.assertTrue(mock.is_connected.called)

  def testPersistTeamData(self):
    """ Tests the method persistTeamData of TeamAssigner.py """
    mockTeamDataDf = pd.DataFrame(columns = ["ProjectId", "ProjectName", "MemberId", "MemberName"])
    mockTeamDataDf = mockTeamDataDf.append({"ProjectId": 3, "ProjectName": 'PQR', 'MemberId': '40', 'MemberName': 'Rick'}, ignore_index=True)

    testSQL = "INSERT INTO Team(ProjectId, ProjectName, MemberId, MemberName)VALUES(%s,%s,%s,%s);"

    with patch(target='mysql.connector.connect') as mock:
      TeamAssigner.persistTeamData(mockTeamDataDf, mock)
      mockCursor = mock.cursor()
    
    self.assertIsNotNone(mock)
    self.assertTrue(mock.commit.called)
    mockCursor.execute.assert_called_with(testSQL, (str(mockTeamDataDf.loc[0, 'ProjectId']),str(mockTeamDataDf.loc[0, 'ProjectName']),str(mockTeamDataDf.loc[0, 'MemberId']),str(mockTeamDataDf.loc[0, 'MemberName'])))
    self.assertTrue(mockCursor.execute.called)
    self.assertTrue(mock.is_connected.called)

if __name__ == '__main__':
  unittest.main()

