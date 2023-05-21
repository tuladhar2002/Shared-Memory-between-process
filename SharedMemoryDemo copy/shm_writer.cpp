#include <iostream>
#include <semaphore.h>
#include <signal.h>
#include <stdio.h>
#include <sys/ipc.h>
#include <sys/sem.h>
#include <sys/shm.h>
#include <unistd.h>
#include <fstream>

using namespace std;


int main() {
  
  key_t key = 2004;
  key_t sem_key = 2003;

  //get process id inorder for cleanup program to termiate the writer 
  pid_t pid = getpid();
  
  // store pid into a file 

  std::ofstream outfile("pid.txt"); //open
  // write into file
  outfile << pid << std::endl;
  //close file
  outfile.close();

  // Create shared memory and attach to it
  printf("We are about to create sharedmemory\n");
  int shmid = shmget(key, 1024, 0666 | IPC_CREAT);
  int *ptr = (int *)shmat(shmid, NULL, 0);

  // define semaphore
  int sem_id = semget(sem_key, 1, IPC_CREAT | 0666);

  // initialize semaphore value to 1
  semctl(sem_id, 0, SETVAL, 1);

  // deine semaphore acquire release functions
  struct sembuf acquire_op = {0, -1, SEM_UNDO};
  struct sembuf release_op = {0, 1, SEM_UNDO};

  //loop for writing data into the memory segment
  while(true){
    //acquire semaphore
    semop(sem_id, &acquire_op, 1);

    for (int i = 0; i < 33; i++) {

      *ptr = 1002000;
      *(ptr + i) = *ptr + i;
      printf("Data %d: %d\n", i, *(ptr + i));

      usleep(500000);
    }
    // Release semaphore
    semop(sem_id, &release_op, 1);
    // delay for reader to read (the c++ write process too fast)
    usleep(500000);
  }
  

  printf("Detaching from memory");
  
  // detach from shared memory
  shmdt(ptr);
  

  return 0;
}
