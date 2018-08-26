#!/usr/bin/env python3

# compatibility execution helper for Windows requiring a .py-file, just redirecting execution to original 'colctl' file

import argparse
from importlib.machinery import SourceFileLoader
import os

if __name__ == '__main__':    
    path = os.path.abspath(__file__)
    dir_path = os.path.dirname(path)
    colctl = SourceFileLoader("colctl", os.path.join(dir_path, "colctl")).load_module()
    parser = argparse.ArgumentParser()
    colctl.main(parser)