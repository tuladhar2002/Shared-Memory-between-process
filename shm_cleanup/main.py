import signal
import sysv_ipc
import os
# keys for the shared memory and semaphore
key = 2004
sem_key = 2003
# attach process to the shared memory
shm = sysv_ipc.SharedMemory(key)

# attach semaphore
semaphore = sysv_ipc.Semaphore(sem_key)

# read process id of the writer file
with open("/Users/tuladhar2002/c++_Projects/SharedMemoryDemo/pid.txt","r") as pid_file:
    pid_value = pid_file.readline()
# cast id into int
pid_value = int(pid_value)

# kill writer process
os.kill(pid_value, signal.SIGTERM)

# remove existing semaphore
semaphore.remove()
# detach the process from the memory segment
shm.detach()

# remove the memory segment
sysv_ipc.SharedMemory(key).remove()


# termination
print("Removed the shared memory Segment.")
print()

# check to see whether shared memory segment still exists in os
# noinspection PyBroadException
try:
    shm2 = sysv_ipc.SharedMemory(key)
    data = shm2.read()
    print(data)
except:
    print(f"Shared memory segment with key {key}:Not found")



