class FitzBlockWrapper:
    def __init__(self, block):
        self.x0, self.y0, self.x1, \
            self.y1, self.text, \
            self.block_number, self.block_type = block

        self.x0 = int(self.x0)
        self.x1 = int(self.x1)
        self.y0 = int(self.y0)
        self.y1 = int(self.y1)
        self.block_number = int(self.block_number)
        self.block_type = int(self.block_type)

    def __str__(self):
        return str((
            self.x0, self.y0, self.x1, self.y1, self.text
        ))

    def __repl__(self):
        return self.__str__()
