import json

class BoardIndexing:
    '''
        A class to label sudoku board indexes and cache them in data files

        ATTRIBUTES
        _cells: array of cell indexes from A1 ... I9
        _units: dictionary of index-units pairs (e.g. A1: [[row unit of A1], [col unit of A1], [subgrid unit of A1]])
        _peers: dictionary of index-peers pairs (e.g. A1: {A2 ... A9, B1 ... B9, subgrid of A1})

        METHODS
        _cross(A, B)
            function that takes the cross product of A and B
    '''
    def __init__(self):
        rows = '123456789'
        cols = 'ABCDEFGHI'
        subgrid_rows = ('123','456','789')
        subgrid_cols = ('ABC','DEF','GHI')

        # get every possible cell in a sudoku board, from A1 ... I9
        self._cells = self._cross(cols, rows)
        
        # list of cols. First list would be A1 ... I1
        col_indexes = [self._cross(number, rows) for number in cols]
        
        # list of rows. First list would be A1 ... A9
        row_indexes = [self._cross(cols, letter) for letter in rows]

        # list of subgrids. First row would be A1, A2, A3, B1, B2, B3, C1, C2, C3
        subgrid_indexes = [self._cross(col_slice, row_slice) for row_slice in subgrid_rows for col_slice in subgrid_cols]

        # list of all rows, columns, and subgrigds
        unit_list = (col_indexes + row_indexes + subgrid_indexes)

        # a dictionary where the keys are all possible cell indexes (A1 ... I9) and the values are that cell's units (row, column, and subgrid)
        self._units = dict((cell, [unit for unit in unit_list if cell in unit]) for cell in self._cells)

        # a dictionary where the keys are all possible cell indexes (A1 ... I9) and the values are that cell's distinct peers
        self._peers = dict((cell, list(set(sum(self._units[cell],[])) - set([cell]))) for cell in self._cells)

        cells = {
            "cells": self._cells
        }
        with open("../data/board_indexes/cells.txt", "w+") as cells_file:
            cells_file.write(json.dumps(cells))
        with open("../data/board_indexes/units.txt", "w+") as units_file:
            units_file.write(json.dumps(self._units))
        with open("../data/board_indexes/peers.txt", "w+") as peers_file:
            peers_file.write(json.dumps(self._peers))

    
    '''
        Cross product function

        PARAMS
        A: set of strings
        B: set of strings

        RETURNS
        A x B 
    '''    
    def _cross(self, A, B):
        # this takes the cross of A and B, assuming their elements are strings
        return [a + b for a in A for b in B] 


    '''
        Get functions for board index types
    '''
    def get_cell_indexes(self):
        return self._cells

    def get_unit_indexes(self):
        return self._units

    def get_peer_indexes(self):
        return self._peers
    
    


    