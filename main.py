from dataclasses import dataclass
import datetime
import pandas as pd
import plotly.express as px


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


def find_empty_machine_index(machine_list: list[Machine], machine_type: str) -> int:
    for i, machine in enumerate(machine_list):
        if machine.current_product is None and machine.machine_type == machine_type:
            return i


def prepare_data(machine_list: list[Machine], daily_efficiency: int) -> dict:
    machine_list = list(machine_list[::-1])
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

        # Check products already on machines
        for machine_index, machine in enumerate(machine_list):
            if machine.current_product is not None:
                # If product is in production, add time unit
                if machine.current_product.progress < machine.current_product.goal - 1:
                    machine.current_product.progress += 1
                # If product is done, try to move it to next machine
                elif machine.current_product.progress >= machine.current_product.goal - 1:
                    # If it's the last machine, remove product from it
                    if machine.machine_type == last_machine_type:
                        machine.current_product = None

                        if available_machines.get(machine.machine_type):
                            available_machines[machine.machine_type].append(find_empty_machine_index(machine_list, machine.machine_type))
                        else:
                            available_machines[machine.machine_type] = [find_empty_machine_index(machine_list, machine.machine_type)]

                    # If next machine is empty, move product
                    if available_machines.get(machine.output):
                        available_machine_index = available_machines[machine.output][-1]

                        machine_list[available_machine_index].current_product = Product(sequence=machine.current_product.sequence,
                                                                                        progress=0,
                                                                                        goal=machine_list[available_machine_index].duration,
                                                                                        starting_point=step_counter)

                        results[str(machine_list[available_machine_index].current_product.sequence)].append(
                            tuple(
                                (machine_list[available_machine_index].current_product.starting_point,
                                 machine_list[available_machine_index].current_product.starting_point +
                                 machine_list[available_machine_index].current_product.goal, machine_list[available_machine_index].name)))
                        machine.current_product = None

                        available_machines[machine.output].pop(-1)
                        if available_machines.get(machine.machine_type):
                            available_machines[machine.machine_type].append(machine_index)
                        else:
                            available_machines[machine.machine_type] = [machine_index]
                        if available_machines[machine.output] == []:
                            del available_machines[machine.output]

        # Products enter the line through the empty first machines
        if to_produce_counter > 0:
            if available_machines.get(first_machine_type):
                for available_machine_index in available_machines[first_machine_type]:
                    top_product = Product(sequence=daily_efficiency-to_produce_counter+1,
                                          progress=0,
                                          goal=machine_list[available_machine_index].duration,
                                          starting_point=step_counter)
                    machine_list[available_machine_index].current_product = top_product
                    to_produce_counter -= 1

                    results[str(top_product.sequence)] = [tuple((top_product.starting_point,
                                                                 top_product.starting_point + top_product.goal, machine_list[available_machine_index].name))]

        # Check if we have achieved daily efficiency
        if to_produce_counter == 0:
            all_machines_empty = True
            for machine in machine_list:
                if machine.current_product is not None:
                    all_machines_empty = False
            if all_machines_empty:
                break

        step_counter = step_counter + 1

    return results


def create_dataframe_from_results(machine_list: list[Machine], results: dict) -> pd.DataFrame:
    machine_names = []

    for machine in machine_list:
        machine_names.append(machine.name)

    df_list = []

    for product in results:
        for result in results[product]:
            df_list.append(dict(
                Task=str(list(series_1_results.keys())[0]),
                Start=datetime.datetime.fromtimestamp(result[0], tz=datetime.timezone.utc),
                Finish=datetime.datetime.fromtimestamp(result[1], tz=datetime.timezone.utc),
                Product=str(product),
                Machine=f"Maszyna {result[2]}"))

    df = pd.DataFrame(df_list)
    return df


def show_plot(df: pd.DataFrame, title: str) -> None:
    fig = px.timeline(df, x_start="Start", x_end="Finish", y="Machine", color="Product", title=f"Gantt Chart - {title}")
    fig.update_layout(yaxis={'categoryorder': 'category ascending'})
    fig.update_xaxes(
        tickformat="%H\n%M",
        tickformatstops=[dict(dtickrange=[3600000, 86400000], value="%H:%M")]
    )
    fig.show()


# Series 1
series_1_daily_efficiency = 150
series_1_input_data = {
    "M1": {"duration": 210, "count": 2, 'input': None, 'output': 'M2'},
    "M2": {"duration": 390, "count": 3, 'input': 'M1', 'output': 'M3'},
    "M3": {"duration": 420, "count": 3, 'input': 'M2', 'output': 'M4'},
    "M4": {"duration": 130, "count": 1, 'input': 'M3', 'output': None},
}
series_1_machine_list = instantiate_machines(series_1_input_data)

series_1_results = prepare_data(series_1_machine_list, series_1_daily_efficiency)
series_1_df = create_dataframe_from_results(series_1_machine_list, series_1_results)
show_plot(series_1_df, 'Series 1')

# Series 2
series_2_daily_efficiency = 100
series_2_input_data = {
    "M1": {"duration": 200, "count": 2, 'input': None, 'output': 'M2'},
    "M2": {"duration": 250, "count": 3, 'input': 'M1', 'output': 'M3'},
    "M3": {"duration": 350, "count": 3, 'input': 'M2', 'output': 'M4'},
    "M4": {"duration": 270, "count": 1, 'input': 'M3', 'output': None},
}
series_2_machine_list = instantiate_machines(series_2_input_data)

series_2_results = prepare_data(series_2_machine_list, series_2_daily_efficiency)
series_2_df = create_dataframe_from_results(series_2_machine_list, series_2_results)
show_plot(series_2_df, 'Series 2')
