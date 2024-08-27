import threading
import time
from collections import deque

class Core:
    def __init__(self, memory_size=256):
        self.registers = [0] * 4
        self.program_counter = 0
        self.memory = [0] * memory_size
        self.running = False
        self.lock = threading.Lock()

    def load_program(self, program):
        for i, instruction in enumerate(program):
            self.memory[i] = instruction
        self.running = True
        self.program_counter = 0

    def fetch(self):
        with self.lock:
            if self.program_counter < len(self.memory):
                instruction = self.memory[self.program_counter]
                self.program_counter += 1
                return instruction
            return None

    def decode_execute(self, instruction):
        parts = instruction.split()
        opcode = parts[0]
        if opcode == 'MOV':
            reg = int(parts[1][1])
            value = int(parts[2])
            self.registers[reg] = value
        elif opcode == 'ADD':
            reg1 = int(parts[1][1])
            reg2 = int(parts[2][1])
            self.registers[reg1] += self.registers[reg2]
        elif opcode == 'SUB':
            reg1 = int(parts[1][1])
            reg2 = int(parts[2][1])
            self.registers[reg1] -= self.registers[reg2]
        elif opcode == 'LOAD':
            reg = int(parts[1][1])
            address = int(parts[2])
            self.registers[reg] = self.memory[address]
        elif opcode == 'STORE':
            reg = int(parts[1][1])
            address = int(parts[2])
            self.memory[address] = self.registers[reg]
        elif opcode == 'JMP':
            address = int(parts[1])
            self.program_counter = address
        elif opcode == 'JZ':
            reg = int(parts[1][1])
            address = int(parts[2])
            if self.registers[reg] == 0:
                self.program_counter = address
        elif opcode == 'JNZ':
            reg = int(parts[1][1])
            address = int(parts[2])
            if self.registers[reg] != 0:
                self.program_counter = address
        elif opcode == 'HLT':
            self.running = False
        return self.running

    def run(self):
        while self.running:
            instruction = self.fetch()
            if instruction:
                self.decode_execute(instruction)
                self.debug_state()
            else:
                self.running = False

    def debug_state(self):
        print(f"PC: {self.program_counter}, Registers: {self.registers}, Memory: {self.memory[:10]}")

class SimpleCPU:
    def __init__(self, memory_size=256, num_threads=2, scheduling_algorithm='round_robin'):
        self.num_threads = num_threads
        self.cores = [Core(memory_size) for _ in range(num_threads)]
        self.threads = []
        self.tasks = deque()
        self.lock = threading.Lock()
        self.running = True
        self.scheduling_algorithm = scheduling_algorithm
        self.task_states = {}  # Stores the state of each task (ready, running, waiting)

    def load_program(self, program):
        for core in self.cores:
            core.load_program(program)

    def add_task(self, task, priority=1):
        task_tuple = tuple(task)  # Convert task to a hashable type (tuple)
        with self.lock:
            self.tasks.append((priority, task_tuple))
            self.tasks = deque(sorted(self.tasks, key=lambda x: -x[0]))  # Higher priority tasks first
            self.task_states[task_tuple] = 'ready'

    def schedule(self):
        while self.running:
            with self.lock:
                for core in self.cores:
                    if not core.running and self.tasks:
                        priority, task = self.tasks.popleft()
                        core.load_program(list(task))  # Convert task back to list
                        thread = threading.Thread(target=core.run)
                        self.threads.append(thread)
                        thread.start()
                        self.task_states[task] = 'running'
                    elif core.running:
                        self.task_states[task] = 'running'
                    else:
                        self.task_states[task] = 'waiting'
            time.sleep(0.1)  # Simple time slice for round-robin scheduling

    def stop(self):
        self.running = False
        for thread in self.threads:
            thread.join()
        print("All threads have been stopped.")

class SimpleRTOS:
    def __init__(self, cpu):
        self.cpu = cpu

    def add_task(self, task, priority=1):
        self.cpu.add_task(task, priority)

    def start(self):
        scheduler_thread = threading.Thread(target=self.cpu.schedule)
        scheduler_thread.start()

    def stop(self):
        self.cpu.stop()

# Example program with branching and memory access
program = [
    "MOV R0 10",   # Move 10 to R0
    "MOV R1 20",   # Move 20 to R1
    "ADD R0 R1",   # Add R1 to R0
    "STORE R0 0",  # Store the value of R0 to memory address 0
    "MOV R2 0",    # Move 0 to R2
    "LOAD R3 0",   # Load the value from memory address 0 to R3
    "JZ R3 10",    # Jump to address 10 if R3 is zero
    "SUB R0 R1",   # Subtract R1 from R0
    "MOV R2 1",    # Use R2 as a condition to break the loop
    "JZ R2 9",     # Jump to HLT if R2 is zero (never true here)
    "JMP 6",       # Jump to address 6 (infinite loop if not halted)
    "HLT"          # Halt the CPU
]

# Create CPU and RTOS
cpu = SimpleCPU(num_threads=2)
rtos = SimpleRTOS(cpu)

# Add tasks to the RTOS with different priorities
rtos.add_task(program, priority=2)
rtos.add_task(program, priority=1)

# Start the RTOS
rtos.start()

# Run for some time then stop
time.sleep(2)
rtos.stop()