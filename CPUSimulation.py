import simpy
import random

def CpuProcess(env, name, memory, Instructions):
    print("%s creado en %.1f con memoria de %i con %i instrucciones" % (name, env.now, memory, Instructions))
    

def CPUProc_Generator(env, Qty, Interval):
    for i in range(1 , Qty + 1):
        yield  env.timeout(random.expovariate(1.0/Interval))
        random_Inst = random.randint(1, 10)
        random_Mem = random.randint(1, 10)
        print("%s creado en %.1f con memoria de %i con %i instrucciones" % ("Proceso %d" % i, env.now,random_Mem, random_Inst))
    
        #env.process(CpuProcess(env, "Proceso %d" % i, random_Mem, random_Inst) )  

print("Bienvenido al simulador de procesos en un CPU, por favor ingrese los siguientes datos")

RANDOM_SEED = 42
ProcessesQty = int(input("Cuantos procesos se desean crear para la simulacion\n"))
RAMSpace = int(input("Cuanto espacio de RAM estara disponible\n"))
InstructionsPerSecond = int(input("Que tan rapido sera el procesador (Cuantas instrucciones podra hacer por segundo)\n"))
ProccesorsQty = int(input("Cuantos procesadores se usaran\n"))
Interval = int(input("Cual sera el intervalo para la creacion de procesos\n"))

print(ProccesorsQty)
print(RAMSpace)
print(InstructionsPerSecond)
print(ProccesorsQty)
print(Interval)

random.seed(RANDOM_SEED)

env = simpy.Environment()
RAM = simpy.Container(env, init = RAMSpace, capacity = RAMSpace)  
CPUs = simpy.Resource(env, capacity = ProccesorsQty)

env.process(CPUProc_Generator(env, ProcessesQty, Interval))
env.run(10000)
