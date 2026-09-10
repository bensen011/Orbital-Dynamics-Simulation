'''
This is an independent project where I am aiming to create a simulation of a satellite orbiting a planet

Objective 1.: Simulate a satellite orbiting a planet

Objective 2.: Going from an elliptical orbit to a Circular orbit (stabilising)

Planet Parameters:
    - g = Gravity of Planet [m/s^2]
    - R = Radius of Planet [km]
    - M = Mass of Planet []

Satellite Parameters:
    - m = Mass of Satellite
    - r_p = Periapsis Radius (closest orbit)
    - r_a = Apoapsis Radius (furthest orbit)
    - T = Orbital Period
    - v_orbital_t = Orbital Velocity at Time t

Assumptions:
    - Assume mass of planet is constant
    - Assume no other gravitational pulls on satellite

======================    

'''

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import csv

print('=====================================')
print('               Welcome               ')
print('=====================================')
print('This is a Simulation of an Satellites Orbit')
input('Please type [ENTER] to begin: ').lower()

def select_planet():
    planets_data ={}

    with open('Planets.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            planets_data[row['Planet'].lower()] = {
                'M': float(row['Mass_kg']),
                'R': float(row['Radius_m']),
                'g': float(row['Gravity_m_s2']),
                'color': (row['Color'])
            }

    available_planets = list(planets_data.keys())

    print('=====================================')
    
    print(f"\nAvailable Celestial Bodies: \n{', '.join(available_planets).title()}")

    choice = input('\nType the name of the body you want to orbit: ').lower()


    while choice not in planets_data:
        print('\nERROR: Body not found in database\n')
        choice = input("Please try again: ").lower()

    print(f"\n>>> Loading parameters for {choice.title()}... <<<")

    planets_data[choice]['name'] = choice.title()
    return planets_data[choice]


def orbital_type(r_p, r_a):

    e = (r_a - r_p)/(r_a + r_p)
    a = (r_a + r_p)/2

    if e == 0:
        orbit = 'Circular'

    elif 0 < e < 1:
        orbit = 'Elliptical'

    elif e == 1:
        orbit = 'Parabolic'

    elif e > 1:
        orbit = 'Hyperbolic'

    else:
        
        print('\nERROR: r_p > r_a: ')
        
        return
        

    return a, r_p, r_a, orbit, e


selected = select_planet()


G = 6.6743e-11      # Gravitational Constant
g = selected['g']       # Gravity of Planet [m/s^2]
R = selected['R']      # Average Radius of Planet [km]
M = selected['M']      # Mass of Planet [kg * 10^24]

def radius():
    print(f"\nRadius of {selected['name']}: {R/1e6:.1f} [Mm]. \nRecommended Apsides: \n - Periapsis ≈ {2*selected['R']/1e6:.1f} [Mm] \n - {2*selected['R']/1e6:.1f} <= Apoapsis < {10*selected['R']/1e6:.1f} [Mm] ")


    r_p =  float(input('\nEnter Periapsis altitude (Mm from surface): ')) *1e6        # Periapsis Radius [Mm]
    r_a = float(input('Enter Apoapsis altitude (Mm from surface): ')) *1e6       # Apoapsis Radius [Mm]


    if r_p > r_a:
        print('\nERROR: r_a < r_p:') 
        print('\nPlease try again: ')
        return radius()

    return r_p, r_a

r_p, r_a = radius()

R_p = r_p + R       # Periapsis Radius + Planets Radius
R_a = r_a + R       # Apoapsis Radius + Planets Radius

a, _, _, orbit_type, e = orbital_type(R_p, R_a)
T = 2*np.pi*np.sqrt(a**3/(G*M))


def kepler(t, a, e):

    mu = np.sqrt(G*M/a**3) * t
    E = mu

    for i in range(5):

        E_new = E - (E - e*np.sin(E) - mu)/(1 - e*np.cos(E))
        E = E_new

    r_t = a*(1 - e*np.cos(E))

    vu = 2*np.arctan(np.sqrt((1+e)/(1-e))*np.tan(E/2))


    x = r_t * np.cos(vu) 
    y = r_t * np.sin(vu)

    return (int(x),int(y))

    
dt = 60
n = 2       # No. of orbits


def orbit():

    coords = []

    num_frames = int(T/dt)

    times = np.linspace(0, T, num_frames)
    
    for t in times:
        
        coords.append(kepler(t, a, e))

        t = t+ dt
        if t >= T:
            t = t - T

    return coords


