%% Environment setup

% Size of the ground
planex = 4;           % m
planey = 4;            % m
planedepth = 0.1;       % m

% Size of the walls
wally = 4;      % m
wallz = 2.5;        % m
walldepth = 0.1;        % m

% Drone initial position
dronez = 0.2;       % m 
%% Drone Properties

% Material used
rho   = 1.25;            % g/cm^3 

% Approximate Drone mass 
drone_mass = 1;     % kg


%% Propeller parameters
propeller.diameter = 0.254; % m
propeller.Kthrust  = 0.1072; 
propeller.Kdrag    = 0.01;

air_rho            = 1.225;  % kg/m^3
air_temperature    = 273+25; % degK
wind_speed         = 0;      % Wind speed (m/s)


%% Battery and motors

% Battery Capacity
battery_capacity = 7.6*3;

% Motor parameters
motor.max_torque = 0.8;  % N*m
motor.max_power  = 160;  % W
motor.time_const = 0.02; % sec
motor.efficiency = 25/30*100; 
motor.efficiency_spd = 5000; % rpm
motor.efficiency_trq = 0.05; % N*m
motor.rotor_damping  = 1e-7; % N*m/(rad/s)

max_power = motor.max_power;