#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  3 12:23:46 2021

@author: kmarfatia
"""

# A Boeing 747 is flying at an altitude of 10,000 meters and has a velocity of 250 m/s. The aircraft has a wing area of
# 541.2 m^2. The coefficient of lift is 0.52 and the density is of air at 12,192 meters is approximately 0.30267 kg/m3. The
# weight of the 747 is 2,833,500 N (637,000 pounds). Solve for lift. 

# The aspect ratio of a Boeing 747-400 is ~ 7.7
# The wingspan of a Boeing 747-400 is 64.4 meters.


import openmdao.api as om 

class Surface_Area(om.ExplicitComponent):
    """calculating surface area using wingspan and aspect ratio"""

    def setup(self):
        
        #inputs
        self.add_input('b', 64.4, units="m", desc="wingspan")
        self.add_input('AR', 7.7, desc="aspect ratio")

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
        self.add_input('CL', 0.52, desc="lift coefficient")
        self.add_input('rho', 0.4135, units="kg/m**3", desc="air density")
        self.add_input('V', 250.0, units="m/s", desc="velocity")
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


print(prob.get_val('S'))
print(prob.get_val('L'))

#n2 diagram below. 


