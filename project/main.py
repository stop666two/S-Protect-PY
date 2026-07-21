import sys
from utils import greet
from helpers.math import add
def main():
    print(greet("World"))
    print(f"2+3={add(2,3)}")
if __name__ == "__main__":
    main()
