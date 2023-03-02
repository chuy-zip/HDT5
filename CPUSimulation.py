#Ricardo Chuy 221007 Hoja de trabajo 5 
import simpy
import random
import numpy as np

#Global value
START_TIMES = []
END_TIMES = []
CRUN_TIME = []

def CpuProcessReady(env, name, memory, Instructions, RAM, InstrP_S,tempInterval):
   yield env.timeout(tempInterval) #Interval for creation of process
   print("%s creado en %.1f con memoria de %i con %i instrucciones" % ("Proceso %d" % i, env.now,random_Mem, random_Inst))

   print("%s ha pasado a la ram y esta listo para ejecutarse en %.1f" % (name, env.now))
   start = round(env.now, 1)

   yield RAM.get(memory) #Waiting for available ram
   ##Queue for Cpu proceseses, it while only execute once the processor is free
   
   while Instructions > 0:  #While the process still has instructions
        with CPUs.request() as req: 
            yield req  #request cpu
       
            Instructions = Instructions - InstrP_S
            
            if(Instructions <= 0 ): #Free process if tehere are no more instructions
                yield env.timeout(1)
                print("%s terminado en %.1f" % (name, env.now))
                end = round(env.now, 1)
                CRUN_TIME.append(round(end - start, 1))

                yield RAM.put(memory)
                
            else:
                rand_Status = random.randint(1, 2)

                if(rand_Status == 2):
                    CPUs.release(req)
                    yield env.timeout(1)
                    print("%s ejecutado, ahora tiene %d instrucciones y regresa directamente a la cola de procesos en %d" % (name, Instructions, env.now))        
                
                elif(rand_Status == 1):
                    CPUs.release(req)
                    print("%s ejecutado y puesto en espera, ahora tiene %d instrucciones y regresa a la cola waiting en %d" % (name, Instructions, env.now))                                
                    yield env.timeout(4)
                    print("%s sale de la cola de espera, ahora tiene %d instrucciones y regresa a la cola de procesos en %d" % (name, Instructions, env.now))        

print("Bienvenido al simulador de procesos en un CPU, por favor ingrese los siguientes datos")

RANDOM_SEED = 42
ProcessesQty = int(input("Cuantos procesos se desean crear para la simulacion\n"))
RAMSpace = int(input("Cuanto espacio de RAM estara disponible\n"))
InstrP_S = int(input("Que tan rapido sera el procesador (Cuantas instrucciones podra hacer por segundo)\n"))
ProccesorsQty = int(input("Cuantos procesadores se usaran\n"))
Interval = int(input("Cual sera el intervalo para la creacion de procesos\n"))

print()
print(ProcessesQty)
print(RAMSpace)
print(InstrP_S)
print(ProccesorsQty)
print(Interval)

random.seed(RANDOM_SEED)

env = simpy.Environment()
RAM = simpy.Container(env, init = RAMSpace, capacity = RAMSpace)  
CPUs = simpy.Resource(env, capacity = ProccesorsQty)

for i in range(ProcessesQty):
    tempInterval = (random.expovariate(1/Interval))
    random_Inst = random.randint(1, 10)
    random_Mem = random.randint(1, 10)
    #Creating process with interval
    env.process(CpuProcessReady(env, "Proceso %d" % i, random_Mem, random_Inst, RAM, InstrP_S,tempInterval))

env.run()

print("Tiempos de ejecuacion de cada proceso: ")

print(CRUN_TIME)

print("Tiempo promedio de los procesos hasta salir nuevo: %d " % np.average(CRUN_TIME))

print("Desviacion estandar de los tiempos de los procesos nuevo: %d" % np.std(CRUN_TIME))