import math, random

activate_functions = [
    lambda x : x, 
    lambda x : max(0, x),
    lambda x : 1 / (1 + pow(math.e, -x)),
]

class Neural:
    def __init__(self, bias = 0, function = 0):
        self.bias = bias
        self.function = function
        self.out = None

class Node:
    def __init__(self, type_, id_):
        self.type = type_
        self.id = id_

    def __eq__(self, other):
        return self.type == other.type and self.id == other.id

    def __repr__(self):
        return f"Node<type:{self.type}, id:{self.id}>"

class Connexion:
    def __init__(self, node_in, node_out, weight = 1):
        self.input = node_in
        self.output = node_out
        self.weight = weight

    def __eq__(self, other):
        return self.input == other.input and self.output == other.output and self.weight == other.weight
    
class Network:
    def __init__(self, n_inputs, n_outputs, connexions = list(), hiddens = list()):
        self.inputs = [Neural() for i in range(n_inputs)]        
        self.outputs = [Neural() for i in range(n_outputs)]
        self.hiddens = hiddens.copy()
        self.connexions = connexions.copy()

    def copy(self):
        netcopy = Network(len(self.inputs), len(self.outputs), self.connexions, self.hiddens)
        netcopy.inputs = self.inputs.copy()
        netcopy.outputs = self.outputs.copy()
        return netcopy
    
    def reset(self):
        for input_ in self.inputs:
            input_.out = None
        for hidden in self.hiddens:
            hidden[1].out = None
        for output in self.outputs:
            output.out = None
            
    def process(self, node):
        neural = self.get_neural(node)
        if neural.out is not None:
            return neural.out

        output = neural.bias

        connexions = self.get_in_connexions(node)
        for connexion in connexions:
            output += connexion.weight * self.process(connexion.input)

        return output

    def get_neural(self, node):
        if node.type == "input":
            return self.inputs[node.id]
        if node.type == "output":
            return self.outputs[node.id]
        if node.type == "hidden":
            for hidden in self.hiddens:
                if hidden[0] == node.id:
                    return hidden[1]

            raise RuntimeError(f"Didn't find the hidden neural of id {node.id}!")
        else:
            raise RuntimeError(f"There is no node of type {node.type}!") 

    def get_in_connexions(self, node):
        connexions = list()
        for connexion in self.connexions:
            if connexion.output.type == node.type and connexion.output.id == node.id:
                connexions.append(connexion)

        return connexions

    def get_out_connexions(self, node):
        connexions = list()
        for connexion in self.connexions:
            if connexion.input.type == node.type and connexion.input.id == node.id:
                connexions.append(connexion)
                
        return connexions

    def add_bias(self, _range):
        neural_index = random.randint(0, len(self.inputs) + len(self.hiddens) + len(self.outputs) - 1)
        num = random.uniform(-_range, _range)
        if neural_index < len(self.inputs):
            self.inputs[neural_index].bias += num
        elif neural_index < len(self.inputs) + len(self.hiddens):
            self.hiddens[neural_index - len(self.inputs)][1].bias += num
        else:
            self.outputs[neural_index - len(self.inputs) - len(self.hiddens)].bias += num    
        
    def add_weight(self, _range):
        connexion_index = random.randint(0, len(self.connexions) - 1)
        num = random.uniform(-_range, _range)
        self.connexions[connexion_index].weight += num

    def change_function(self):
        neural_index = random.randint(0, len(self.hiddens) + len(self.outputs) - 1)
        function_id = random.randint(0, len(activate_functions))
        if neural_index < len(self.hiddens):
            self.hiddens[neural_index][1].function  = function_id
        else:
            self.outputs[neural_index - len(self.hiddens)].function = function_id

    def add_neural(self, bias_range, weight_range):
        index = -1
        for i in range(0, 100):
            for _id, neural in self.hiddens:
                if _id == i:
                    break
            else:
                index = i
                break

        neural = Neural(random.uniform(-bias_range, bias_range), random.randint(0, len(activate_functions)-1))
        self.hiddens.append((index, neural))
        self.connexions.append(Connexion(Node("input", random.randint(0, len(self.inputs)-1)), Node("hidden", index), random.uniform(-weight_range, weight_range)))
        self.connexions.append(Connexion(Node("hidden", index), Node("output", random.randint(0, len(self.outputs)-1)), random.uniform(-weight_range, weight_range)))

    def add_connexion(self, weight_range):
        num = random.uniform(-weight_range, weight_range)

        neural_index = random.randint(0, len(self.inputs) + len(self.hiddens) -1)
        first_node = None
        if neural_index < len(self.inputs):
            first_node = Node("input", neural_index)
        else:
            first_node = Node("hidden", neural_index - len(self.inputs))

        neural_index = random.randint(0, len(self.outputs) + len(self.hiddens) -1)
        second_node = None
        if neural_index < len(self.outputs):
            second_node = Node("output", neural_index)
        else:
            second_node = Node("hidden", neural_index - len(self.outputs))

        connexion = Connexion(first_node, second_node, num)
        self.connexions.append(connexion)
        if not self.validate_connexion(self.connexions[-1]):
            self.connexions = self.connexions[:-1]
        
    def validate_connexion(self, connexion, lenght = 0):
        if lenght > 10:
            return False

        connexions = self.get_in_connexions(connexion.output)
        for con in connexions:
            if not self.validate_connexion(con, lenght + 1):
                return False

        return True

    def remove_connexion(self):
        index = random.randint(0, len(self.connexions)-1)
        connexion = self.connexions[index]
        if len(self.get_out_connexions(connexion.input)) > 1 and len(self.get_in_connexions(connexion.output)) > 1:
            self.connexions.pop(index)

    def remove_neural(self):
        if len(self.hiddens) == 0:
            return
        
        index = random.randint(0, len(self.hiddens)-1)
        node = Node("hidden", self.hiddens[index][0])
        in_connexions = self.get_in_connexions(node)
        out_connexions = self.get_out_connexions(node)

        for connexion in in_connexions:
            if len(self.get_out_connexions(connexion.input)) == 1:
                return
        for connexion in out_connexions:
            if len(self.get_in_connexions(connexion.output)) == 1:
                return
      
    def low_mutation(self):
        if random.uniform(0, 1) <= 0.70:
            self.add_bias(0.1)
        if random.uniform(0, 1) <= 0.70:
            self.add_weight(0.05)
        if random.uniform(0, 1) <= 0.10:
            self.change_function()
    
    def medium_mutation(self):
        if random.uniform(0, 1) <= 0.08:
            self.add_neural(0.5, 1)
        if random.uniform(0, 1) <= 0.15:
            self.add_connexion(1)
        if random.uniform(0, 1) <= 0.15:
            self.add_bias(0.4)
        if random.uniform(0, 1) <= 0.15:
            self.add_weight(0.2)
        if random.uniform(0, 1) <= 0.05:
            self.change_function()
        
    def high_mutation(self):
        if random.uniform(0, 1) <= 0.02:
            self.remove_connexion()
        if random.uniform(0, 1) <= 0.005:
            self.remove_neural()
        if random.uniform(0, 1) <= 0.12:
            self.add_neural(1.3, 1.5)
        if random.uniform(0, 1) <= 0.20:
            self.add_connexion(1.5)
        if random.uniform(0, 1) <= 0.10:
            self.add_bias(1)
        if random.uniform(0, 1) <= 0.10:
            self.add_weight(0.6)
        if random.uniform(0, 1) <= 0.07:
            self.change_function()

class Population:
    def __init__(self, base_network, fitness, n_individuals, lmr, mmr, hmr):
        self.network = base_network
        self.best_network = base_network
        self.best_fitness = fitness

        self.current_network = None
        self.current_fitness = 0
        self.max = n_individuals
        self.count = 1
        
        total = lmr + mmr + hmr
        self.low_rate = lmr / total
        self.medium_rate = mmr / total
        self.high_rate = hmr / total

    def generate_network(self):
        prob = random.uniform(0, 1)
        self.current_network = self.network.copy()
        
        if prob <= self.low_rate:
            self.current_network.low_mutation()
        elif prob <= self.low_rate + self.medium_rate:
            self.current_network.medium_mutation()
        else:
            self.current_network.high_mutation()
            
    def get_network(self):
        if self.current_network is None:
            self.generate_network()

        return self.current_network

    def next_network(self):
        if self.current_fitness >= self.best_fitness:
            self.best_fitness = self.current_fitness
            self.best_network = self.current_network.copy()

        self.current_network = None
        self.current_fitness = 0

        self.count += 1
        if self.count == self.max:
            return False
        return True
    
