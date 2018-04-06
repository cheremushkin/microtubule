class Monomer:
    def __init__(self, type):
        self.hydrolysed = False
        self.bended = True  # by default new monomer is bended
        self.type = type  # 1 - alpha, 2 - betha

    def straighten(self):
        self.bended = False

        return self

    def bend(self):
        self.bended = True

        return self

    def hydrolyse(self):
        self.hydrolysed = True

        return self

    def __del__(self):
        return True
