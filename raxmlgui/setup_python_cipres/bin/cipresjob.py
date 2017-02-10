#!/usr/bin/env python
import sys
import os
import python_cipres.commands as CipresCommands

def main():
	return CipresCommands.cipresjob(sys.argv)

if __name__ == "__main__":
    sys.exit(main())
