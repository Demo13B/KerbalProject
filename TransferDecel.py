import krpc
import time
import math

# Opening connection to a server, setting up variables
conn = krpc.connect(name='Transfer deceleration')
vessel = conn.space_center.active_vessel
control = vessel.control
ut = conn.add_stream(getattr, conn.space_center, 'ut')
node = control.nodes[0]
delta_v = node.delta_v
 

# Calculating burn time (using rocket equation)
F = vessel.available_thrust
Isp = vessel.specific_impulse * 9.82
m0 = vessel.mass
m1 = m0 / math.exp(delta_v/Isp)
flow_rate = F / Isp
burn_time = (m0 - m1) / flow_rate
print('Burn time calculated')
 
 
# Waiting until burn
print('Waiting until maneuver burn')
burn_ut = node.ut - (burn_time/2)
lead_time = 30
conn.space_center.warp_to(burn_ut - lead_time)

 
# Orientating the ship
control.sas = True
print('SAS engaged')
time.sleep(1)
control.sas_mode = conn.space_center.SASMode.retrograde
print('SAS set to retrograde')
control.rcs = True
print('RCS engaged')
  

# Executing burn
print('Ready to execute burn')
while ut() < burn_ut:
	pass
print('Executing burn')
control.throttle = 1.0
time.sleep(burn_time)
print('The maneuver is successfully completed')
control.throttle = 0
node.remove()
control.rcs = False
print('RCS disengaged')
control.sas = False
print('SAS disengaged')

