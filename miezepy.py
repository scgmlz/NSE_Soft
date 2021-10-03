from miezepy.mieze import Mieze
import sys
import traceback
from time import sleep
try:
    if __name__ == '__main__':
        sys.exit(Mieze(True))

except:
    print(sys.exc_info()[0])
    print(traceback.format_exc())
    print('Press Enter to Continue...')
    
    input()
