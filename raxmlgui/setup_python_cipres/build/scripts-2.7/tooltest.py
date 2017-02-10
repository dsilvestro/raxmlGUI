#!/Library/Frameworks/Python.framework/Versions/2.7/Resources/Python.app/Contents/MacOS/Python
import sys
import os
import python_cipres.commands as CipresCommands

def main():
	return CipresCommands.tooltest(sys.argv)

if __name__ == "__main__":
    sys.exit(main())
