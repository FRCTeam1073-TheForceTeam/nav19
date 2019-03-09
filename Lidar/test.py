import fieldScanner #Katherine - import the scanner methods
import sys

########## Test ###########

# quality, scan, degrees, distance

# Test case 1 : 4 towers in front (robot at 100:114)
tc1_data = [(False,15,310.31,17.00), # noise
            (False,15,318.31,171.41), # tower A
            (False,15,322.31,5.00), # noise
            (False,15,345.84,446.15), # tower B
            (False,15,350.31,700.00), # noise
            (False,15,15.31,600.00), # noise
            (False,15,24.92,498.40), # tower C
            (False,15,35.31,600.00), # noise
            (False,15,58.64,245.93), # tower D
            (False,15,65.31,600.00)]


# Test case 2 : 4 towers in back

# Test case 3 : 2 towers in front, 2 in back

# Test case 4 : more than 4 candidates

def main(path):
        print(__file__ + " start!!")

        scanner = fieldScanner.fieldScanner()

        scanner.extractFeatures(tc1_data, 0, 0, 0)

        return

if __name__ == '__main__':
    main(sys.argv[0])
