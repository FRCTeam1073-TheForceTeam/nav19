import towerIdentification #imports tower identification functions in towerIdentification.py
import sys
import unittest

########## Test ###########

# quality, scan, degrees, distance

# Test case 1 : 4 towers in front (robot @ 100:114)
tc1_data = [(False,15,310.31,17.00), # noise
            (False,15,333.9,225.0), # tower A
            (False,15,322.31,5.00), # noise
            (False,15,345.75,406.5), # tower B
            (False,15,350.31,700.00), # noise
            (False,15,15.31,600.00), # noise
            (False,15,29.62,453.22), # tower C
            (False,15,35.31,600.00), # noise
            (False,15,47.96,301.63), # tower D
            (False,15,87.5,34.89)] # noise


# Test case 2 : 4 towers in back (robot @ 110:752)

# Test case 3 : 2 towers in front, 2 in back

# Test case 4 : more than 4 candidates

class TestExtractFeatures(unittest.TestCase):

    def test_all_towers_in_front(self):
        scanner = TowerIdentificationEverywhere.TowerIdentification()
        towerArray = scanner.extractFeatures(tc1_data, 0, 0, 0)
        self.assertEqual(len(towerArray),4)

        self.assertEqual(towerArray[0][2],333.9)
        self.assertEqual(towerArray[0][3],225.0)

        self.assertEqual(towerArray[1][2],345.75)
        self.assertEqual(towerArray[1][3],406.5)

        self.assertEqual(towerArray[2][2],29.62)
        self.assertEqual(towerArray[2][3],453.22)

        self.assertEqual(towerArray[3][2],47.96)
        self.assertEqual(towerArray[3][3],301.63)

        return

    def setup(self):
            f = open('./testdata/test_192_144_0', 'r')

if __name__ == '__main__':
    unittest.main()