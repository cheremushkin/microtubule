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

    def __init__(self, **args):
        self.events = args.get('events')

        # time
        self.step = 1 / args.get('fps')
        self.timer = args.get('timer')

        # initial
        self.time = 0
        self.iterator = 0

        # structure
        self.columns = args.get('columns')
        self.structure = [[] for i in range(self.columns)]
        self.window = args.get('window')
        self.shift = 3
        self.layers = 0

        # seed
        for x in range(self.columns):
            for y in range(self.window):
                self.structure[x].append(Monomer(type='a').straighten())
                self.structure[x].append(Monomer(type='b').straighten())

        # output data
        #self.table = [[i] for i in range(self.columns)]
        #self.data = [['time'], ['straight'], ['bend']]

    def build(self):
        while self.time < self.timer:
            print()
            #print('before resize')
            print('layers: {}'.format(self.layers))
            print('len: {}'.format(self.layers + sum(map(lambda f: int(len(f) / 2), self.structure)) / self.columns))
            print('str: {}'.format(self.layers + sum(map(lambda f: int(len([e for e in f if not e.bended]) / 2), self.structure)) / self.columns))
            print()
            self.resize_window()
            #print('after resize')
            #print('len: {}'.format(list(map(lambda f: int(len(f) / 2), self.structure))))
            #print('str: {}'.format(list(map(lambda f: int(len([e for e in f if not e.bended]) / 2), self.structure))))
            #print()

            # parse events
            self.parse()
            self.time += self.possible_events[0][0]

            # count state and generate output
            #self.output()

            # invoke an event
            self.invoke()

            # clear an array of events
            self.possible_events.clear()

        #return self.table, self.data

    # check dynamic window
    def resize_window(self):
        l = int(min(map(lambda f: len([c for c in f if not c.bended]), self.structure)) / 2)

        if l > self.window:
            self.structure = list(map(lambda f: f[2:], self.structure))
            self.layers += 1
            print('delete row')
        elif l < self.window:
            for i in range(self.window - l):
                print('add row')
                list(
                    map(
                        lambda f: {
                            f.insert(0, Monomer(type='a').straighten()),
                            f.insert(1, Monomer(type='b').straighten())
                        },
                        self.structure
                    )
                )
                self.layers -= 1

    # count lateral connections for each monomer => (t, d)
    def connections(self, x, y):
        t = 0
        d = 0

        # previous column
        try:
            if x == 0:
                left = next(e for i, e in enumerate(reversed(self.structure[self.columns - 1])) if (not e.bended and i == y - self.shift))
            else:
                left = next(e for i, e in enumerate(reversed(self.structure[x - 1])) if (not e.bended and i == y))

            if left.hydrolysed:
                d += 1
            else:
                t += 1
        except StopIteration:
            pass

        # next column
        try:
            if x == self.columns - 1:
                right = next(e for i, e in enumerate(reversed(self.structure[0])) if (not e.bended and i == y + self.shift))
            else:
                right = next(e for i, e in enumerate(reversed(self.structure[x + 1])) if (not e.bended and i == y))

            if right.hydrolysed:
                d += 1
            else:
                t += 1
        except StopIteration:
            pass

        return t, d

    # parsing events
    def parse(self):
        # association
        for x in range(self.columns):
            try:
                self.possible_events.append(self.events.association(x, len(self.structure[x])))
            except ZeroDivisionError:
                continue

        # straightening
        for x in range(self.columns):
            try:
                y = next(i for i, e in enumerate(self.structure[x]) if e.bended)
                try:
                    self.possible_events.append(self.events.straightening(x, y))
                except ZeroDivisionError:
                    continue
            except StopIteration:
                continue

        # bending
        for x in range(self.columns):
            # finds the highest straightened monomer
            try:
                top = next((i for i, e in enumerate(self.structure[x]) if e.bended), len(self.structure[x]))
            except StopIteration:
                continue

            # if it exists
            connections = 0
            y = top - 2  # of the alpha in the filament
            while y >= 0:
                # count connections
                alpha = self.connections(x, y)
                betha = self.connections(x, y + 1)

                try:
                    self.possible_events.append(self.events.bending(x, y, (alpha[0] + betha[0], alpha[1] + betha[1]), self.structure[x][y].hydrolysed))
                except ZeroDivisionError:
                    continue

                y -= 2

        # dissociation
        for x in range(self.columns):
            try:
                first = next(i for i, e in enumerate(self.structure[x]) if e.bended)  # lowest bended alpha monomer
                for y in range(first, len(self.structure[x]), 2):
                    try:
                        self.possible_events.append(self.events.dissociation(x, y, self.structure[x][y].hydrolysed))
                    except ZeroDivisionError:
                        continue
            except StopIteration:
                continue

        # hydrolysis
        '''for column in self.structure:
            try:
                cell = column[-2]
                if not cell.hydrolysed:
                    try:
                        self.possible_events.append(self.events.hydrolysis(cell.x, cell.y))
                    except ZeroDivisionError:
                        continue
            except IndexError:
                continue'''

        # sort by time
        self.possible_events.sort()

    # invokes an event
    def invoke(self):
        event = self.possible_events[0]
        method = getattr(self, self.types[event[1]])
        method(event[2], event[3])

    # list of events to invoke
    def associate(self, x, y):
        print('assoc {}, {}'.format(x, y))
        self.structure[x].append(Monomer(type='a'))
        self.structure[x].append(Monomer(type='b'))

    def straighten(self, x, y):
        print('str {}, {}'.format(x, y))
        self.structure[x][y].straighten()
        self.structure[x][y + 1].straighten()

    def bend(self, x, y):
        for _y in range(y, len([e for e in self.structure[x] if not e.bended])):
            self.structure[x][_y].bend()

    def hydrolyse(self, x, y):
        self.structure[x][y].hydrolyse()
        self.structure[x][y + 1].hydrolyse()

    def dissociate(self, x, y):
        print('dis {}, {}'.format(x, int(y / 2)))
        del self.structure[x][y:]

    # output info
    def output(self):
        for i in range(self.iterator, int(self.time / self.step)):
            # structure
            for j in range(self.columns):
                string = '00 '
                for cell in self.structure[j]:
                    if cell.y % 2:
                        continue

                    string += '{}{} '.format(1 if cell.hydrolysed else 0, 1 if cell.bended else 0)

                self.table[j].append(string)

            self.data[0].append(self.iterator * self.step)
            self.data[1].append(sum(map(lambda f: len([c for c in f if not c.bended]), self.structure)) / self.columns)
            self.data[2].append(sum(map(lambda f: len([c for c in reversed(f) if c.bended]), self.structure)) / self.columns)

            self.iterator += 1