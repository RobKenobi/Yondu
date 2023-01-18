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
dronez = 0.01;       % m 
%% Drone Properties

% Material used
rho   = 1.25;            % g/cm^3 

% Approximate Drone mass 
drone_mass = 0.805;     % kg


%% Propeller parameters
propeller.diameter = 0.160; % m
propeller.Kthrust  = 2.98*10^(-1); 
propeller.Kdrag    = 1.14*10^(-2);
% propeller.diameter = 0.254; % m
% propeller.Kthrust  = 0.1072; 
% propeller.Kdrag    = 0.01;


rho_air        = 1.225;  % kg/m^3
air_temperature    = 273+25; % degK
wind_speed         = 0;      % Wind speed (m/s)

%% Battery and motors

% Battery Capacity
battery_capacity = 7.6*3;
battery_nominal_voltage = 12; % V
battery.internal_R = 2e-2; % Ohm
battery_V1 = 10; % V

% Motor parameters
motor.max_torque = 0.8;  % N*m
motor.max_power  = 160;  % W
motor.time_const = 0.02; % sec
motor.efficiency = 25/30*100; 
motor.efficiency_speed = 500; % rpm
motor.efficiency_torque = 0.05; % N*m
motor.rotor_damping  = 1e-7; % N*m/(rad/s)

max_power = motor.max_power;

% % Motor parameters
% motor.max_torque = 0.8;  % N*m
% motor.max_power  = 160;  % W
% motor.time_const = 0.02; % sec
% motor.efficiency = 25/30*100; 
% motor.efficiency_speed = 5300; % rpm
% motor.efficiency_torque = 0.05; % N*m
% motor.rotor_damping  = 1e-7; % N*m/(rad/s)
%% Controller parameters battery

kp_motor       = 0.00375;
ki_motor       = 4.50000e-4;
kd_motor       = 0;
filtD_motor    = 10000;
filtSpd_motor    = 0.001;
limit_motor    = 0.25;


received_command = 1
cmd_gain = 1