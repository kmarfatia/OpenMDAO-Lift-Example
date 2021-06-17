#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  3 12:23:46 2021

@author: kmarfatia
"""

# testing the lift program with values from the Concorde
# wingspan of concorde is 26 m; AR = 1.55
# the lift coefficient at supersonic cruise is 0.125.(about 600 m/s)
# air density at 60k feet is 0.0003097 kg/m**3


import openmdao.api as om 

class Surface_Area(om.ExplicitComponent):
    """calculating surface area using wingspan and aspect ratio"""

    def setup(self):
        
        #inputs
        self.add_input('b', 26, units="m", desc="wingspan")
        self.add_input('AR', 1.55, desc="aspect ratio")

        #outputs
        self.add_output('S', 0.0, units="m**2",
                        desc="surface area of wing")

    def setup_partials(self):
        self.declare_partials('S', ['AR', 'b'], dependent=True, method='cs')
    
    def compute(self, inputs, outputs):
        
        b = inputs['b']
        AR = inputs['AR']
    
        outputs['S'] = S = b**2 / AR
        
    def compute_partials(self, inputs, partials):   
        
        pass 

    
class Lift(om.ExplicitComponent):
    """equation to calculate lift"""

    def setup(self):

        # Inputs
        self.add_input('CL', 0.125, desc="lift coefficient")
        self.add_input('rho', 0.0003097, units="kg/m**3", desc="air density")
        self.add_input('V', 600.0, units="m/s", desc="velocity")
        self.add_input('S', 0.0, units="m**2", desc="surface area of wing")
        

        # Outputs
        self.add_output('q', 0.0, units="kg/(m*s**2)",
                        desc="dynamic pressure")
        self.add_output('L', 0.0, units="(kg*m)/s**2",
                        desc="Lift")
       
    def setup_partials(self):
        self.declare_partials('q', ['rho', 'V'], dependent=True, method='cs')
        self.declare_partials('L', ['CL', 'S', 'rho', 'V'], dependent=True, method='cs')
        
    def compute(self, inputs, outputs):

      
        rho = inputs['rho']
        V = inputs['V']
        CL = inputs['CL']
        S = inputs['S']

        outputs['q'] = q = 0.5 * rho * V**2
        
        outputs['L'] = L = CL * S * q
        
    def compute_partials(self, inputs, partials):   
        
        pass 

prob = om.Problem()
model= prob.model

model.add_subsystem('S', Surface_Area(),
                        promotes_inputs=['b', 'AR'],
                        promotes_outputs=['S',])

model.add_subsystem('L', Lift(),
                        promotes_inputs=['V', 'rho', 'CL', 'S'], 
                        promotes_outputs=['q', 'L'])
                        
prob.setup()
prob.run_model()

data = prob.check_partials()

print(prob.get_val('q'))
print(prob.get_val('S'))
print(prob.get_val('L'))




