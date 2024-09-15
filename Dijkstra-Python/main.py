import threading
import random

# Constantes
N = 5  # Número de filósofos
THINKING = 0
HUNGRY = 1
EATING = 2
EAT_TIMES = 3  # Número de vezes que cada filósofo vai comer

# Funções para cálculo dos vizinhos à esquerda e à direita
def LEFT(i):
    return (i + N - 1) % N

def RIGHT(i):
    return (i + 1) % N

# Estado de cada filósofo
state = [THINKING] * N
eat_count = [0] * N  # Número de refeições de cada filósofo

# Semáforos e mutex
semaphores = [threading.Semaphore(0) for _ in range(N)]
mutex = threading.Lock()

# Função que simula pensar sem bloquear
def think(i):
    print(f"Filósofo {i} está pensando.")
    # Fazer algo produtivo ou simulado aqui sem pausar a execução
    # Por exemplo, um cálculo, ou simplesmente esperar por outro evento ou entrada

# Função que simula comer sem bloquear
def eat(i):
    print(f"Filósofo {i} está comendo.")
    # Em vez de "sleep", poderíamos registrar um evento que simula comer
    # Ou realizar operações não bloqueantes aqui
    eat_count[i] += 1

# Função que verifica se o filósofo pode comer
def check(i):
    if state[i] == HUNGRY and state[LEFT(i)] != EATING and state[RIGHT(i)] != EATING:
        state[i] = EATING
        semaphores[i].release()

# Função para o filósofo pegar os garfos
def take_forks(i):
    with mutex:
        state[i] = HUNGRY
        print(f"Filósofo {i} está com fome.")
        check(i)
    semaphores[i].acquire()

# Função para o filósofo colocar os garfos de volta
def put_forks(i):
    with mutex:
        state[i] = THINKING
        check(LEFT(i))
        check(RIGHT(i))

# Rotina principal do filósofo
def philosopher_routine(i):
    while eat_count[i] < EAT_TIMES:
        think(i)  # Simula pensar
        take_forks(i)  # Tenta pegar os garfos
        eat(i)  # Simula comer
        put_forks(i)  # Devolve os garfos
    print(f"Filósofo {i} terminou de comer.")

# Inicializando as threads para os filósofos
def main():
    threads = []
    for i in range(N):
        t = threading.Thread(target=philosopher_routine, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()  # Espera que todas as threads terminem

    print("Todos os filósofos terminaram de comer.")

if __name__ == "__main__":
    main()
