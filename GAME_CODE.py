#ROCKET LAUNCH AND REVOLVE GAME IN PYTHON
# --------------------
%matplotlib notebook
def norm(vec):
    """Unit aware vector norm (magnitude)"""
    return np.sqrt(np.sum(vec**2.0))
# Include import statements and unit registry from above
# (Remove the above line for Spyder; 
# you will need to type '%matplotlib qt' into the command window instead.)
def event_handler(event):
        global T_angle
        if event.key==',': # press comma to rotate left
            # Rotate left (increase angle)
            T_angle += 10.0*ur.degree
            pass
        elif event.key=='.': # press period to rotate right
            # Rotate right (decrease angle)
            T_angle -= 10.0*ur.degree
            pass
        elif hasattr(event,"button") and event.button==1:
            if event.xdata < 0.0: 
                # Click on left-half of plot to
                # Rotate left (increase angle)
                T_angle += 10.0*ur.degree
                pass
            else:
                # Click on right-half of plot to
                # Rotate right (decrease angle)
                T_angle -= 10.0*ur.degree
                pass
            pass
        
        pass 
import numpy as np
from matplotlib import pyplot as pl
import pint
ur = pint.UnitRegistry() # Import pint and create unit registry

# Include Rocket and planet characteristics; physics constants
empmass=29500*ur.kg
payload=1000*ur.kg
fuelm=480000*ur.kg
TSFC=3.5*(10**-4)*(ur.s/ur.m)
Fullt=7600*ur.kN
G=6.674*(10**-11)*(ur.m**3)/((ur.kg)*(ur.s**2))
Earthm=(5.98*(10**24))*ur.kg


# Include earth diameter, surface speed, initial rocket position,
# initial rocket velocity
# Earth's diameter is given by
d_earth = 12.7e6*ur.m 
pos = np.array((0.0,d_earth.to(ur.m).magnitude/2.0))*ur.m
v_surface = 460.0*ur.m/ur.s # at the equator
vel=np.array((v_surface.magnitude,0.00))*ur.m/ur.s
# and Earth's tangential speed (due to rotation) is 
# approximately
# Define initial thrust angle and direction
T_angle = 60.0*ur.degree # 60 deg. CCW from horizontal
T_direc=np.array(((np.cos(T_angle)).to(ur.radian).magnitude,(np.sin(T_angle).to(ur.radian)).magnitude))


# Include code for the baseline plot and initial arrow
pl.ion() # interactive mode ON
fig = pl.figure()
pl.axis((-1e6,1e6,6e6,7e6)) # Define axis bounds in (assumed) meters
pl.grid(True) # Enable grid

# create green filled circle representing earth
earth = pl.Circle((0,0),float(d_earth/2.0/ur.m),color='g')
fig.gca().add_artist(earth)

# Add your Arrow-drawing code here

# Include the event handler
arrowplt=pl.arrow(pos[0]/ur.m, pos[1]/ur.m, T_direc[0]*500000, T_direc[1]*500000,width=100000)
t=0.0 * ur.s # Start at t=0

# Loop until ctrl-C or press stop button on 
# Spyder console or t exceeds 36000 seconds (10 hours
# of simulated time)

while t < 36000 * ur.s: 

   # Connect this event handler to the figure so it is called
   # when the mouse is clicked or keys are pressed. 
    fig.canvas.mpl_connect('key_press_event',event_handler)
    fig.canvas.mpl_connect('button_press_event',event_handler)
    T_direc=np.array(((np.cos(T_angle)).to(ur.radian).magnitude,(np.sin(T_angle).to(ur.radian)).magnitude))
    pl.title("Fuel remaining %f kg" % (fuelm.magnitude))
    #  * Show the time in the x axis label, e.g.
    pl.xlabel("Time = %f s" % (t.magnitude))
# Connect this event handler to the figure so it is called
# when the mouse is clicked or keys are pressed.
    # Select the time step (code above)
    if fuelm!=0:
        dt=1*ur.s#ascent
    else:
        dt=10*ur.s#descent(my mod)
    # Update the plot:
    #t+=dt
    arrowplt.remove()
    
    #  * Call arrowplt.remove() method on the old arrow
    #  * Calculate the thrust (rocket) direction from
    #    the rocket angle (code way above)
    if fuelm >0:
        thrust_mag=Fullt
    else:
        thrust_mag=0*ur.kN
    thrust_vec=thrust_mag*T_direc
    #  * Plot the new arrow (code way above)
    arrowplt=pl.arrow(pos[0]/ur.m, pos[1]/ur.m, T_direc[0]*500000, T_direc[1]*500000,width=100000)
    print(arrowplt)
    
    #  * Label the fuel state in the plot title, e.g.
    #    pl.title("Fuel remaining %f kg" % ())
    #  * Show the time in the x axis label, e.g.
    #    pl.xlabel("Time = %f s" % ())
    #  * Select the plot region according to fuel state (code above)
    if fuelm!=0:#zoomin
        pl.axis((-1e6,1e6,6e6,7e6))
    else:
        pl.axis((-100e6,+100e6,-100e6,+100e6))
    
    # These next two lines cause the plot display to refresh
    fig.canvas.draw()
    fig.canvas.flush_events()

    # Determine the forces on the rocket (code above): 
    r = norm(pos)#aldready in m
    F_Gravity = ((G/r**2)*((Earthm)*(empmass+payload+fuelm)))
    #  * Calculate the magnitude of the force of gravity
    #  * Calculate the direction of the force of gravity
    Direc_Gravity = -(pos/norm(pos))
    Vec_Gravity = F_Gravity*Direc_Gravity
    #    and gravity vector on the rocket
    #  * Calculate the thrust vector
    if fuelm>0:
        dm_f=-TSFC*thrust_mag*dt
        fuelm+=dm_f
    elif fuelm<=0:
        fuelm=0*ur.kg
    # Update the fuel mass (code above)
    
    # Determine the change in velocity (code above)
    F=thrust_vec-(F_Gravity*Direc_Gravity)
    print(F)
    a=F/(empmass+payload+fuelm)
    dv=a*dt
    vel+=dv
    print(vel)
    # Determine the change in position (code above)
    dpos=vel*dt
    pos+=dpos
    t = t + dt # Update the time
    pass  # End of loop block