import numpy as np
import math
from py_expression_eval import Parser

class FalsePosition:
    def __init__(self):
        self.EPSILON = 0.0001
        self.ALPHA = 0.000000001
        self.PRECISION = 10
        self.STEP_SIZE = 0.0001
        self.parser = Parser()
        self.expression = None
        

    ## checks is the expression is valid before setting it [if not, expression remains None]
    def set_expression(self, expression):
        try:
            self.expression = expression
            self.expr = self.parser.parse(expression)
            return True
        except Exception as e:
            raise ValueError(f"Invalid expression: {str(e)}")
            
    def f(self, x):
        try:
            result = self.expr.evaluate({'x': x})
            return float(result)
        except Exception as e:
            raise ValueError(f"Error evaluating expression: {str(e)}")
            
    def approximately_equal_to_zero(self, val):
        return abs(val) <= self.EPSILON
        
    def is_continuous(self, a, b):
        """Check if function is continuous in interval [a,b]"""
        try:
            for p in np.arange(a, b, self.STEP_SIZE):
                left_limit = self.f(p - self.ALPHA)
                right_limit = self.f(p + self.ALPHA)
                actual = self.f(p)
            
                if (math.isnan(left_limit) or math.isnan(right_limit) or math.isnan(actual) 
                    or 
                    math.isinf(left_limit) or math.isinf(right_limit) or math.isinf(actual)):
                    return False
                
                ## A = B, B = C, then A = C
                if not (self.approximately_equal_to_zero(actual - left_limit) and 
                       self.approximately_equal_to_zero(actual - right_limit)):
                    return False
            return True
        except Exception:
            return False
            
    def unequal_signs(self, a, b):
        fa, fb = self.f(a), self.f(b)
        return fa * fb < 0
            
    def number_of_roots(self, a, b):
        roots = 0
        prev_sign = self.f(a) < 0
        
        for x in np.arange(a, b, self.STEP_SIZE):
            curr_sign = self.f(x) < 0
            if curr_sign != prev_sign:
                roots += 1
                prev_sign = curr_sign
        return roots
            
    def is_workable(self, a, b):
        """Check if false position method is applicable"""
        try:
            if self.expression is None:
                return False
                
            cts = self.is_continuous(a, b)
            unequal = self.unequal_signs(a, b)
            n_roots = self.number_of_roots(a, b)
            
            return {
                'workable': cts and unequal and n_roots == 1,
                'continuous': cts,
                'unequal_signs': unequal,
                'num_roots': n_roots
            }
        except Exception as e:
            raise ValueError(f"Error checking workability: {str(e)}")
            
    def solve(self, a, b, callback=None):
        """
        Find root using false position method.
        callback is an optional function to receive iteration updates.
        """
        try:
            n_iters = 0
            while True:
                n_iters += 1
                fa, fb = self.f(a), self.f(b)
                
                # Calculate c using false position formula
                c = b - fb * (b - a) / (fb - fa)
                fc = self.f(c)
                
                # Call callback with iteration info if provided
                if callback:
                    callback(n_iters, c, fc)
                
                if abs(fc) <= self.ALPHA:
                    break
                    
                if fa * fc < 0:
                    b = c
                else:
                    a = c
                    
            return {
                'root': c,
                'f_root': fc,
                'iterations': n_iters
            }
        except Exception as e:
            raise ValueError(f"Error in false position method: {str(e)}")
            
    def get_plot_points(self, a, b, num_points=1000):
        """Get points for plotting the function"""
        try:
            THREE_HALFS = 1.5
            rng = b - a
            x = np.linspace(a-THREE_HALFS*rng, b+THREE_HALFS*rng, num_points)
            y = [self.f(xi) for xi in x]
            return x, y
        except Exception as e:
            raise ValueError(f"Error generating plot points: {str(e)}")
