from dataclasses import dataclass

@dataclass
class Machine:
    machine_type: str
    name: str
    duration: int
    input: str = ''
    output: str = ''
    is_occupied: bool = False

@dataclass
class Product:
    progress: int = 0
    goal: int = 0
    current_machine: str = ''
    next_machine: str = ''

def instantiate_machines(input_list: dict) -> list[Machine]:
    output_list = list()
    
    for machine_type in input_list:
        for i in range(1, input_list[machine_type]['count']+1):
            output_list.append(Machine(
                machine_type=machine_type,
                name=f'{machine_type}_{i}',
                duration=input_list[machine_type]['duration'],
                input=input_list[machine_type]['input'],
                output=input_list[machine_type]['output']
                ))
    
    return output_list

def calculate_takt(input_list: dict) -> int:
    takt = 0
    
    for machine_type in input_list:
        if input_list[machine_type]['duration'] > takt:
            takt = input_list[machine_type]['duration']
        
    return takt

def decide_start(input_list: dict) -> str:
    start = ''
    
    for machine_type in input_list:
        if not input_list[machine_type]['input']:
            start = machine_type
    
    return start

def available_machines(machine_list: dict, machine_type: str) -> list[Machine]:
    ...

test_daily_efficiency = 1
test_input_data = {
    "M1": { "duration": 210, "count": 1, 'input': None, 'output': 'M2'},
    "M2": { "duration": 390, "count": 1, 'input': 'M1', 'output': 'M3'},
    "M3": { "duration": 420, "count": 1, 'input': 'M2', 'output': 'M4'},
    "M4": { "duration": 130, "count": 1, 'input': 'M3', 'output': None},
}
test_takt = calculate_takt(test_input_data)
test_start = decide_start(test_input_data)

#region Series 1
series_1_daily_efficiency = 150
series_1_input_data = {
    "M1": { "duration": 210, "count": 2, 'input': None, 'output': 'M2'},
    "M2": { "duration": 390, "count": 3, 'input': 'M1', 'output': 'M3'},
    "M3": { "duration": 420, "count": 3, 'input': 'M2', 'output': 'M4'},
    "M4": { "duration": 130, "count": 1, 'input': 'M3', 'output': None},
}
series_1_takt = calculate_takt(series_1_input_data)
series_1_start = decide_start(series_1_input_data)
#endregion

#region Series 2
series_2_daily_efficiency = 100
series_2_input_data = {
    "M1": { "duration": 200, "count": 2, 'input': None, 'output': 'M2'},
    "M2": { "duration": 250, "count": 3, 'input': 'M1', 'output': 'M3'},
    "M3": { "duration": 350, "count": 3, 'input': 'M2', 'output': 'M4'},
    "M4": { "duration": 270, "count": 1, 'input': 'M3', 'output': None},
}
series_2_takt = calculate_takt(series_2_input_data)
series_2_start = decide_start(series_2_input_data)
#endregion

series_1_machine_list = instantiate_machines(series_1_input_data)
series_2_machine_list = instantiate_machines(series_2_input_data)
test_machine_list = instantiate_machines(test_input_data)

test_to_produce_list = []
for _ in range(0, test_daily_efficiency):
    test_to_produce_list.append(Product())
test_in_production_list: list[Product] = []

series_1_order_end_time = 0
series_2_order_end_time = 0
test_order_end_time = 0

current_step = 0

#Series 1 main loop
while True:
    current_step = current_step + 1
    
    available_machines = []
    for machine in test_machine_list:
        if not machine.is_occupied:
            available_machines.append(machine)
    
    for product in test_in_production_list:
        if product.progress >= product.goal:
            ...
    
    ...
    break


'''
co kazdy krok:
    * sprawdzamy czy mozna dodać nowy wyrob do linii (czyli czy typ maszyny startowej jest wolny)
    * dla kazdej maszyny:
        * jezeli progress jest rowny duration:
            * wyzeruj progress i is_occupied=False
            * sprawdz
        * jezeli jest mniejszy, is_occupied=True
    * 
'''
