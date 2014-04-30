import argparse

parser = argparse.ArgumentParser()
parser.add_argument('date', type=int, help='enter single date')
args = parser.parse_args()
print(args)
print(args.date)
