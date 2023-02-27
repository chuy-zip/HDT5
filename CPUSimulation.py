import simpy
import random

def ProcessRunning(env, name, memory, Instructions, RAM, CPUs, req):
    
    Instructions = Instructions - 3

    if(Instructions <= 0 ):
        Instructions = 0
        RAM.put(memory)
        print("%s terminado en %.1f" % (name, env.now))
    
    else:

        rand_Status = random.randint(1, 2)

        if(rand_Status == 2):
            print("%s ejecutado, ahora tiene %d instrucciones y regresa directamente a la cola de procesos en %d" % (name, Instructions, env.now))        
            CPUs.release(req)
            yield env.process(CpuProcessReady(env, name, memory, Instructions, RAM, CPUs))
        
        elif(rand_Status == 1):
             CPUs.release(req)
             print("%s ejecutado y puesto en espera, ahora tiene %d instrucciones y regresa a la cola waiting en %d" % (name, Instructions, env.now))        
             yield env.timeout(3)
             
             print("%s sale de la cola de espera, ahora tiene %d instrucciones y regresa a la cola de procesos en %d" % (name, Instructions, env.now))        
             yield env.process(CpuProcessReady(env, name, memory, Instructions, RAM, CPUs))

def CpuProcessReady(env, name, memory, Instructions, RAM, CPUs):
   print("%s ha pasado a la ram y esta listo para ejecutarse en %.1f" % (name, env.now))
   with CPUs.request() as req:
       yield req

       yield env.process(ProcessRunning(env, name, memory, Instructions, RAM, CPUs, req))

def CPUProc_Generator(env, Qty, Interval, RAM, CPUs):

    for i in range(1 , Qty + 1):
        random_Inst = random.randint(1, 10)
        random_Mem = random.randint(1, 10)
        print("%s creado en %.1f con memoria de %i con %i instrucciones" % ("Proceso %d" % i, env.now,random_Mem, random_Inst))
        yield  env.timeout(random.expovariate(1.0/Interval))

        if(RAM.level - random_Mem >= 0):

            RAM.get(random_Mem)
            env.process(CpuProcessReady(env, "Proceso %d" % i, random_Mem, random_Inst, RAM, CPUs))
        else:
            print("Memoria insuficiente para el %s, agregado a la lista de espera en %.1f" % ("Proceso %d" % i, env.now))
            env.process(ProcessWaitingforRam(env, "Proceso %d" % i, random_Mem, random_Inst, RAM, CPUs) )

def ProcessWaitingforRam (env, name, memory, Instructions, RAM, CPUs):
    if(RAM.level - memory >= 0):
        print("Memoria disponible, Ingresando %s en %d" % (name, env.now))
        yield env.process(CpuProcessReady(env, name, memory, Instructions, RAM, CPUs))
    
    else:
        print("%s esperando por espacio de ram en %d" % (name , env.now))
        yield env.timeout(1) #Check every cicle for available memory
        yield env.process(ProcessWaitingforRam (env, name, memory, Instructions, RAM, CPUs))

#########################################################################################################
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

env.process(CPUProc_Generator(env, ProcessesQty, Interval, RAM, CPUs))
env.run()

# Pendiente
# Hacer que sea dinamico con, el numero de instrucciones por segundo
# Ver promedios y desviacion estandar
#
#
#
