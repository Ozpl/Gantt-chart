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

def check_available_machines(machine_list: list[Machine]) -> list[Machine]:
    result = {}

    for i, machine in enumerate(machine_list):
        if not machine.is_occupied:
            if result.get(machine.machine_type):
                result[machine.machine_type].append(i)
            else:
                result[machine.machine_type] = [i]
            
    return result

test_daily_efficiency = 1
test_input_data = {
    "M1": {"duration": 210, "count": 1, 'input': None, 'output': 'M2'},
    "M2": {"duration": 390, "count": 1, 'input': 'M1', 'output': 'M3'},
    "M3": {"duration": 420, "count": 1, 'input': 'M2', 'output': 'M4'},
    "M4": {"duration": 130, "count": 1, 'input': 'M3', 'output': None},
}
test_takt = calculate_takt(test_input_data)
test_start = decide_start(test_input_data)

# region Series 1
series_1_daily_efficiency = 150
series_1_input_data = {
    "M1": {"duration": 210, "count": 2, 'input': None, 'output': 'M2'},
    "M2": {"duration": 390, "count": 3, 'input': 'M1', 'output': 'M3'},
    "M3": {"duration": 420, "count": 3, 'input': 'M2', 'output': 'M4'},
    "M4": {"duration": 130, "count": 1, 'input': 'M3', 'output': None},
}
series_1_takt = calculate_takt(series_1_input_data)
series_1_start = decide_start(series_1_input_data)
# endregion

# region Series 2
series_2_daily_efficiency = 100
series_2_input_data = {
    "M1": {"duration": 200, "count": 2, 'input': None, 'output': 'M2'},
    "M2": {"duration": 250, "count": 3, 'input': 'M1', 'output': 'M3'},
    "M3": {"duration": 350, "count": 3, 'input': 'M2', 'output': 'M4'},
    "M4": {"duration": 270, "count": 1, 'input': 'M3', 'output': None},
}
series_2_takt = calculate_takt(series_2_input_data)
series_2_start = decide_start(series_2_input_data)
# endregion

series_1_machine_list = instantiate_machines(series_1_input_data)
series_2_machine_list = instantiate_machines(series_2_input_data)
test_machine_list = instantiate_machines(test_input_data)

test_to_produce_counter = test_daily_efficiency
test_in_production_list: list[Product] = []

series_1_order_end_time = 0
series_2_order_end_time = 0
test_order_end_time = 0

current_step = 0

check_available_machines(test_machine_list)

def prepare_data(machine_list: list[Machine], first_machine_name: str) -> None:
    machine_list = list(machine_list)
    in_production_list = []
    
    while True:
        available_machines = check_available_machines(machine_list)
        
        #Produkty na linii
        for product in in_production_list:
            for machine_type in available_machines.keys():
                if machine_type is not first_machine_name:
                    ...
        
        #Puste produkty wprowadzamy na linię
        for machine_index in available_machines[first_machine_name]:
            if available_machines.get(first_machine_name):
                top_product = Product(0,
                                    machine_list[machine_index].duration,
                                    machine_list[machine_index].machine_type,
                                    machine_list[machine_index].output)
                in_production_list.append(top_product)
                machine_list[machine_index].is_occupied = True

prepare_data(test_machine_list, test_start)
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
