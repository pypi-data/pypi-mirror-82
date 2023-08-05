import numpy as np
from sklearn.linear_model import LinearRegression

class Linear():
    def __init__(self):
        super().__init__()
    def initModel(self):
        self.model = LinearRegression()
    def fit(self, x, y):
        self.model.fit(x, y)
    def predict(self, val):
        return self.model.predict(val)    
    def score(self, x, y):
        r_sq = self.score(x, y)
        return r_sq
        
