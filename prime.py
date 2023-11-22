#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Kocaeli University
    Arsene Adjevi(235172001)
    Innovative Approaches in Computer Architectures(Exam report)

"""
import multiprocessing
from math import isqrt
from timeit import timeit
from concurrent.futures import ThreadPoolExecutor
#import matplotlib.pyplot as plt
import time




def is_prime_sequential(number):
    if number <= 1:
        return False
    for i in range(2, isqrt(number) + 1):
        if number % i == 0:
            return False
    return True

def is_prime_parallel_util(args):
    number, start, end = args
    for i in range(start, end):
        if number % i == 0:
            return False
    return True

def is_prime_parallel(number, processes):
    sqrt_num = isqrt(number) + 1
    chunk_size = (sqrt_num - 2) // processes + 1
    
    # Create a pool of processes
    with multiprocessing.Pool(processes=processes) as pool:
        # Divide the range of numbers to check among processes
        chunks = [(number, i, min(i + chunk_size, sqrt_num)) for i in range(2, sqrt_num, chunk_size)]
        
        # Map the chunks to processes
        results = pool.map(is_prime_parallel_util, chunks)
    
    # Check if all chunks returned True (indicating the number is prime)
    return all(results)

def is_prime_threaded(number, threads):
    sqrt_num = isqrt(number) + 1
    chunk_size = (sqrt_num - 2) // threads + 1
    
    # Create a pool of threads
    with ThreadPoolExecutor(max_workers=threads) as executor:
        # Divide the range of numbers to check among threads
        chunks = [(number, i, min(i + chunk_size, sqrt_num)) for i in range(2, sqrt_num, chunk_size)]
        
        # Map the chunks to threads
        futures = [executor.submit(is_prime_parallel_util, chunk) for chunk in chunks]
    
    # Check if all threads returned True (indicating the number is prime)
    return all(future.result() for future in futures)


if __name__ == "__main__":
    number_to_check =  1289237867378231  # Replace with your desired number
    processes = multiprocessing.cpu_count()  # Adjust the number of processes as needed. the max cpu core for this computer is 16. get it with os.cpu_count() or multiprocessing.cpu_count()
    threads = 5
    iterations = 5

    #test output result
    assert is_prime_sequential(number_to_check) == True
    assert is_prime_parallel(number_to_check,processes) == True
    assert is_prime_threaded(number_to_check,threads) == True

    # Sequential version Timing
    total_time_linear = timeit("is_prime_sequential(number_to_check)",number= iterations,globals=globals())
    print(f"Sequential function took  {total_time_linear/iterations} seconds")
    
    # Parallel version
    total_time_parallel = timeit("is_prime_parallel(number_to_check,processes)",number= iterations,globals=globals())
    print(f"Parallel function  took {total_time_parallel/iterations} seconds")
    # Parallel version
    total_time_threaded = timeit("is_prime_threaded(number_to_check, threads)",number= iterations,globals=globals())
    print(f"Multitreaded  function took {total_time_threaded/iterations} seconds")

    #Speedup
    speed_up = total_time_linear/total_time_parallel
    print(f"SpeedUp:{speed_up}")
    #Efficiency
    efficiency = speed_up / processes
    print(f"Efficiency:{efficiency}")

    #ploting
    cores = list(range(1,processes+1))
    times       = []
    speed_up    = []
    efficiency  = []

    for core in cores:
        start_time_pa = time.perf_counter()
        is_prime_parallel(number_to_check,core)
        end_time_pa = time.perf_counter()
        times.append(end_time_pa - start_time_pa)
        #linear function 
        start_time_sq = time.perf_counter()
        is_prime_sequential(number_to_check)
        end_time_sq = time.perf_counter()
        speed = (end_time_sq - start_time_sq)/(end_time_pa - start_time_pa)
        speed_up.append(speed)
        efficiency.append(speed/core)

  #  plt.plot(cores,times)
  #  plt.title("Running Time vs Processors")
  #  plt.xlabel("Processors, K")
  #  plt.ylabel("Times(seconds)")
  #  plt.show()

  #  plt.plot(cores,speed_up)
  #  plt.title("SpeedUp vs Processors")
  #  plt.xlabel("Processor, K")
  #  plt.ylabel("SpeedUp")
  #  plt.show()


  #  plt.plot(cores,efficiency)
  #  plt.title("Efficiency vs Processors")
  #  plt.xlabel("Processor, K")
  #  plt.ylabel("Efficiency")
  #  plt.show()
