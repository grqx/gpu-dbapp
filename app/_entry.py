from . import DB_PATH

import os.path
import sys


def main():
    if not os.path.exists(DB_PATH):
        print(f'database {DB_PATH} does not exist!')
        sys.exit(1)
    print('TODO')
