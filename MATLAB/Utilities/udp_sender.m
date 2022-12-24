clear; clc;
localHost = '127.0.0.1';
port = 25000;

% MQTT parameters
BROKER = "tcp://mqtt.eclipseprojects.io";
BROKER_PORT = 1883;

% UDP communication object
udp_simulink = udpport;

% MQTT communication object
mqttClient = mqttclient(BROKER,Port=BROKER_PORT);
% Subscribing to all the subtopics of "YONDU/DroneCommand/"
mySub = subscribe(mqttClient,"YONDU/DroneCommand/#");

% Index association of each topic
gesture_table = table;
gesture_table.takeoff = 1;
gesture_table.landing = 2;
gesture_table.vx = 3;
gesture_table.vy = 4;
gesture_table.vz = 5;
gesture_table.v_yaw = 6;


while true
    % Initializing the commands to be sent
    commands = zeros(1,6);

    % Reading message available on MQTT server
    mqttMsg = read(mqttClient);
    % Getting the number of message available
    h = height(mqttMsg);
    % If at least one message is available
    if h ~= 0
        % We get through all the messages starting from the oldest one (the
        % one at the end of the table)
        for i = h:-1:1
            % We get the topic on which is has been published
            topic = extractAfter(mqttMsg.Topic(i), "DroneCommand/");
            % We get the value published on the topic
            value = mqttMsg.Data(i);
            % We set the command as published on the server
            commands(1,gesture_table(1,topic).Variables) = value;
        end
    end

    % We send the commands to Simulink
    write(udp_simulink, commands, "int8", localHost, port)
    fprintf("\t Tf\t  Ld\t vx\t  vy\t vz\t  vw\n");
    disp(commands)
    % Waiting 0.5 second
    pause(0.5);
end

 
