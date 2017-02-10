#!/usr/bin/env python
import sys
import os
import python_cipres.commands as CipresCommands

def main():
	return CipresCommands.tooltest(sys.argv)

if __name__ == "__main__":
    sys.exit(main())
