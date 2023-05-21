import sysv_ipc
import time

# Create key for shared memory and semaphores
key = 2004
sem_key = 2003

# create shared memory segment
shmmem = sysv_ipc.SharedMemory(key)

# create semaphore to synchronize access to shared memory
semaphore = sysv_ipc.Semaphore(sem_key)

# lists of read values from the shared memory
List = []

# Loop to read data from shared memory
while True:
    # semaphore acquire
    semaphore.acquire()

    # Read data from shared memory
    data = shmmem.read(1024)

    # Print data
    values = data.split(b"\0")
    for value in values:
        if value != b"":
            List.append(int.from_bytes(value, byteorder="little"))
    print("Read Data: {}".format(List))
    List.clear()

    # sleep for testing synchronization conditions
    # time.sleep(4)

    # Release write semaphore
    semaphore.release()

    # 1 sec delay for reader to read (the c++ write process too fast)
    time.sleep(1)

# detach if needed
# shmmem.detach()
