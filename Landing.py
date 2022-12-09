import krpc 
import time
import math

# Opening connection to a server, setting up variables
conn = krpc.connect(name='Duna landing')
vessel = conn.space_center.active_vessel
control = vessel.control

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
control.sas = False
print('SAS disengaged')


# Deploying parachutes 
while surf_altitude() > 3000:
	pass
control.activate_next_stage()
print('Parachutes deployed')


# Detaching parachutes
while surf_altitude() > 0:
	pass
control.activate_next_stage()
print('Parachutes detached')
time.sleep(5)
print('Landing succesfully completed')

