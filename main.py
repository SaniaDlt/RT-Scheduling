from threading import Semaphore


def runner(semaphore:Semaphore):
    semaphore.release()

