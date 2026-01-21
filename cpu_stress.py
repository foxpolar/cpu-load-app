import threading
import time

running = False
threads = []

def burn_cpu():
    while running:
        _ = sum(i*i for i in range(10000))

def start_cpu_load():
    global running, threads
    if not running:
        running = True
        threads = [threading.Thread(target=burn_cpu) for _ in range(8)]
        for t in threads:
            t.start()

def stop_cpu_load():
    global running
    running = False
    for t in threads:
        t.join()