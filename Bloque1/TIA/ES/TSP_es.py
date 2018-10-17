import random
import math

seed = random.random()
random.seed(0.4845872451543184)

# Open input file
infile = open('Qatar.tsp', 'r')

# Read instance header
Name = infile.readline().strip().split()[1] # NAME
FileType = infile.readline().strip().split()[1] # TYPE
Comment = infile.readline().strip().split()[1] # COMMENT
Dimension = infile.readline().strip().split()[1] # DIMENSION
EdgeWeightType = infile.readline().strip().split()[1] # EDGE_WEIGHT_TYPE
infile.readline()

# Read node list
distances = []
N = int(Dimension)
for i in range(0, int(Dimension)):
    x,y = infile.readline().strip().split()[1:]
    distances.append([float(x), float(y)])

# Close input file
infile.close()

cities = list(range(len(distances)))
max_iterations = 1000000
N = len(distances)

def initialize_solution(size):

    sol = random.sample(range(size), size)

    return sol

def distance(x, y):
    posx = distances[x]
    posy = distances[y]
    dist = math.sqrt(((posx[0]-posy[0])**2)+((posx[1]-posy[1])**2))
    return dist


def fitness(individual):
    fitness_value = 0

    for element in individual:
        if element == individual[-1]:
            fitness_value += distance(element, individual[0])
        else:
            fitness_value += distance(element, individual[individual.index(element)+1])

    return fitness_value

def swap(solution):

    pos1 = random.randint(0, N - 1)
    pos2 = random.randint(0, N - 1)
    while pos2 == pos1:
        pos2 = random.randint(0, N - 1)

    aux1 = solution[pos1]
    aux2 = solution[pos2]

    solution[pos1] = aux2
    solution[pos2] = aux1

    return solution


if __name__ == '__main__':

    sol = initialize_solution(N)
    new_sol = []
    T=100000000000000


    for i in range(max_iterations):
        f_s = fitness(sol)
        new_sol = sol.copy()
        new_sol = swap(new_sol)

        f_ns = fitness(new_sol)
        dif = f_s - f_ns
        if dif>0: #si mejora el fitness
            sol = new_sol.copy()
            print("-------------------")
            print("NEW BEST SOLUTION: (ITER)", i)
            print(f_ns, sol)

        else:
            if T>0 and math.exp(dif/T) > 0.1:
                sol = new_sol.copy()

                print("-------------------")
                print("NEW NOT BEST SOLUTION: (ITER)", i)
                print(f_ns, sol)
            T = T/(i+0.01*T)


