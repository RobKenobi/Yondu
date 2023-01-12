from djitellopy import Tello

drone = Tello()
drone.connect()
print(drone.get_battery())
drone.end()

# drone.takeoff()
# drone.move_forward(20)
# drone.land()

# drone.end()
