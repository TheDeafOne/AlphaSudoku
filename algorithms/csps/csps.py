'''
    A constraint satisfaction problem solver
'''

from . import ac3

class CSPS:
    def __init__(self):
        self.value = 'csps test'
    
    def run(self):
        ac3.AC3().run()
        print(self.value)