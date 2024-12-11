from dataclasses import dataclass

@dataclass
class Product:
    sequence: int = 0
    progress: int = 0
    goal: int = 0
    starting_point: int = 0

@dataclass
class Machine:
    machine_type: str
    name: str
    duration: int
    input: str = ''
    output: str = ''
    current_product: Product = None

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

def check_available_machines(machine_list: list[Machine]) -> list[Machine]:
    result = {}

    for i, machine in enumerate(machine_list):
        if machine.current_product is None:
            if result.get(machine.machine_type):
                result[machine.machine_type].append(i)
            else:
                result[machine.machine_type] = [i]
            
    return result

def prepare_data(machine_list: list[Machine], daily_efficiency: int) -> dict:
    #Machine list needs to be reversed first
    machine_list.reverse()
    machine_list = list(machine_list)
    first_machine_type = ''
    last_machine_type = ''
    
    to_produce_counter = daily_efficiency
    
    results = {}
    
    for machine in machine_list:
        if machine.input is None:
            first_machine_type = machine.machine_type
        if machine.output is None:
            last_machine_type = machine.machine_type
    
    step_counter = 0
    while True:
        available_machines = check_available_machines(machine_list)
        
        #Check products already on machines
        for machine in machine_list:
            if machine.current_product is not None:                
                #If product is in production, add time unit
                if machine.current_product.progress < machine.current_product.goal - 1:
                    machine.current_product.progress += 1
                #If product is done, try to move it to next machine
                elif machine.current_product.progress >= machine.current_product.goal - 1:
                    #If it's the last machine, remove product from it
                    if machine.machine_type == last_machine_type:
                        results[str(machine.current_product.sequence)].append(machine.current_product.starting_point + machine.current_product.goal)
                        machine.current_product = None
                    
                    #If next machine is empty, move product
                    if available_machines.get(machine.output):
                        machine_index = available_machines[machine.output][-1]
                        
                        machine_list[machine_index].current_product = Product(sequence=machine.current_product.sequence,
                                                                              progress=0,
                                                                              goal=machine_list[machine_index].duration,
                                                                              starting_point=step_counter)
                        machine.current_product = None
                        
                        available_machines[machine.output].pop(-1)
                        if available_machines.get(machine.machine_type):
                            available_machines[machine.machine_type].append(machine_index+1)
                        else:
                            available_machines[machine.machine_type] = [machine_index+1]
                        if available_machines[machine.output] == []:
                            del available_machines[machine.output]
                            
                        results[str(machine_list[machine_index].current_product.sequence)].append(machine_list[machine_index].current_product.starting_point)
        
        #Products enter the line through the empty first machines
        if to_produce_counter > 0:
            if available_machines.get(first_machine_type):
                for machine_index in available_machines[first_machine_type]:
                        top_product = Product(sequence=daily_efficiency-to_produce_counter+1,
                                            progress=0,
                                            goal=machine_list[machine_index].duration,
                                            starting_point=step_counter)
                        machine_list[machine_index].current_product = top_product
                        to_produce_counter -= 1
                        results[str(top_product.sequence)] = [top_product.starting_point]
        
        #Check if we have achieved daily efficiency
        if to_produce_counter == 0:
            all_machines_empty = True
            for machine in machine_list:
                if machine.current_product is not None:
                    all_machines_empty = False
            if all_machines_empty:
                break
            
        step_counter = step_counter + 1
        
    return results

#Machines need to be in sequence from first to last
test_daily_efficiency = 100
test_input_data = {
    "M1": {"duration": 150, "count": 1, 'input': None, 'output': 'M2'},
    "M2": {"duration": 200, "count": 1, 'input': 'M1', 'output': 'M3'},
    "M3": {"duration": 300, "count": 1, 'input': 'M2', 'output': 'M4'},
    "M4": {"duration": 250, "count": 1, 'input': 'M3', 'output': None},
}
test_machine_list = instantiate_machines(test_input_data)

series_1_daily_efficiency = 150
series_1_input_data = {
    "M1": {"duration": 210, "count": 2, 'input': None, 'output': 'M2'},
    "M2": {"duration": 390, "count": 3, 'input': 'M1', 'output': 'M3'},
    "M3": {"duration": 420, "count": 3, 'input': 'M2', 'output': 'M4'},
    "M4": {"duration": 130, "count": 1, 'input': 'M3', 'output': None},
}
series_1_machine_list = instantiate_machines(series_1_input_data)

series_2_daily_efficiency = 100
series_2_input_data = {
    "M1": {"duration": 200, "count": 2, 'input': None, 'output': 'M2'},
    "M2": {"duration": 250, "count": 3, 'input': 'M1', 'output': 'M3'},
    "M3": {"duration": 350, "count": 3, 'input': 'M2', 'output': 'M4'},
    "M4": {"duration": 270, "count": 1, 'input': 'M3', 'output': None},
}
series_2_machine_list = instantiate_machines(series_2_input_data)

results = prepare_data(test_machine_list, test_daily_efficiency)