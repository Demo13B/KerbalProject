import krpc
import time
import math

# Setting target orbut altitude
target_altitude = 100000


# Opening connection to a server, setting up variables
conn = krpc.connect(name='Orbital launch')
vessel = conn.space_center.active_vessel
ap = vessel.auto_pilot
control = vessel.control
panels = vessel.parts.with_tag('sol')


# Creating useful stream variables
ut = conn.add_stream(getattr, conn.space_center, 'ut')
altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
periapsis = conn.add_stream(getattr, vessel.orbit, 'periapsis_altitude')
stage_8_resources = vessel.resources_in_decouple_stage(stage=8, cumulative=False)
srb_fuel = conn.add_stream(stage_8_resources.amount, 'SolidFuel')
srb_sep = False


# Setting up auto-pilot and starting engines
control.throttle = 1
time.sleep(1)
ap.target_pitch_and_heading(90, 90)
ap.engage()
print('3...')
time.sleep(1)
print('2...')
time.sleep(1)
print('1...')
time.sleep(1)
print('Launch')
control.activate_next_stage()


# Executing gravity turn
for step in range(1, 10):
	while altitude() < 10000 + (step - 1) * 3333:
		if not srb_sep and srb_fuel() < 0.1:
			control.activate_next_stage()
			srb_sep = True
			print('Boosters seperated')
			pass
		continue
	new_angle = step * 10
	ap.target_pitch_and_heading(90 - new_angle, 90)


# Burning until apoapsis reaches target orbit altitude
while apoapsis() < target_altitude:
	pass
control.throttle = 0
print('Target apoapsis reached. ')


# Seperating the first cover
while altitude() < 71000:
	pass
control.activate_next_stage()


# Planning circularization burn (using vis-viva equation)
print('Planning circularization burn')
mu = vessel.orbit.body.gravitational_parameter
r = vessel.orbit.apoapsis
a1 = vessel.orbit.semi_major_axis
a2 = r
v1 = math.sqrt(mu*((2./r)-(1./a1)))
v2 = math.sqrt(mu*((2./r)-(1./a2)))
delta_v = v2 - v1
node = control.add_node(ut() + vessel.orbit.time_to_apoapsis, prograde=delta_v)


# Calculating burn time (using rocket equation)
F = vessel.available_thrust
Isp = vessel.specific_impulse * 9.82
m0 = vessel.mass
m1 = m0 / math.exp(delta_v/Isp)
flow_rate = F / Isp
burn_time = (m0 - m1) / flow_rate
 
# Orientating the ship
ap.disengage()
print('Auto Pilot disengaged')
control.sas = True
print('SAS engaged')
time.sleep(1)
control.sas_mode = conn.space_center.SASMode.prograde
print('SAS set to prograde')

# Waiting until burn
print('Waiting until circularization burn')
burn_ut = ut() + vessel.orbit.time_to_apoapsis - (burn_time/2)
lead_time = 5
conn.space_center.warp_to(burn_ut - lead_time)

# Executing burn
print('Ready to execute burn')
time_to_apoapsis = conn.add_stream(getattr, vessel.orbit, 'time_to_apoapsis')
while time_to_apoapsis() - (burn_time/2) > 0:
	pass
print('Executing burn')
control.throttle = 1.0
time.sleep(burn_time)
print('The vessel is successfully parked at ', target_altitude // 1000,' km orbit')
control.throttle = 0
control.remove_nodes()

# Removing take-off stage
time.sleep(5)
print('Seperating take-off stage')
control.activate_next_stage()
time.sleep(1)
control.activate_next_stage()
control.throttle = 0.5
time.sleep(1)
vessel.control.throttle = 0
print('Take-off stage seperated')
control.sas = False
print('SAS disengaged')
panels[0].solar_panel.deployed = True
panels[1].solar_panel.deployed = True
panels[2].solar_panel.deployed = True
panels[3].solar_panel.deployed = True
print('Solar panels deployed')

