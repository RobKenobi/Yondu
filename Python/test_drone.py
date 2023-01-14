from djitellopy import Tello

drone = Tello()
drone.connect()
print(drone.get_battery())


drone.takeoff()
drone.flip_left()
drone.land()

drone.end()
