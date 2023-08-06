#!/usr/bin/python3

import unittest
from spinney.tests import my_suite

def main():
    print('\n')
    print('-'*30)
    print('Tests to be run:')
    print('-'*30)
    runner = unittest.TextTestRunner(buffer=True)
    runner.run(my_suite())
