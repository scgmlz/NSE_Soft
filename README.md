# Mieze data management and reduction tool
Neutron Spin Echo software package

## Installation

Open a terminal window in the directory of the distribution and execute the following commands. The python requirements will be fetched from the requirements.txt file except two git bsed dependencies.

- Linux:

        sudo apt-get install python3.7
        sudo apt-get install python3-pip
        sudo pip3 install git+git://github.com/pyqtgraph/pyqtgraph.git
        sudo pip3 install git+git://github.com/AlexanderSchober/simpleplot_qt.git
        sudo setup.py install
        
- MacOs:

        ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
        brew install python
        sudo pip3 install git+git://github.com/pyqtgraph/pyqtgraph.git
        sudo pip3 install git+git://github.com/AlexanderSchober/simpleplot_qt.git
        sudo setup.py install
        
## Running the package

The software can be launched from the python interpreter through 'from mieze_python.main import Manager as mieze'. it is equally possible to launch it from a jupyter notebook using the same instruction. 
