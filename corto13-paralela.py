from multiprocessing import Process, Queue
import random

def worker(sublist, q):
    print(f"Proceso {Process().name} comenzando con sublista de tamaño {len(sublist)}")
    partial_sum = sum(sublist)
    q.put(partial_sum)
    print(f"Proceso {Process().name} ha terminado")

if __name__ == '__main__':
    # Generacion de la lista
    totalElements = 1000000
    numProcess = 4 # Numero de procesos a crear
    data = [random.randint(1, 100) for _ in range(totalElements)]
    
    # Division en sublistas
    chunkSize = totalElements // numProcess
    sublists = [data[i*chunkSize:(i+1)*chunkSize] for i in range(numProcess)]
    
    q = Queue()
    
    # Crear y comenzar los procesos
    processes = []
    
    for i in range(numProcess):
        p = Process(target=worker, args=(sublists[i], q))
        processes.append(p)
        p.start()
        print(f"Proceso {p.name} iniciado")
        
    totalSum = 0
    for _ in range(numProcess):
        totalSum += q.get()
    
    # Esperar a que los procesos terminen    
    for p in processes:
        p.join()
        print(f"Proceso {p.name} ha terminado")
        
    # Verificar el resultado con la suma de un solo hilo
    expected_sum = sum(data)
    print(f"Suma total usando multiprocessing: {totalSum}")
    print(f"Suma total usando la función sum integrada: {expected_sum}")
    print(f"Las sumas coinciden: {totalSum == expected_sum}")