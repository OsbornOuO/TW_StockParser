import threading


def job2(a):
    global lock
    while True:
        lock.acquire()
        if len(a) <= 0:
            lock.release()
            break
        print(a.pop())
        lock.release()


if __name__ == '__main__':
    A = [1, 2, 3, 4, 5]
    lock = threading.Lock()
    t1 = threading.Thread(target=job2, args=(A,))
    t2 = threading.Thread(target=job2, args=(A,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
