from enum import Enum
import random

class StateEnum(Enum): 
    DEAD = 0
    ALIVE = 1

class TypeEnum(Enum):
    NONE = 0
    LEAF = 1
    BRANCH = 2
    SEED = 3

class Direction(Enum):
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

    def __add__(self, other):
        new_x, new_y = self.value[0] + other.value[0], self.value[1] + other.value[1]
        if new_x > 1 or new_x < -1 or new_y > 1 or new_y < -1: return Direction(None)
        return Direction(new_x, new_y)

    def __neg__(self):
        """ 
            Returns the opposite direction 
        """
        if self.value:
            return Direction(-self.value[0], -self.value[1])
    


def distance_from_cell(a: Direction|tuple, b: Direction|tuple, obs: list=[Direction.CENTRE], limits: tuple=(-1, 1)) -> dict[Direction:int]:
    q = [(a, 0)]
    visited = {a:0}
    moves = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]

    while len(q) > 0:
        pos, dist = q.pop(0)
        if pos == b: 
            return visited

        for d in moves: 
            new_pos = pos + d
            if new_pos == Direction.VOID: continue
            if new_pos in obs: continue
            if new_pos not in visited:
                q.append((new_pos, dist + 1))
                visited[new_pos] = dist + 1





def update_growth_chance(chances: dict, impossible_keys: list) -> dict:
    if len(impossible_keys) == 0: return chances  # nothing changes 
    elif len(impossible_keys) == len(chances): return None
    else:
        prob = .0 
        s = len([i for i in chances.keys() if i not in impossible_keys])
        for item in impossible_keys:
            if item in chances.keys():
                prob += chances[item]
                chances[item] = .0 
        to_distribute = prob/s
        for k in chances.keys():
            if k not in impossible_keys: 
                chances[k] += to_distribute 
        return chances

def pick_random(items: dict) -> Enum:
    # Using roulette wheel selection
    ws = sum(items.values()) 
    r  = random.random()
    for k, w in items.items():
        if r < w: return k
        r -= w



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
        self.structure = False

    def update(caller):
        """
            Returns True or False whether it grew.
        """
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
        self.generated = 0
        self.count += 1

    def get_neighbours(self) -> dict:
        """
            Return only valid neighbours, i.e. those that arent None
        """
        neigh = {}
        for dir, n in self.n.items():
            if n: neigh[dir] = n
        return neigh 
    
    def update(self):
        return self.cell_type.update(caller=self)

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
        Direction.UP: 0.4,
        Direction.UPLEFT: 0.25,
        Direction.UPRIGHT: 0.25,
        Direction.VOID: 0.1
    }

    def __init__(self):
        super().__init__()
        self.type = TypeEnum.SEED 

    def update(caller: Cell) -> bool:
        # -- Cases when it wont do a thing -- 
        if (caller.get_state() == StateEnum.DEAD or
            caller.generated   >= 2) : return False
        
        # Check the neighbouring cells for alive cells
        impossible_directions = []
        for d, n in caller.get_neighbours().items():
            if n.get_state() == StateEnum.ALIVE and d in SeedCell.growth_chance.keys():
                impossible_directions.append(d)

        actual_gc = update_growth_chance(SeedCell.growth_chance, impossible_keys=impossible_directions)
        chosen = pick_random(actual_gc)
        if chosen != Direction.VOID:
            if caller.n[chosen] == None: return False  # Grew outside
            caller.n[chosen].set_state(StateEnum.ALIVE)
            caller.n[chosen].cell_type = BranchCell
            caller.generated += 1
            return True
        else: return False


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
        
        for i in range(self.border_offset, self.h):
            for j in range(self.border_offset, self.w):
                for d in Look: 
                    if d is not Look.VOID:
                        cell =  self.matrix[i][j] 
                        if isinstance(self.matrix[i+d.value[0]][j + d.value[1]], Cell): 
                            cell.n[d] = self.matrix[i + d.value[0]][j + d.value[1]]
                        else: cell.n[d] = None

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
    b = Board(7,7)
    b.matrix[7][4].set_state(StateEnum.ALIVE)
    b.matrix[7][4].cell_type = SeedCell
    print(b)
    b.update()
    print(b)
    b.update()
    print(b)