'''
    An implementation of Mackworth's Arc Consistency Algorithm Three (AC3)
'''

from idna import valid_string_length


class AC3:
    def __init__(self, variables = None):
        self._variables = variables    

        # constraint lists
        # dictionary where key is constraint type and value is list of pairs of variables
        self._constraints = []

        self._arcs = []

    def set_variables(self, variables):
        self._variables = variables
    
    def set_constraints(self, constraints, inverse = False):
        self._constraints = constraints
        self._arcs.extend(constraints)
        if inverse:
            self._arcs.extend([x[::-1] for x in constraints])

        

    def ac3(self):
        agenda = self._arcs
        # emulate do while
        while True:
            arc = agenda.pop(0)
            if self.arc_reduce(arc):
                if len(self._variables[arc[0]]) == 0:
                    return False
                else:
                    agenda.extend([new_arc for new_arc in self._arcs if new_arc[1] == arc[0]])
            
            if len(agenda) == 0:
                break
        
        return self._variables
                    
    
    def arc_reduce(self, arc):
        x, y = arc
        changed = False
        x_domain = self._variables[x]
        y_domain = self._variables[y]
        for x_val in x_domain:
            is_val = True
            for y_val in y_domain:
                if x_val != y_val:
                    is_val = False
            if is_val:
                self._variables[x] = self._variables[x] - set([x_val])
                print('removed ' + x_val)
                changed = True
        return changed
                




    