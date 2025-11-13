from enum import Enum
import random


def pick_random(items: list|dict, weights=[]) -> Enum:
    # Using roulette wheel selection
    ws = sum(items.values()) if len(weights) == 0 else sum(weights)
    r  = random.random()
    if len(weights) == 0:  # Dealing with dict 
        for k, w in items.items():
            if r < w: return k
            r -= w
    else:
        for i in range(len(weights)):
            if r < weights[i]: return i
            r -= weights[i]

class StateEnum(Enum): 
    DEAD = 0
    ALIVE = 1

class TypeEnum(Enum):
    NONE = 0
    LEAF = 1
    BRANCH = 2
    SEED = 3

class Look(Enum):
    "Offset to look at neighbour"
    UP = -1, 0
    UPLEFT = -1, -1
    UPRIGHT = -1, 1
    DOWN= 1, 0 
    DOWNLEFT = 1, -1 
    DOWNRIGHT = 1, 1 
    RIGHT =  0, 1 
    LEFT = 0, -1
    CENTRE = 0, 0 
    VOID = None


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


class BaseCell:
    def __init__(self):
        self.type = TypeEnum.NONE

    def update(caller):
        # caller.cell_type = SeedCell  # Exemplo de como alterar o tipo de célula
        pass

    def __str__(self): return __name__


class Cell:
    count = 0
    def __init__(self, state=StateEnum.DEAD, cell_type=BaseCell, id=None):
        self.state_ = state
        self.cell_type = cell_type 
        self.id = id
        self.n = {} 
        self.count += 1

    def get_neighbours(self):
        return self.n
    
    def update(self):
        self.cell_type.update(caller=self)

    def get_state(self): return self.state_
    def set_state(self, state): self.state_ = state 
    def switch_state(self):
        if self.state_ == StateEnum.DEAD: self.state_ = StateEnum.ALIVE
        elif self.state_ == StateEnum.ALIVE: self.state_ = StateEnum.DEAD

    def spy(self):
        o = ""
        for d, n in self.n.items():
            o += f"{d:<10}\t:{n.id:<4}\t{n.get_state()}\n"
        print(o)

    def __str__(self): 
        return f"{self.state_.name}:{self.cell_type.__name__}" if not self.id else f"{self.id}:{self.state_.name}"


class SeedCell(BaseCell):
    growth_chance = {
        Look.UP: 0.4,
        Look.UPLEFT: 0.25,
        Look.UPRIGHT: 0.25,
        Look.VOID: 0.1
    }

    def __init__(self):
        super().__init__()
        self.type = TypeEnum.SEED 

    def update(caller: Cell):
        if caller.get_state() == StateEnum.DEAD: return
        chosen = pick_random(SeedCell.growth_chance)
        if chosen != Look.VOID:
            caller.n[chosen].set_state(StateEnum.ALIVE)
            caller.n[chosen].cell_type = BranchCell


class LeafCell(BaseCell):
    def __init__(self):
        super().__init__()
        self.type = TypeEnum.LEAF

    def update(caller):
        pass

class BranchCell(BaseCell):
    def __init__(self):
        super().__init__()
        self.type = TypeEnum.BRANCH

    def update(caller):
        pass


class Board:
    border_offset = 1   # How thick is the border

    def __init__(self, width, height):
        # Define the board effective area with its borders
        self.matrix = Matrix(width+2, height+2) 
        self.w = width + self.border_offset   # Effective width
        self.h = height + self.border_offset  # Effective height
        
        # populate
        for i in range(self.border_offset, self.h):
            for j in range(self.border_offset, self.w):
                self.matrix[i][j] = Cell(id=str(i)+str(j))
                if i == self.w - 1: 
                    self.matrix[i][j].set_state(StateEnum.ALIVE)
                    self.matrix[i][j].cell_type = SeedCell
        
        for i in range(self.border_offset, self.h):
            for j in range(self.border_offset, self.w):
                for d in Look: 
                    if d is not Look.VOID:
                        cell =  self.matrix[i][j] 
                        if isinstance(self.matrix[i+d.value[0]][j + d.value[1]], Cell): 
                            cell.get_neighbours()[d] = self.matrix[i + d.value[0]][j + d.value[1]]
                        else: cell.get_neighbours()[d] = None

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


import os
if __name__ == "__main__":
    os.system("cls")
    b = Board(6,6)
    print(b)
    b.update()
    print(b)
