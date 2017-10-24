class Monomer:
    def __init__(self, tube, x, y, type):
        print('new')

        self.columns = tube.columns
        self.struct = tube.struct
        self.shift = 3
        self.x = x
        self.y = y
        self.hydrolysed = False
        self.type = type  # 1 - alpha, 2 - betha
        self.bended = True  # by default new monomer is bended
        self.connections = 0  # monomer is bended => 0 lateral connections

    def straighten(self):
        print('str')
        # previous column
        try:
            if self.x == 0:
                self.left = next(e for e in reversed(self.struct[self.columns - 1]) if (not e.bended and e.y == self.y - self.shift))
            else:
                self.left = next(e for e in reversed(self.struct[self.x - 1]) if (not e.bended and e.y == self.y))

            self.left.connections += 1
            self.connections += 1
        except StopIteration:
            pass

        # next column
        try:
            self.right = next(e for e in reversed(self.struct[self.x + 1]) if (not e.bended and e.y == self.y))
        except StopIteration:
            pass
        except IndexError:
            try:
                self.right = next(e for e in reversed(self.struct[0]) if (not e.bended and e.y == self.y + self.shift))
            except StopIteration:
                pass

        try:
            self.right.connections += 1
            self.connections += 1
        except AttributeError:
            pass

        self.bended = False

    def bend(self):
        print('bnd')

        # left neighbour
        try:
            del self.left.right
            self.left.connections -= 1
        except AttributeError:
            pass

        # right neighbour
        try:
            del self.right.left
            self.right.connections -= 1
        except AttributeError:
            pass

        self.bended = True
        return True

    def hydrolyse(self):
        print('hydro')

        self.hydrolysed = True
        return True

    def __del__(self):
        return True
