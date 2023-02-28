import simpy
import random
import numpy as np

#Global value
START_TIMES = []
END_TIMES = []

#def CPUProc_Generator(env, Qty, Interval, RAM, CPUs, InstrP_S):

#    for i in range(1 , Qty + 1):
 #       yield  env.timeout(random.expovariate(1.0/Interval))
  #      random_Inst = random.randint(1, 10)
   #     random_Mem = random.randint(1, 10)
#
 #       print("%s creado en %.1f con memoria de %i con %i instrucciones" % ("Proceso %d" % i, env.now,random_Mem, random_Inst))
  #      START_TIMES.append(round(env.now, 1))
#
 #       if(RAM.level - random_Mem >= 0):
  #          yield RAM.get(random_Mem)
   #         env.process(CpuProcessReady(env, "Proceso %d" % i, random_Mem, random_Inst, RAM, CPUs, InstrP_S))

#        else:
 #           print("Memoria insuficiente para el %s, agregado a la lista de espera en %.1f" % ("Proceso %d" % i, env.now))
  #          env.process(ProcessWaitingforRam(env, "Proceso %d" % i, random_Mem, random_Inst, RAM, CPUs, InstrP_S) )


#def CpuProcessReady(env, name, memory, Instructions, RAM, CPUs, InstrP_S):
 #  print("%s ha pasado a la ram y esta listo para ejecutarse en %.1f" % (name, env.now))
  # with CPUs.request() as req:
   #    yield req
    #   env.process(ProcessRunning(env, name, memory, Instructions, RAM, CPUs, req, InstrP_S))

#def ProcessRunning(env, name, memory, Instructions, RAM, CPUs, req, InstrP_S):
    
 #   Instructions = Instructions - InstrP_S

  #  if(Instructions <= 0 ):
   #     yield env.timeout(InstrP_S)
    #    print("%s terminado en %.1f" % (name, env.now))
     #   END_TIMES.append(round(env.now, 1))
      #  yield RAM.put(memory)
        
        
  #  else:
   #     rand_Status = random.randint(1, 2)

    #    if(rand_Status == 2):
     #       print("%s ejecutado, ahora tiene %d instrucciones y regresa directamente a la cola de procesos en %d" % (name, Instructions, env.now))        
      #      CPUs.release(req)
       #     yield env.process(CpuProcessReady(env, name, memory, Instructions, RAM, CPUs, InstrP_S))
        
        #elif(rand_Status == 1):
        #     CPUs.release(req)
         #    print("%s ejecutado y puesto en espera, ahora tiene %d instrucciones y regresa a la cola waiting en %d" % (name, Instructions, env.now))        
          #   yield env.timeout(3)
           #  
            # print("%s sale de la cola de espera, ahora tiene %d instrucciones y regresa a la cola de procesos en %d" % (name, Instructions, env.now))        
             #yield env.process(CpuProcessReady(env, name, memory, Instructions, RAM, CPUs, InstrP_S))


#def ProcessWaitingforRam (env, name, memory, Instructions, RAM, CPUs, InstrP_S):
 #   if(RAM.level - memory >= 0):
  #      print("Memoria disponible, Ingresando %s en %d" % (name, env.now))
   #     env.process(CpuProcessReady(env, name, memory, Instructions, RAM, CPUs , InstrP_S))
    
    #else:
     #   print("%s esperando por espacio de ram en %d" % (name , env.now))
      #  yield env.timeout(2) #Check every cicle for available memory
        

#########################################################################################################
print("Bienvenido al simulador de procesos en un CPU, por favor ingrese los siguientes datos")

RANDOM_SEED = 42
ProcessesQty = int(input("Cuantos procesos se desean crear para la simulacion\n"))
RAMSpace = int(input("Cuanto espacio de RAM estara disponible\n"))
InstrP_S = int(input("Que tan rapido sera el procesador (Cuantas instrucciones podra hacer por segundo)\n"))
ProccesorsQty = int(input("Cuantos procesadores se usaran\n"))
Interval = int(input("Cual sera el intervalo para la creacion de procesos\n"))

print(ProcessesQty)
print(RAMSpace)
print(InstrP_S)
print(ProccesorsQty)
print(Interval)

random.seed(RANDOM_SEED)

env = simpy.Environment()
RAM = simpy.Container(env, init = RAMSpace, capacity = RAMSpace)  
CPUs = simpy.Resource(env, capacity = ProccesorsQty)

env.process(CPUProc_Generator(env, ProcessesQty, Interval, RAM, CPUs, InstrP_S))
env.run()

print(f"Tiempos inicio: {START_TIMES}")
print(f"Tiempos Salida: {END_TIMES}")

RUN_TIMES = []

print(len(START_TIMES))
print(len(END_TIMES))

for i in range (len(START_TIMES)):
   RUN_TIMES.append(round(END_TIMES[i] - START_TIMES[i], 1))

print(RUN_TIMES)

print("Tiempo promedio de los procesos hasta salir: %d " % np.average(RUN_TIMES))

print("Desviacion estandar de los tiempos de los procesos: %d" % np.std(RUN_TIMES))
