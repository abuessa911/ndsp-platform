class CapitalManager:

    def __init__(self):
        self.peak_equity = 0

    def update_peak(self, equity):
        if equity > self.peak_equity:
            self.peak_equity = equity

    def get_peak(self):
        return self.peak_equity

    def compute_drawdown(self, equity):
        if self.peak_equity == 0:
            return 0
        return (self.peak_equity - equity) / self.peak_equity
