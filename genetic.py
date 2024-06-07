# best distance to target weight: 99


import os
import random as rnd


class Packet:
    def __init__(self, s):
        self.number, self.price, self.weight = s.split(";")
        self.number = int(self.number.split()[1])
        self.price = int(self.price.rstrip("EUR"))
        self.weight = int(self.weight.rstrip("kg\n"))

    def __str__(self):
        return f"Number: {self.number}, Price: {self.price}, Weight: {self.weight}"

 
dir = "/".join(os.path.abspath(__file__).split("\\")[:-1])
content = list(open(dir + "/packets.txt", "r"))
packets = [Packet(e) for e in content]
MAX_WEIGHT = 26_630
mutation_prob = 0.01

class Individuum:
    def __init__(self):
        #self.data = [rnd.randint(0, 1) for i in range(len(packets))]
        self.data = [rnd.choice([0, 0, 0, 0, 0, 0, 0, 0, 1]) for i in range(len(packets))] # otherwise, too many packets with a 1 get created, making the total weight of the Individuum too big

    def fitness(self):
        sum_price = 0
        sum_weight = 0

        for i, p in enumerate(packets):
            if self.data[i] == 1:
                sum_price += p.price
                sum_weight += p.weight

        if sum_weight <= MAX_WEIGHT:
            return sum_price
        else:
            return 0

    def mutate(self):
        for i in range(len(self.data)):
            if rnd.random() < mutation_prob:
                if self.data[i] == 0:
                    self.data[i] = 1
                else:
                    self.data[i] = 0

    def summed_weight(self):
        #w = 0
        #for i in range(len(self.data)):
        #    if self.data[i] == 1:
        #        w += packets[i].weight
        #return w
        return sum([packets[i].weight for i in range(len(self.data)) if self.data[i] == 1])


    def cross(self, other):
        split_point = rnd.randint(0, len(self.data)-2)

        self_part_one = self.data[:split_point]
        self_part_two = self.data[split_point:]
        other_part_one = other.data[:split_point]
        other_part_two = other.data[split_point:]

        self_part_one.extend(other_part_two) # self
        other_part_one.extend(self_part_two) # other

        ind1 = Individuum()
        ind1.data = self_part_one
        ind2 = Individuum()
        ind2.data = other_part_one

        return ind1, ind2


class Population:
    def __init__(self, amt):
        self.population = [Individuum() for i in range(amt)]

    def get_candidates(self):
        return rnd.choice(self.population), rnd.choice(self.population) # get two random parent Individuums

    def evolve(self):
        evolve_done = False
        evolve_count = 0

        while not evolve_done:
            # first competition -> first parent
            p1, p2 = self.get_candidates()

            p1_index = self.population.index(p1)
            p2_index = self.population.index(p2)

            f1 = p1.fitness()
            f2 = p2.fitness()

            if f1 >= f2:
                winner1 = p1
                winner1_index = p1_index
            else:
                winner1 = p2
                winner1_index = p2_index

            # second competition -> second parent
            p3, p4 = self.get_candidates()

            p3_index = self.population.index(p3)
            p4_index = self.population.index(p4)

            f3 = p3.fitness()
            f4 = p4.fitness()

            if f3 >= f4:
                winner2 = p3
                winner2_index = p3_index
            else:
                winner2 = p4
                winner2_index = p4_index

            
            # creating children from parents
            child1, child2 = winner1.cross(winner2)

            child1.mutate()
            child2.mutate()

            self.population[winner1_index] = child1
            self.population[winner2_index] = child2

            evolve_count += 1
            
            if evolve_count%1000 == 0:
                print(evolve_count)

            if evolve_count == len(self.population):
                evolve_done = True


        # get best Individuum
        max_fitness = 0
        max_indiv = Individuum()
        for e in self.population:
            f = e.fitness()
            if f > max_fitness:
                max_fitness = f
                max_indiv = e

        print(f"Distance to target weight: {MAX_WEIGHT - max_indiv.summed_weight()}")
        return max_indiv, max_fitness


p = Population(10000)
ind, fit = p.evolve()
print(ind.data, fit)