def terminal_display():

    '''print('\nCoords Check:')
    print('==============')
    if R_p-10 <= coords[0][0] <= R_p+10:
        if -10 <= coords[0][1] <= 10:
            print('Starting (Periapsis) Coords: CORRECT')
        else:
            print('Starting (Periapsis) y-Coords: FAIL')
    else:
        print('Starting (Periapsis) x-Coords: FAIL')
    print(coords[0])
    print('')
    if -R_a-1e6 <= coords[int(T/(2*dt))][0] <= -R_a+1e6:
        if -1e6 <= coords[int(T/(2*dt)+1)][1] <= 1e6:
            print('Apoapsis Coords: CORRECT')
        else:
            print('Apoapsis y-Coords: FAIL')
    else:
        print('Apoapsis x-Coords: FAIL')
    print(coords[int(T/(2*dt))])
    print('')
    if R_p-1e6 <= coords[-1][0] <= R_p+1e6:
        if -1.5e6 <= coords[-1][1] <= 1.5e6:
            print('Final (Periapsis) Coords: CORRECT')
        else:
            print('Final (Periapsis) y-Coords: FAIL')
    else:
        print('Final (Periapsis) x-Coords: FAIL')
    print(coords[int(-1)])'''

    print('=====================================\n')

    print('Planet Parameters:')
    print(f'g = {g} [m/s^2], R = {R/1e6} [Mm], M = {M} [kg], G = {G} [-]')
    print('Orbital Type:', orbital_type(R_p, R_a)[3])
    print(f'R_p: {R_p/1e6} [Mm], R_a: {R_a/1e6} [Mm], a = {a/(1e6)} [km]')
    print('=====================================')


coords = orbit()


def stabilisation(location):

    a_0 = orbital_type(R_p, R_a)[0]

    if location == 'periapsis':
        target_r = R_p
        time_offset = 0
    else:
        target_r = R_a
        time_offset = np.pi*np.sqrt(target_r**3 / (G*M))

    v_0 = np.sqrt(G*M*(2/target_r - 1/a_0))
    v_target = np.sqrt(G*M/target_r)

    delta_v = float(v_target - v_0)     # Speed change required to change trajectory

    a_stable, _, _, _, e_stable = orbital_type(target_r, target_r)

    
    T_stable = 2*np.pi*np.sqrt(a_stable**3/(G*M))

    stablised_coords =[]

    num_frames = int(T_stable/dt)
    times = np.linspace(0, T_stable, num_frames)

    for t in times:
        stablised_coords.append(kepler(t + time_offset, a_stable, e_stable))


    return delta_v, a_stable, e_stable, stablised_coords, v_target, T_stable


def maneuver_choice():

    while True:
        print('\nManeuver Options: ')
        print(' [P] - Stabilise at Periapsis')
        print(' [A] - Stabilise at Apoapsis')
        print(' [M] - Maintain current orbit')

        choice = input('Select Option: ').lower()

        if choice == 'p' or choice == 'a':
            location = 'periapsis' if choice == 'p' else 'apoapsis'

            delta_v, a_stable, e_stable, stabilised_coords, v_target, T_stable = stabilisation(location)

            print('=====================================')
            return stabilised_coords, location

        elif choice == 'm':
            print('=====================================')
            return [], 'none'

        else:
                print('\nWrong Input. Please try again...')
    





terminal_display()

stabilised_coords, user_choice = maneuver_choice()

if user_choice != 'none':
    delta_v, a_stable, e_stable, stabilised_coords, v_target, T_stable = stabilisation(user_choice)


