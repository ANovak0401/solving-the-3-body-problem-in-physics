from turtle import Shape, Screen, Turtle, Vec2D as Vec


# user input:
G = 8
NUM_LOOPS = 4100
Ro_X = 0
Ro_Y = -85
Vo_X = 485
Vo_Y = 0


class GravSys():
    """runs a gravity simulation on n-bodies"""

    def __init__(self):
        self.bodies = []
        self.t = 0
        self.dt = 0.001

    def sim_loop(self):
        """loop bodies in a list through time steps"""
        for _ in range(NUM_LOOPS):  # for each time step in num_loops
            self.t += self.dt  # increment time variable by dt
            for body in self.bodies:  # increment time shift for each body
                body.step()  # with body step


class Body(Turtle):
    """Celestial object that orbits and projects gravity field"""

    def __init__(self, mass, start_loc, vel, gravsys, shape):
        super().__init__(shape=shape)  # inherit Turtle class from module
        self.gravsys = gravsys  # gravity system for object
        self.penup()  # remove drawn lines
        self.mass = mass  # mass for body
        self.setpos(start_loc)  # starting location of object on screen
        self.vel = vel  # velocity of object
        gravsys.bodies.append(self)  # add to list of bodies in Gravsys
        #self.resizemode("user")
        #self.pendown()

    def acc(self):
        """Calculate combined force on body and return vector compnents."""
        a = Vec(0, 0)  # vector tuple for acceleration
        for body in self.gravsys.bodies:  # loop through the bodies list
            if body != self:  # if body is not the current body
                r = body.pos() - self.pos()  # find distance between the two bodies
                a += (G * body.mass / abs(r)**3) * r  # acceleration equation added to acceleration tuple
        return a  # return acceleration

    def step(self):
        """Calculate position, orientation, and velocity of a body."""
        dt = self.gravsys.dt  # increment velocity at each step with floating point
        a = self.acc()  # variable holds acceleration calculation
        self.vel = self.vel + dt * a  # update velocity
        self.setpos(self.pos() + dt * self.vel)  # update position of body
        if self.gravsys.bodies.index(self) == 2:  # index 2 = CSM.  # the space capsule
            rotate_factor = 0.0006  # amount or rotation of spacecraft
            self.setheading((self.heading() - rotate_factor * self.xcor()))  # calculate heading of capsule
            if self.xcor() < -20:  # time to eject service module when CSM is close to returning to earth
                self.shape('arrow')  # draw a directional arrow on screen
                self.shapesize(0.5)  # set size
                self.setheading(105)  # set heading of arrow to face correctly


def main():
    screen = Screen()  # instantiate instance of turtle screen
    screen.setup(width=1.0, height=1.0)  # for fullscreen
    screen.bgcolor('black')  # background color of turtle screen
    screen.title("Apollo 8 Free Return Simulation")  # screen title

    gravsys = GravSys()

    image_earth = 'C:/Users/austi/Documents/pythonWork/three_body_problem/earth_100x100.gif'  # location of image file
    screen.register_shape(image_earth)  # register shape on screen
    earth = Body(1000000, (0, -25), Vec(0, -2.5), gravsys, image_earth)  # create instance of Body named earth
    earth.pencolor('white')  # set color of earth trail
    earth.getscreen().tracer(n=0, delay=0)  # delay screen for smoother visuals

    image_moon = 'C:/Users/austi/Documents/pythonWork/three_body_problem/moon_27x27.gif'  # location of moon image
    screen.register_shape(image_moon)  # register image to screen
    moon = Body(32000, (344, 42), Vec(-27, 147), gravsys, image_moon)  # create instance of Body for moon
    moon.pencolor('gray')  # set tracer trail

    csm = Shape('compound')  # create shape for CSM
    cm = ((0, 30), (0, -30), (30, 0))  # arguments are polygon type triangle tuple,
    csm.addcomponent(cm, 'white', 'white')  # add component to csm
    sm = ((-60, 30), (0, 30), (0, -30), (-60, -30))  # service module square tuple coords
    csm.addcomponent(sm, 'white', 'black')  # add service module to csm shape
    nozzle = ((-55, 0), (-90, 20), (-90, -20))  # triangle tuple to create nozzle
    csm.addcomponent(nozzle, 'white', 'white')  # add nozzle to CSM
    screen.register_shape('csm', csm)  # register CSM to turtle screen

    ship = Body(1, (Ro_X, Ro_Y), Vec(Vo_X, Vo_Y), gravsys, 'csm')
    ship.shapesize(0.2)
    ship.color('white')
    ship.getscreen().tracer(1, 0)
    ship.setheading(90)

    gravsys.sim_loop()

    screen.bye()


if __name__ == '__main__':
    main()
