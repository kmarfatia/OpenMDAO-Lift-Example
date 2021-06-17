#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 11:51:06 2021

@author: kmarfatia
"""

# testing the lift program with values from the Concorde
# wingspan of concorde is 26 m; AR = 1.55
# the lift coefficient at supersonic cruise is 0.125.(about 600 m/s)
# air density at 60k feet is 0.0003097 kg/m**3

# approx values from test run. 

import numpy as np
import unittest
import os

import openmdao.api as om
from openmdao.utils.assert_utils import assert_near_equal

import pycycle.api as pyc 

from Lift_AR_NASA.py import Lift
from Lift_AR_NASA.py import Surface_Area

class LiftTestCase(unittest.TestCase):
    
    def benchmark_case1(self):
        
        prob = om.Problem()
        
        prob.model = LiftEq = Lift()
        
        prob.setup()
        
        # initial conditions
        prob.set_val('b', 26, units='m')
        prob.set_val('AR', 1.55)
        
        prob.set_val('CL', 0.125)
        prob.set_val('rho', 0.0003097, units='kg/m**3')
        prob.set_val('S', 0.0, units='m**2')
        prob.set_val('V', 600, units='m/s')
        
        
        
        prob.run_model()
        tol = 1e-5
        print()
        
        
        reg_data = 
        ans = prob['q']
        print('q:', reg_data, ans)
        assert_near_equal(ans, reg_data, tol)
        
        
        reg_data = 
        ans = prob['L']
        print('L:', reg_data, ans)
        assert_near_equal(ans, reg_data, tol)
        
        
        reg_data = 
        ans = prob['S']
        print('S:', reg_data, ans)
        assert_near_equal(ans, reg_data, tol)
        
        
if__name__ == "__main__":
    unittest.main()
            
        
        