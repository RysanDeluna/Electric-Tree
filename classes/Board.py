from enum import Enum

class StateEnum(Enum): 
    DEAD = 0
    ALIVE = 1

class TypeEnum(Enum):
    NONE = 0
    TIP = 1
    MID = 2
    ROOT = 3

class Look(Enum):
    "Off set para observar o vizinho"
    UP = -1, 0
    UPLEFT = -1, -1
    UPRIGHT = -1, 1
    DOWN= 1, 0 
    DOWNLEFT = 1, -1 
    DOWNRIGHT = 1, 1 
    RIGHT =  0, 1 
    LEFT = 0, -1
    CENTRE = 0, 0 


class Matrix: 
    def __init__(self, width, height):
        self.width_ = width
        self.height_ = height
        self.matrix_ = [[0]*width for row in range(height)]

    def get_matrix(self): return self.matrix_

    def get_shape(self): return self.width_, self.height_
    
    def set_shape(self, width, height):
        self.width_ = width
        self.height_ = height
        self.matrix_ = [[0]*width for row in range(height)]
    
    def __getitem__(self, i):  return self.matrix_[i]
    
    def __setitem__(self, i, v): self.matrix_[i] = v


class SimpleCell:
    def __init__(self):
        self.type = TypeEnum.NONE

    def update(n, caller):
        caller.cell_type = RootCell  # Exemplo de como alterar o tipo de célula
        pass

    def __str__(self): return __name__


class RootCell(SimpleCell):
    def __init__(self):
        super().__init__()
        self.type = TypeEnum.ROOT 

    def update(caller):
        caller.cell_type = SimpleCell

    def __str__(self): return super().__str__()


class Cell:
    def __init__(self, state=StateEnum.DEAD, cell_type=SimpleCell, id=None):
        self.state_ = state
        self.cell_type = cell_type 
        self.id = id
        self.n = {} 

    def get_neighbours(self):
        return self.n
    
    def update(self):
        self.cell_type.update(self.n, caller=self)

    def get_state(self): return self.state_

    def spy(self):
        o = ""
        for d, n in self.n.items():
            o += f"{d:<10}\t:{n.id:<4}\t{n.get_state()}\n"
        print(o)

    def __str__(self): 
        return f"{self.state_.name}:{self.cell_type.__name__}" if not self.id else f"{self.id}:{self.state_.name}"


class Board:
    border_offset = 1   # How thick is the border

    def __init__(self, width, height):
        # Define the board effective area with its borders
        self.matrix = Matrix(width+2, height+2) 
        self.w = width + self.border_offset   # Effective width
        self.h = height + self.border_offset  # Effective height
        
        count=0
        # populate
        for i in range(self.border_offset, self.h):
            for j in range(self.border_offset, self.w):
                self.matrix[i][j] = Cell(id=str(count))
                count+=1
        
        for i in range(self.border_offset, self.h):
            for j in range(self.border_offset, self.w):
                for d in Look: 
                    cell =  self.matrix[i][j] 
                    if isinstance(self.matrix[i+d.value[0]][j + d.value[1]], Cell): 
                        cell.get_neighbours()[d] = self.matrix[i + d.value[0]][j + d.value[1]]

    def update(self):
        for i in range(1, self.h):
            for j in range(1, self.w):
                self.matrix[i][j].update()
    
    def __str__(self):
        o = ""
        m = self.matrix.get_matrix()
        max_len = max(len(str(x)) for row in m for x in row)
        for row in m:
            o += "[ " + " ".join(f"{str(x):>{max_len}}" for x in row) + " ]\n"
        return o


if __name__ == "__main__":
    b = Board(5, 5)
    print(b)