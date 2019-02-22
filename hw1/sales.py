from search import Problem, hill_climbing, simulated_annealing, exp_schedule
import itertools
import math


class TSP(Problem):
    """An implementation of Travelling Salesperson Problem

    State representation:
        [n1, n2, n3...] gives the order in which the cities are visited
    Move representation:
        [x, y]: Swap the order of visit x with visit y
    """

    def __init__(self):
        """The distance from node x to node y is map[x][y] or map[y][x]"""
        self.map = [(0, 11, 29, 15, 6), (11, 0, 37, 42, 12), (29, 37, 0, 54, 2), (15, 42, 54, 0, 6), (6, 12, 2, 6, 0)]
        self.initial = [0, 1, 2, 3, 4]

    def actions(self, state):
        """Actions will swap the order of two moves
        """
        actions = []
        for i in range(5):
            for j in range(5):
                if i != j:
                    actions.append([i, j])
        return actions

    def result(self, state, move):
        """Makes the given swap on a copy of the given state."""
        new_state = list(state)
        i = new_state[move[0]]
        new_state[move[0]] = new_state[move[1]]
        new_state[move[1]] = i;
        return new_state

    def value(self, state):
        """This method computes a value of given state based on the distance
        """
        value = 0
        for i in range(len(state)):
            value -= self.map[state[i]][state[(i + 1) % len(state)]]

        return value


if __name__ == '__main__':

    p = TSP()

    print(p.value([0,1,2,3,4]))

    # Solve the problem using hill-climbing.
    hill_solution = hill_climbing(p)
    print('Hill-climbing solution       x: ' + str(hill_solution)
          + '\tvalue: ' + str(p.value(hill_solution))
          )

    # Solve the problem using simulated annealing.
    annealing_solution = simulated_annealing(
        p,
        exp_schedule(k=20, lam=0.005, limit=1000)
    )
    print('Simulated annealing solution x: ' + str(annealing_solution)
          + '\tvalue: ' + str(p.value(annealing_solution))
          )
