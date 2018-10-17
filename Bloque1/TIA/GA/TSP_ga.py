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
for z in range(0, int(Dimension)):
    x,y = infile.readline().strip().split()[1:]
    distances.append([float(x), float(y)])

# Close input file
infile.close()

cities = list(range(len(distances)))
max_iterations = 100000
N = len(distances)


def initialize_population(size):
    pop = []
    for i in range(100):
        pop.append(random.sample(range(size), size))
    return pop


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


def selection(population, fitness_values):

    p=[]
    m_fit = sum(fitness_values)

    for i in range(len(population)):
        p.append(fitness_values[i]/m_fit)

    selected = []

    while len(selected) < 10:
        for tio in range(len(population)):
            if p[tio]> random.random():
                selected.append(population[tio])

    return selected


def selectionalt(population, fitness_values):

    selected = []
    auxval = []
    auxpos= []

    while len(selected) < 10:
        selected.append(population[fitness_values.index(min(fitness_values))])

        auxval.append(fitness_values[fitness_values.index(min(fitness_values))])
        auxpos.append(fitness_values.index(min(fitness_values)))

        fitness_values[fitness_values.index(min(fitness_values))] = math.inf

    for ppp in range(len(auxpos)):
        fitness_values[auxpos[ppp]] = auxval[ppp]

    return selected

def crossing(selected_pop):

    new_pop = []
    for i in range(len(selected_pop)-1):
        n = len(selected_pop[i])
        part1 = 2*(n//3)
        p1 = selected_pop[i]
        p2 = selected_pop[i+1]
        block11 = p1[:part1]
        block22 = p2[part1:]


        if set(block11).intersection(block22) == set():
            new_pop.append(block11 + block22)
        else:
            repeated_elements = list(set(block11).intersection(block22))
            for element in block22:
                if element in repeated_elements:
                    block22[block22.index(element)] = None

            new_pop.append(block11 + block22)
            toaddn1 = set(cities) ^ set(new_pop[i])
            toaddn1.remove(None)
            for j in range(len(new_pop[i])):
                if new_pop[i][j] == None:
                    new_pop[i][j] = toaddn1.pop()


    return new_pop

def mutation(p1):

    for m in range(len(p1)//5):
        pos1 = random.randint(0, N - 1)
        pos2 = random.randint(0, N - 1)
        while pos2 == pos1:
            pos2 = random.randint(0, N - 1)

        aux1 = p1[pos1]
        aux2 = p1[pos2]

        p1[pos1] = aux2
        p1[pos2] = aux1

    return p1


def replacement(population, fitness_values, cross_members):

    newpop=[]
    best = population[fitness_values.index(min(fitness_values))]
    alt = []
    for i in range(len(cross_members)):
        p = mutation(cross_members[i])
        alt.append(p)


    newpop.append(best)

    for j in range(len(cross_members)):
        newpop.append(cross_members[j])

    for k in range(len(cross_members)):
        newpop.append(alt[k])

    for l in range(100-len(newpop)):
        newpop.append(random.sample(range(N), N))

    return newpop

def apocalypsis(population, fitness_values, size):

    index1 = fitness_values.index(min(fitness_values))
    p1 = population[index1]

    pop = []
    pop.append(p1)
    for i in range(len(population)):
        pop.append(random.sample(range(size), size))

    return pop


def stop(last_values):
    if len(set(last_values)) == 1:
        return True
    return False


if __name__ == '__main__':

    last_best_values = [math.inf]*10000
    best_solution = [math.inf, []]
    apoc_counter = 0
    population = initialize_population(N)

    
    for i in range(max_iterations):
        fitness_values = []
        for indiv in population:
            f = fitness(indiv)
            fitness_values.append(f)
        selected_pop = selection(population, fitness_values)

        new_pop = crossing(selected_pop)

        population = replacement(population, fitness_values, new_pop)

        if best_solution[0]> min(fitness_values):
            best_solution = [min(fitness_values), population[fitness_values.index(min(fitness_values))]]
            print("-------------------")
            print("NEW BEST SOLUTION: (ITER)", i, seed)
            print(best_solution)
            apoc_counter = 0

        apoc_counter += 1


        if apoc_counter == 5000:
            print("APOCALYPSIS EXECUTED")
            population = apocalypsis(population, fitness_values, N)
            apoc_counter = 0
