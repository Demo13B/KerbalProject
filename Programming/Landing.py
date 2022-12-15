import krpc 
import time
import math

# Opening connection to a server, setting up variables
conn = krpc.connect(name='Duna landing')
vessel = conn.space_center.active_vessel
control = vessel.control
antenna = vessel.parts.with_tag('radio')


# Creating useful stream variables
altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
surf_altitude = conn.add_stream(getattr, vessel.flight(), 'surface_altitude')


# Seperating cruise engine
control.activate_next_stage()
print('Cruise engine seperated')


# Stabilizing capsule before atmosphere entry
while altitude() > 50000:
	pass
control.sas = True
print('SAS engaged')
time.sleep(1)
control.sas_mode = conn.space_center.SASMode.retrograde
print('SAS set to retrograde')
control.rcs = True
print('RCS engaged')


# Opening capsule after atmosphere entrance
while altitude() > 10000:
	pass
control.activate_next_stage()
print('Capsule opened')
control.rcs = False
print('RCS disengaged')
control.sas_mode = conn.space_center.SASMode.stability_assist
print('SAS disengaged')


# Deploying parachutes 
while surf_altitude() > 3000:
	pass
control.activate_next_stage()
print('Parachutes deployed')


# Final engine braking and touchdown
while surf_altitude() > 50:
	pass
control.throttle = 0.1
print('Braking engines activated')
while surf_altitude() > 3:
	pass
control.throttle = 1
control.activate_next_stage()
print('Parachute detached')
time.sleep(5)
control.activate_next_stage()
control.sas = False
antenna[0].antenna.deployed = True
print('Antenna has been deployed')
print('Landing successful! Welcome to Dune!')

