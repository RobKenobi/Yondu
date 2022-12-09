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
drone_mass = 2;     % kg


%% Propeller parameters
propeller.diameter = 0.160; % m
propeller.Kthrust  = 0.1072; 
propeller.Kdrag    = 0.01;

rho_air        = 1.225;  % kg/m^3
air_temperature    = 273+25; % degK
wind_speed         = 0;      % Wind speed (m/s)

%% Battery and motors

% Battery Capacity
battery_capacity = 7.6*3;
battery_nominal_voltage = 14; % V
battery.internal_R = 2e-2; % Ohm
battery_V1 = 11.5; % V

% Motor parameters
motor.max_torque = 0.8;  % N*m
motor.max_power  = 160;  % W
motor.time_const = 0.02; % sec
motor.efficiency = 25/30*100; 
motor.efficiency_speed = 5000; % rpm
motor.efficiency_torque = 0.05; % N*m
motor.rotor_damping  = 1e-7; % N*m/(rad/s)

max_power = motor.max_power;


%% Controller parameters
filtM_position = 0.005;
kp_position    = 8;
ki_position    = 0.04;
kd_position    = 3.2;
filtD_position = 100;
pos2attitude   = 2.4;

filtM_attitude = 0.01;
kp_attitude    = 128.505;
ki_attitude    = 5.9203;
kd_attitude    = 78.2000*2;
filtD_attitude = 1000;
limit_attitude = 800;

filtM_yaw      = 0.01;
kp_yaw         = 25.7010*4*2;
ki_yaw         = 5.9203*0.01;
kd_yaw         = 78.2000*0.01;
filtD_yaw      = 100;
limit_yaw      = 20;

filtM_altitude = 0.05;
kp_altitude    = 0.27;
ki_altitude    = 0.07;
kd_altitude    = 0.35;
filtD_altitude = 10000;
limit_altitude = 10;

kp_motor       = 0.00375;
ki_motor       = 4.50000e-4;
kd_motor       = 0;
filtD_motor    = 10000;
filtSpd_motor    = 0.001;
limit_motor    = 0.25;

%% Drag coefficients
qd_drag.Cd_X = 0.35;
qd_drag.Cd_Y = 0.35;
qd_drag.Cd_Z = 0.6;
qd_drag.Roll = 0.2;
qd_drag.Pitch = 0.2;
qd_drag.Yaw = 0.2;
qd_area.YZ = 0.0875;
qd_area.XZ = 0.0900;
qd_area.XY = 0.2560;
qd_area.Roll = qd_area.XY*2;
qd_area.Pitch = qd_area.XY*2;
qd_area.Yaw = qd_area.XY;

