from time import time
import numpy as np
import tqdm

class Timer_Decorator:

    min_execution_time = None # atrybuty klasowe
    max_execution_time = None
    av_execution_time = None
    stdev_execution_time = None
    execution_times = [] # pusta tablica na czasy wykonywania funkcji

    def __init__(self, func):
        self.function = func # atrybut instancji klasy 
 
    def __call__(self, *args, **kwargs):
        start_time = time()
        result = self.function(*args, **kwargs)
        end_time = time()
        execution_time = end_time-start_time
        self.execution_times.append(execution_time)
        min_execution_time = min( self.execution_times )
        max_execution_time = max( self.execution_times )
        av_execution_time = np.average( self.execution_times ) 
        stdev_execution_time = np.std( self.execution_times )
        print("Wykonanie zajelo {0:.4f} sekund".format(execution_time))
        print("Minimalny czas wykonania funkcji wynosi {0:.4f} sekund".format(min_execution_time))
        print("Maksymalny czas wykonania funkcji wynosi {0:.4f} sekund".format(max_execution_time))
        print("Sredni czas wykonania funkcji wynosi {0:.4f} sekund".format(av_execution_time))
        print("Odchylenie standardowe czasu wykonania funkcji wynosi {0:.4f} sekund".format(stdev_execution_time))
        return result

@Timer_Decorator # zrodlo: https://www.geeksforgeeks.org/python-program-for-bubble-sort/
def bubblesort(elements):
    swapped = False
    # Looping from size of array from last index[-1] to index [0]
    for n in tqdm.tqdm(range(len(elements)-1, 0, -1)):
        for i in range(n):
            if elements[i] > elements[i + 1]:
                swapped = True
                # swapping data if the element is less than next element in the array
                elements[i], elements[i + 1] = elements[i + 1], elements[i]       
        if not swapped:
            # exiting the function if we didn't make a single swap
            # meaning that the array is already sorted.
            return

for i in range(5):
    test_array = np.random.rand(10000)
    print("Sortowanie losowej tablicy po raz {}.\n".format(i+1))
    bubblesort(test_array)
    print("\n")
