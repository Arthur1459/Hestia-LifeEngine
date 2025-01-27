# Hestia Life Engine - Arthur1459

### Overview
Hestia is a 'Cellular Life Engine': in a world, [creature](./src/Creature.py) can grow, reproduce and evolve according to natural selection.

Each creature have a multiple brains ([Neural Network](./src/Brain.py)) for their possible actions (Moving, Reproduce, Grow...) according to the information that the creature have (Itself, close environment, eyes..).

The creature is composed of a BODY which is its main organ (the brain). From it, ARM can be generated as children of the BODY. And each ARM can have children like other ARM or SPIKE or REPRODUCTOR or even EYE.
Each cell which is part of a creature have a father-cell and children-cells.

Each cell can eat [Food](./src/Environement.py) by moving on it, which gave them life points. But if a creature develop some "SPIKE" organ, they can eat the other creatures and get their life points.
If a cell of the creature have more than 100 life points, the extra is given to its father, until the main BODY cell is reached.

When a creature decide to **reproduce** itself, it will search a REPRODUCTOR cell in its body and ask a free place for the newborn.
If the place is found and the condition full-filled, a new BODY appears with the **mutated-genetic** of its father. The mutation follow a **normal law** of variance set in `config.py`. (For more details see the `Mutate` method in [Neural Network](./src/Brain.py)).
The mutation leads to modify the weights of the neural-networks and can also add new neurons and even new layers. Thus, the creature's brain evolve over generations and natural selection do its job.

### Try Yourself

Requirement :
+ Python 3  (`terminal : python3 --version`)
+ Pygame  (`terminal : pip3 install pygame`)

You can config the simulation in [config.py](./src/config.py).
You can modify some config parameter during the simulation with keyboard. (see `config.py`).

To setup walls, go in [Grid.py](./src/Grid.py) and find the `add_initial_elements` method. You can add wall at (line, row) with `self.putAt(Wall((line, row)), (line, row))`.

You still need to run `main.py`.

### How it looks : Video


[![Video Demo](https://www.youtube.com/watch?v=lEb7CYoWC1o)](./src/rsc/ytb_viewer.png)

