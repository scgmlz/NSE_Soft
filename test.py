import nose
import os
argv = ['-w', os.path.join('.', 'miezepy', 'tests'), '--processes', '0']
nose.main(argv=argv) 