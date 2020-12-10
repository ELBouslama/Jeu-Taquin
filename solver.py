from queue import PriorityQueue
from random import shuffle

class Position: # For PriorityQueue, to make "<" do the right thing.
        def __init__(self,dimension, position, start_distance,heuristic):
            self.position = position
            self.start_distance = start_distance
            self.dimension=dimension

            if heuristic=="malplace":
                self.heuristic = self.heuristic_malplace(position)
            else :
                self.heuristic = self.heuristic_distance(position)
            
        """
        H1
        """
        def heuristic_distance(self,puzzle):
            N=self.dimension
            return sum(abs(i//N - puzzle[i]//N) + abs(i%N - puzzle[i]%N) for i in range(N*N - 1))

        """
        H2
        """
        def heuristic_malplace(self,puzzle):
            N=self.dimension
            return sum(int((i//N != puzzle[i]//N) or (i%N != puzzle[i]%N)) for i in range(N*N - 1))



        def __lt__(self, other): # For A* and Dijkstra start_distance is indeed distance to start position
                return self.heuristic + self.start_distance < other.heuristic + other.start_distance




class Solver:
    def __init__(self,dimension,puzzle,heuristic,fix=True):
        self.dimension=dimension
        self.puzzle=puzzle
        assert heuristic in ["malplace","distance"]
        self.heuristic=heuristic
        self.fix=True

    """
    Find legal moves
    """
    def moves(self,position):
        N=self.dimension
        blank = position.index(N*N-1)
        x, y = divmod(blank, N)
        offsets = []
        if x>0: offsets.append(-N)  # Down
        if x<N-1: offsets.append(N) # Up
        if y>0: offsets.append(-1)  # Right
        if y<N-1: offsets.append(1) # Left
        for offset in offsets:
            swap = blank + offset
            yield tuple(position[swap] if x==blank else position[blank] if x==swap else position[x] for x in range(N*N))


    """
    fixer taquin pour debuter de l'indice 0 (adaptation avec les lists python)
    """
    def fix_index(self,puzzle):
        start=[]
        for i in puzzle:
            if i!=0: start.append(i-1)
            else : start.append(self.dimension*self.dimension-1)
        return start

    def solve(self,log=True):
        N=self.dimension
        start=self.fix_index(self.puzzle)
        start = tuple(start)
        if log:
            print (start)
        current_puzzle = Position(N,start, 0,self.heuristic)
        open_list = PriorityQueue()
        open_list.put(current_puzzle)
        closed_list = set([current_puzzle]) # Tuples rather than lists so they go into a set.
        came_from = {current_puzzle.position: None}

        while current_puzzle.position != tuple(range(N*N)):
            current_puzzle = open_list.get()
            for k in self.moves(current_puzzle.position):
                if k not in closed_list:
                    open_list.put(Position(N,k,current_puzzle.start_distance+1,self.heuristic))
                    came_from[k] = current_puzzle
                    closed_list.add(k)
        
        solution=[]
        while current_puzzle.position != start:       
            next_puzzle = came_from[current_puzzle.position]
            for i,j in zip(next_puzzle.position,current_puzzle.position):
                if i!=N*N-1 and i!=j:
                    solution.append(i+1)
            current_puzzle=next_puzzle
        return solution
        




if __name__ == '__main__':
    solver=Solver(3,[1, 0, 3, 6, 5, 2, 7, 4,8],"malplace")
    solver.solve()