class AC3:
    '''
        An implementation of Mackworth's Arc Consistency Algorithm Three (AC3)

        ATTRIBUTES
        _variables: a dictionary where key: variable, value: domain of variable
        _arcs: list of constraints and their inverse (e.g. if (A1, A2) is in _arcs, then (A2, A1) will also be in arcs)

        METHODS
        ac3()
            implementation of ac3 algorithm
        
        revise(x, y)
            prunes values from domain of variable x with respect to the values in the domain of variable y
    '''
    def __init__(self, variables={}, constraints=[], inverse = False):
        self._variables = variables    
        self._arcs = [x[::-1] for x in constraints] if inverse else constraints

 
    '''
        Arc consistency algorithm 3
        cycles through agenda and revises domain of elements in each arc
    '''
    def ac3(self):
        agenda = self._arcs
        
        # cycle through agenda while it contains arcs
        while len(agenda) > 0:
            # arbitrary arc (e.g. (A1, A2))
            x, y = agenda.pop(0)

            if self.revise(x, y): # true if domain of x has changed
                if len(self._variables[x]) != 0:
                    agenda.extend([new_arc for new_arc in self._arcs if new_arc[1] == x])
                else:
                    return False # empty domain
        
        return self._variables
                    
    
    '''
        Prunes values from domain of variable x with respect to the values in the domain of variable y

        RETURNS
        True if domain of variable x has changed, False otherwise
    '''
    def revise(self, x, y):
        changed = False
        # grab domains of variables x and y
        x_domain = self._variables[x]
        y_domain = self._variables[y]

        # cycle through x domain and prune domain values accordingly
        for x_val in x_domain:
            if any([x_val == y_val for y_val in y_domain]): # true if every value in y domain is == x_val
                self._variables[x] = self._variables[x] - set([x_val])
                changed = True # domain of X has changed

        return changed
                
    
    '''
        Get and set functions
    '''
    def set_variables(self, variables):
        self._variables = variables
    
    def get_variables(self):
        return self._variables


    