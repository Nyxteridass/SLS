# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 19:37:17 2024

@author: chris
"""
from queue import PriorityQueue
import random
import sys


round_robin_queue = []
completed_processes = []
global currecurrent_time
global total_response_time
global total_turnaround_time

#current_time = 0
total_response_time = 0
total_turnaround_time = 0

class Process:
    def __init__(self, name, arrival_time, duration, priority):
        self.name = name
        self.arrival_time = arrival_time
        self.duration = duration
        self.priority = priority
        self.response_time = -1
        self.turnaround_time = -1

def create_random_processes():
    processes = []
    num_processes= random.randint(1,10)
    print(f"Nr of processes: {num_processes}")
    for i in range(num_processes):
        name = f"P{i + 1}"
        arrival_time = random.randint(0, 10)  # Adjust range based on your scenario
        duration = random.randint(1, 10)
        priority = random.randint(1, 8)
        processes.append(Process(name, arrival_time, duration, priority))
        print(f"P{i + 1}",f"arrival time :{arrival_time}",f"duration :{duration}", f"priority :{priority}")
    return processes



def calc_avgs(completed_processes):
    avg_response_time = sum(process.response_time - process.arrival_time for process in completed_processes) / len(completed_processes)
    avg_turnaround_time = sum(process.turnaround_time for process in completed_processes) / len(completed_processes)

    print("\nProcess\tResponse Time\tTurnaround Time")
    for process in completed_processes:
        print(f"\t{process.name}\t\t\t{process.response_time}\t\t\t\t{process.turnaround_time}")
    else:
        print("\nNo processes to display.")
    print(f"\nAverage Response Time: {avg_response_time:.2f}")
    print(f"Average Turnaround Time: {avg_turnaround_time:.2f}")
    
def scan_queues(current_process, current_time, time_quantum, total_response_time,total_turnaround_time):
    
    if current_process.response_time == -1:
        current_process.response_time = current_time

    if current_process.duration <= time_quantum:
        current_time += current_process.duration
        current_process.turnaround_time = current_time - current_process.arrival_time
        total_response_time += current_process.response_time - current_process.arrival_time
        total_turnaround_time += current_process.turnaround_time
        print(f"to {current_time} (Completed)")
        completed_processes.append(current_process)
    else:
        current_time += time_quantum
        current_process.duration -= time_quantum
        print(f"to {current_time} (Remaining time: {current_process.duration})")
        round_robin_queue.append(current_process)
    return current_process,current_time, total_response_time, total_turnaround_time,completed_processes,round_robin_queue

def RoundRobin(processes, time_quantum):
    priority_queue = PriorityQueue()
    
    current_time = 0

    while processes or priority_queue.qsize() > 0 or round_robin_queue:
        # Add arriving processes to priority queue
        while processes and processes[0].arrival_time <= current_time:
            process = processes.pop(0)
            priority_queue.put((process.priority, process))

        # Execute processes in priority queue
        if not priority_queue.empty():
            _, current_process = priority_queue.get()
            print(f"Executing {current_process.name} at time {current_time}", end=" ")

            scan_queues(current_process,current_time, time_quantum, total_response_time,total_turnaround_time)
            current_time += time_quantum
 
        elif round_robin_queue:
            # If priority queue is empty, execute processes in round robin queue
            current_process = round_robin_queue.pop(0)
            print(f"Executing {current_process.name} (RR) at time {current_time}", end=" ")
            scan_queues(current_process,current_time, time_quantum, total_response_time,total_turnaround_time)
            current_time += time_quantum
        else:
            current_time += 1  # Idle time when no processes are ready




if __name__ == "__main__":
    num_processes = int(input("Enter the number of processes: "))
    processes = []

    for i in range(num_processes):
        name = f"P{i + 1}"
        arrival_time = int(input(f"Enter arrival time for {name}: "))
        duration = int(input(f"Enter duration for {name}: "))
        priority = int(input(f"Enter priority (1-7) for {name}: "))
        processes.append(Process(name, arrival_time, duration, priority))

    time_quantum = int(input("Enter the time quantum for Round Robin: "))

    # Sort processes based on arrival time and priority
    processes.sort(key=lambda x: (x.arrival_time, x.priority))

    RoundRobin(processes, time_quantum)
    if completed_processes:
        calc_avgs(completed_processes)
        
    while 1:
        temp= input("enter 'q' to exit program : ")
        if temp != 'q':
            round_robin_queue = []
            completed_processes = []
            create_random_processes()
            processes.sort(key=lambda x: (x.arrival_time, x.priority))
            RoundRobin(processes, time_quantum)
            if completed_processes:
                calc_avgs(completed_processes)
        elif temp == 'q':
            sys.exit()