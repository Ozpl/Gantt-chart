# Gantt chart

This script produces Plotly's interactive Gantt chart based on given input.

Let's consider example below:
![Example](https://i.gyazo.com/802d58d60be3502c87bfab07cb7f2a77.png)
We have four types of machines that work in continuous production: first operation on machine called M1, next one being M2 and so on until M4.
We can have multiple machines of any given type, as it is with M3. Knowing time of each operation on each of the machine types, we can calculate production flow and draw Gantt chart from it.

The result is interactive Plotly webpage with drawn chart:
![Result](https://i.gyazo.com/3ded98d6606e12170b723388a9340c94.png)