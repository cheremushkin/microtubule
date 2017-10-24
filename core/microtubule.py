from .monomer import Monomer

import numpy as np


class Microtubule:
    possible_events = []  # all current possible events
    types = {
        'association': 'associate',
        'dissociation': 'dissociate',
        'straightening': 'straighten',
        'bending': 'bend',
        'hydrolysis': 'hydrolyse'
    }

    def __init__(self, columns, timer, depth, fps, events):
        self.events = events

        # time
        self.step = 1 / fps
        self.timer = timer

        # initial
        self.time = 0
        self.iterator = 0

        # structure
        self.columns = columns
        self.struct = [[] for i in range(columns)]
        self.depth = depth

        # output data
        self.table = [[i] for i in range(columns)]
        self.data = [['time'], ['straight'], ['bend']]

    # manually set the structure
    def seed(self, seed):
        for x in range(self.columns):
            y = 0
            for cell in seed[x].split(' '):
                self.struct[x].append(Monomer(self, x, y, 1))
                self.struct[x].append(Monomer(self, x, y + 1, 2))

                if int(cell[0]):
                    self.struct[x][y].hydrolyse()
                    self.struct[x][y + 1].hydrolyse()

                if not int(cell[1]):
                    self.struct[x][y].straighten()
                    self.struct[x][y + 1].straighten()

                y += 2

    def build(self):
        while self.time < self.timer:
            self.parse(self.depth)
            self.time += self.possible_events[0][0]

            # count state and generate output
            self.output()

            # invoke an event
            self.invoke()

            # clear an array of events
            self.possible_events.clear()

        return self.table, self.data

    # parsing events
    def parse(self, depth):
        # depth
        depth = max(0, min(map(lambda f: len([c for c in f if not c.bended]), self.struct)) - depth * 2)

        # association
        for i in range(self.columns):
            self.possible_events.append(self.events.association(i, len(self.struct[i])))

        # straightening
        for column in self.struct:
            try:
                cell = next(e for e in column if e.bended)
                self.possible_events.append(self.events.straightening(cell.x, cell.y))
            except StopIteration:
                continue

        # bending
        for x in range(self.columns):
            # finds the highest straightened monomer
            try:
                cell = next(e for e in reversed(self.struct[x]) if not e.bended)
            except StopIteration:
                continue

            # if it exists
            connections = 0
            y = (cell.y - 1) - 2  # of the alpha in the filament
            while y >= depth:
                # count connections
                try:
                    connections += self.struct[x][y].connections + self.struct[x][y + 1].connections
                    self.possible_events.append(self.events.bending(x, y, connections, self.struct[x][y].hydrolysed))
                except IndexError:
                    print('{}, {}, d: {}'.format(x, y, depth))
                y -= 2

        # dissociation
        for column in self.struct:
            try:
                elem = next(e for e in column if e.bended)  # lowest bended alpha monomer

                for y in range(elem.y, len(column), 2):
                    self.possible_events.append(self.events.dissociation(elem.x, y, elem.hydrolysed))
            except StopIteration:
                continue

        # hydrolysis
        for column in self.struct:
            try:
                cell = column[-2]
                if not cell.hydrolysed:
                    self.possible_events.append(self.events.hydrolysis(cell.x, cell.y))
            except IndexError:
                continue

        # sort by time
        self.possible_events.sort()

    # invokes an event
    def invoke(self):
        event = self.possible_events[0]
        method = getattr(self, self.types[event[1]])
        method(event[2], event[3])

    # list of events to invoke
    def associate(self, x, y):
        self.struct[x].append(Monomer(self, x, y, 1))
        self.struct[x].append(Monomer(self, x, y + 1, 2))

    def straighten(self, x, y):
        self.struct[x][y].straighten()
        self.struct[x][y + 1].straighten()

    def bend(self, x, y):
        for cell in self.struct[x]:
            if cell.y < y: continue;
            if cell.bended: break;
            cell.bend()

    def hydrolyse(self, x, y):
        self.struct[x][y].hydrolyse()
        self.struct[x][y + 1].hydrolyse()

    def dissociate(self, x, y):
        del self.struct[x][y:]

    # output info
    def output(self):
        for i in range(self.iterator, int(self.time / self.step)):
            # structure
            for j in range(self.columns):
                string = '00 '
                for cell in self.struct[j]:
                    if cell.y % 2:
                        continue

                    string += '{}{} '.format(1 if cell.hydrolysed else 0, 1 if cell.bended else 0)

                self.table[j].append(string)

            self.data[0].append(self.iterator * self.step)
            self.data[1].append(sum(map(lambda f: len([c for c in f if not c.bended]), self.struct)) / self.columns)
            self.data[2].append(sum(map(lambda f: len([c for c in reversed(f) if c.bended]), self.struct)) / self.columns)

            self.iterator += 1