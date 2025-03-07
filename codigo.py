import numpy as np
import matplotlib.pyplot as plt
import random

# Definição dos estados 
SUSCEPTIBLE = 0
EXPOSED = 1
INFECTED = 2
RECOVERED = 3

# Função para inicializar a grade com valores aleatórios
def initialize_grid(size, infection_prob, exposed_prob):
    grid = np.zeros((size, size), dtype=int) 
    for i in range(size):
        for j in range(size):
            if random.random() < infection_prob:
                grid[i, j] = INFECTED 
            elif random.random() < exposed_prob:
                grid[i, j] = EXPOSED  
            else:
                grid[i, j] = SUSCEPTIBLE  
    return grid

# Função para visualizar a grade
def plot_grid(grid):
    plt.imshow(grid, cmap='viridis', interpolation='nearest')
    plt.colorbar(label='Estado')
    plt.show()

# Função para simular a propagação da infecção baseado em Self-Replicating Machines
def simulate_step_self_replication(grid, infection_rate, incubation_rate, recovery_rate):
    size = len(grid)
    new_grid = np.copy(grid)

    # Iterando sobre a grade e aplicando as regras de transição com auto-replicação
    for i in range(size):
        for j in range(size):
            # Se a célula está infectada, tenta replicar sua infecção nos vizinhos
            if grid[i, j] == INFECTED:
                # Vizinhos (direção 4: acima, abaixo, esquerda, direita)
                for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ni, nj = (i + di) % size, (j + dj) % size  # Arredondamento para garantir periodicidade
                    if grid[ni, nj] == SUSCEPTIBLE and random.random() < infection_rate:
                        new_grid[ni, nj] = EXPOSED  # Célula suscetível se torna exposta, replicação da infecção

            
            elif grid[i, j] == EXPOSED:
                if random.random() < incubation_rate:
                    new_grid[i, j] = INFECTED  # Exposto se torna infectado

            elif grid[i, j] == INFECTED:
                if random.random() < recovery_rate:
                    new_grid[i, j] = RECOVERED  # Infectado se recupera

    return new_grid

# Função para contar os estados na grade
def count_states(grid):
    unique, counts = np.unique(grid, return_counts=True)
    return dict(zip(unique, counts))

# Parâmetros do modelo
grid_size = 50  
infection_prob = 0.05  
exposed_prob = 0.02 
infection_rate = 0.1  
incubation_rate = 0.05  
recovery_rate = 0.01 


grid = initialize_grid(grid_size, infection_prob, exposed_prob)

# Variáveis para armazenar a evolução dos estados ao longo do tempo
susceptible_history = []
exposed_history = []
infected_history = []
recovered_history = []

# Simulação 
for step in range(25):  
    plot_grid(grid)  
    grid = simulate_step_self_replication(grid, infection_rate, incubation_rate, recovery_rate)  # Atualiza a grade

   
    state_counts = count_states(grid)
    susceptible_history.append(state_counts.get(SUSCEPTIBLE, 0))
    exposed_history.append(state_counts.get(EXPOSED, 0))
    infected_history.append(state_counts.get(INFECTED, 0))
    recovered_history.append(state_counts.get(RECOVERED, 0))

# Plotando o gráfico de evolução dos estados ao longo do tempo
plt.figure(figsize=(10, 6))
plt.plot(susceptible_history, label="Suscetíveis", color="yellow")
plt.plot(exposed_history, label="Expostos", color="green")
plt.plot(infected_history, label="Infectados", color="purple")
plt.plot(recovered_history, label="Recuperados", color="blue")
plt.xlabel("Passos de Simulação")
plt.ylabel("Número de Células")
plt.legend()
plt.title("Evolução dos Estados da Epidemia ao Longo do Tempo")
plt.show()