def plotting_orbit():

    x_vals_coords = [coord[0] for coord in coords]
    y_vals_coords = [coord[1] for coord in coords]

    x_vals_stabilised = [coord[0] for coord in stabilised_coords]
    y_vals_stabilised = [coord[1] for coord in stabilised_coords]

    theta = np.linspace(0, 2*np.pi, 100)
    x_planet = R*np.cos(theta)
    y_planet = R*np.sin(theta)

    # Animation

    fig, ax = plt.subplots()
    ax.plot(x_vals_coords, y_vals_coords, label='Orbit Path', ls=(0, (2,4)), color='red', alpha=0.7)

    if user_choice == 'periapsis' or user_choice == 'apoapsis':
        ax.plot(x_vals_stabilised, y_vals_stabilised, label='Stabilised Path', ls=(0, (2,4)), color='green', alpha=0.7)

    
    ax.fill(x_planet, y_planet, color = selected['color'], label=selected['name'])
    ax.plot(R_p, 0, 'o', label='Periapsis', color='darkviolet')
    ax.plot(-R_a, 0, 'o', label='Apoapsis', color='royalblue')
    ax.axis('equal')
    plt.style.use('dark_background')
    plt.title('Satellite Orbit Simulation')
    ax.legend(loc='lower left')
    ax.set_facecolor('black')
    
    
    orbital_text = ax.text(0.05, 0.95, '', transform=ax.transAxes, color='white', verticalalignment='top')
    satellite_dot, = ax.plot([], [], marker='h', color='gold', markersize=10, label='Satellite')
    trail, = ax.plot([], [], color='orange', lw=2)

    trail_x, trail_y = [], []

    def animate(i):

        # --- Telemetry Output ---

        delay = 75

        if user_choice == 'periapsis':
            if i == (len(coords) // 2):
                print('\n>>> Calculating Periapsis maneuver... <<<')
            if i == (len(coords) // 2 +delay):
                print(f' > Target Radius: {a_stable/1e6:.1f} [Mm]')
            if i == (len(coords) * 5 // 8):
                print('\n.Calculating velocity needed...')
            if i == (len(coords) * 5 // 8 + delay):
                print(f' > Velocity needed: {v_target/1e3:.2f} [km/s]')
                print(f' > ∆V = {delta_v/1e3:.2f} [km/s]')
        
        elif user_choice == 'apoapsis':
            if i == len(coords):
                print('\n>>> Calculating Apoapsis maneuver... <<<')
                print(f' > Target Radius: {a_stable/1e6:.1f} [Mm]')
            if i == (len(coords) * 9 // 8):
                print('\nCalculating velocity needed...')
            if i == (len(coords) * 9 // 8 + delay):
                print(f' > Velocity needed: {v_target/1e3:.2f} [km/s]')
                print(f' > ∆V = {delta_v/1e3:.2f} [km/s]')
        
        # -----------------------------


        tl = 0.035

        if user_choice == 'periapsis' and i >=len(coords):

            if i == len(coords):
                print(f'\n>>> Orbit Stabilised at Periapsis <<<')
            if i == (len(coords) + delay):
                print(f' > Orbital Radius: {a_stable/1e6:.2f} [Mm]')
                print(f' > Velocity: {v_target/1e3:.2f} [km/s]')
                print(f' > Orbital Period: {T_stable/3600:.2f} [hrs]')
            
            loop_index = (i - len(coords)) % len(stabilised_coords)
            current_x = stabilised_coords[loop_index][0]
            current_y = stabilised_coords[loop_index][1]
            trail_length = int(tl * len(stabilised_coords))
            current_a = R_p


        elif user_choice == 'apoapsis' and i >= (3*len(coords) // 2):

            if i == (3*len(coords) // 2):
                print('\n>>> Orbit Stabilised at Apoapsis <<<')
            if i == (3*len(coords)// 2 + delay):
                print(f' > Orbital Radius: {a_stable/1e6:.2f} [Mm]')
                print(f' > Velocity: {v_target/1e3:.2f} [km/s]')
                print(f' > Orbital Period: {T_stable/3600:.2f} [hrs]')

            loop_index = (i - (3*len(coords) // 2)) % len(stabilised_coords)
            current_x = stabilised_coords[loop_index][0]
            current_y = stabilised_coords[loop_index][1]
            trail_length = int(tl * len(stabilised_coords))
            current_a = R_a

        else:
            if i == 1:
                print('\n>>> Maintaining Orbit <<<')
            if i == 50:
                print(f' > Orbit Type: {orbit_type}')
                print(f' > Average Radius: {a/1e6:.2f} [Mm]')
                print(f' > Orbital Period: {T/3600:.2f} [hrs]')

            loop_index = i % len(coords)
            current_x = coords[loop_index][0]
            current_y = coords[loop_index][1]
            trail_length = int(tl * len(coords))
            current_a = a


        satellite_dot.set_data([current_x], [current_y])

        trail_x.append(current_x)
        trail_y.append(current_y)

        while len(trail_x) > trail_length:
            trail_x.pop(0)
            trail_y.pop(0)
        trail.set_data(trail_x, trail_y)

        current_time_hrs = (i *dt)/3600

        r = np.sqrt(current_x**2 + current_y**2)
        current_velocity = np.sqrt(G*M*(2/r - 1/current_a))

        orbital_text.set_text(f"Time: {current_time_hrs:.2f} hrs\nVelocity: {current_velocity/1000:.2f} km/s")
        
        return satellite_dot, orbital_text, trail

    ani= animation.FuncAnimation(fig, animate, frames = 100000, interval = 1, blit =False)
    plt.show()


plotting_orbit()

print('\n\n=====================================')
print('         Thank you, Goodbye          ')
print('        Created By Ben Senior        ')
print('=====================================')





    