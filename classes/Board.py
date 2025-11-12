from enum import Enum

class StateEnum(Enum): 
    DEAD = 0
    ALIVE = 1

class TypeEnum(Enum):
    NONE = 0
    TIP = 1
    MID = 2
    ROOT = 3



class Matrix: 
    def __init__(self, width, height):
        self.width_ = width
        self.height_ = height
        self.matrix_ = [[0]*width for row in range(height)]

    def get_matrix(self):
        return self.matrix_

    def get_shape(self):
        return self.width_, self.height_
    
    def set_shape(self, width, height):
        self.width_ = width
        self.height_ = height
        self.matrix_ = [[0]*width for row in range(height)]
    
    def __getitem__(self, i):
        return self.matrix_[i]
    
    def __setitem__(self, i, v):
        self.matrix_[i] = v


class SimpleCell():
    def __init__(self):
        self.type = TypeEnum.NONE

    def __str__(self):
        return "SimpleCell" 

    def update(self):
        pass


class Cell:
    def __init__(self, state=StateEnum.DEAD, cell_type=SimpleCell):
        self.state_ = state
        self.cell_type = cell_type 
    
    def update(self):
        self.cell_type.update()

    def __str__(self):
        return f"{self.state_.value}:{self.cell_type.__name__}"


class Board:
    def __init__(self, width, height):
        self.matrix = Matrix(width, height) 
        for i in range(height):
            for j in range(width):
                self.matrix[i][j] = Cell()
    
    def __str__(self):
        o = ""
        for i in self.matrix.get_matrix():
            o += "[ "
            for j in i:
                o += str(j) + " "
            o += "]\n"
        return o


if __name__ == "__main__":
    b = Board(5, 5)
    print(b)