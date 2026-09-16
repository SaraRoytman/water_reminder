class WaterTracker:
    def __init__(self, init_amount = 0):
        self.consumed = init_amount


    def add_tub0(self, amount = 500):
        self.consumed += amount
        return self.consumed

    def add_tub1(self, amount = 250):
        self.consumed += amount
        return self.consumed

    def add_tub2(self, amount = 20):
        self.consumed += amount
        return self.consumed

    def add_caffe(self, fine = 100):
        self.consumed -= fine
        return self.consumed
    
    def add_xl(self, fine = 150):
        self.consumed -= fine
        return self.consumed

    def add_amount(self, amount):
        self.consumed += amount
        return self.consumed   