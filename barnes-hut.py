#August

###############################################################################################
# so, I'm pretty sure this won't work, but if it does I'll just have it as part of my program.#
# For one, I actually want to find a good way of simulating an n-body system.                 #
# I really just want to make a cool galaxy model, whith lots of cool swirly colors and        #
# authentic physics.                                                                          #
# Unfortunately my last                                                                       #
# program ran on complexity O(n^2). For systems of more than 50 particles, I found that         #
# computing their interactions took quite a while. Beyond that would be rediculous            #
# According to wikipedia, this way should work noice                                          #
###############################################################################################

import math #if only learning math were as easy as that
import random
import time
pgl_exists = True
try:
    from pgl import GRect, GWindow, GCompound, GState
except:
    pgl_exists = False

THETA = 1

class Vector2():
    def __init__(self,x,y,):
        self.x = x
        self.y = y

    def __str__(self):
        return f"<{self.x},{self.y}>"

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector2(x,y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y

        return Vector2(x,y)

    def __mul__(self,scalar):
        x = self.x * scalar
        y = self.y * scalar

        return Vector2(x, y)

    def get_magnitude(self):
        """returns the magnitude of a vector as a float"""
        return math.sqrt(self.x**2 + self.y**2)

    def get_magnitude_squared(self):
        """returns the square magnitude of a vector as a float"""
        return self.x**2 + self.y**2

    def angle(self,other):
        """returns the angle between two vectors in radians as a float"""
        return math.acos((self*other/(self.get_magnitude()*other.get_magnitude())))

    def cross_product(self,other):
        x = self.y * other.z - self.z*other.y
        y = self.z*other.x - self.x*other.z

        return Vector2(x,y)

    def get_x(self):
        """returns the x component of a vector"""
        return self.x

    def get_y(self):
        """returns the y component of a vector"""
        return self.y

    @staticmethod
    def dot(v1,v2):
        """inputs: two Vector2s
        Outputs: scalar value, integer or float, the dot product of the inputs"""
        x = v1.get_x() * v2.get_x()
        y = v1.get_y() * v2.get_y()
        return x+y

class Body():
    def __init__(self,r,m,v):
        """
        r: defines the position of the body, should be a Vector2
        m: defines the mass of the body, should be a float
        v: defines the velocity of the body, should be a Vector2
        """
        self._position = r #should be a Vector2
        self._mass = m #should be a float
        self._velocity = v #should be a Vector2

    def find_node(self):
        """I want these guys to be smart, to know and tell the nodes that they're in there"""
        pass

    def __str__(self):
        return str(f"m= {self._mass}")

    def draw(self):
        x,y = (self._position.get_x(),self._position.get_y())
        if pgl_exists:
            return GRect(x,y,0,0)
        else:
            print("pgl does not exist")

    def set_position(self,new_pos):
        self._position = new_pos

    def set_velocity(self,new_velocity):
        self._velocity = new_velocity
    
    def set_force(self,force):
        self._force = force
        
    def set_mass(self,mass):
        self._mass = mass

    def get_position(self):
        return self._position

    def get_velocity(self):
        return self._velocity

    def get_mass(self):
        return self._mass

class Universe():
    def __init__(self,bodies):
        """takes in a list of Body's and does physics to them frame by frame, storing the frames list of lists of positions for each frame"""
        self._frame = 0
        self._frames = [] #an array of each body in its position
        self._bodies = bodies

    def calculate_frame(self,expanding_space = False,exp = 0.9999):
        tree = NodeTree(self)
        start = 1
        body = self._bodies[0]
        
        done = False
        
        calcs = 0
        for b in self._bodies:
            if expanding_space:
                b.set_position(b.get_position()*exp)
            b.set_position(b.get_position()+b.get_velocity())
            bods = []
            d = 1
            for n in tree.search_nodes(d):
                all_good = True
                try:
                    n.get_mass_distribution()
                except:
                    pass
                if n != None:
                    r = (b.get_position() - n.get_position()).get_magnitude()
                    if r != 0 and THETA > d/r and n not in bods:
                        bods.append(n)
                        if b != n:

                            r_vec = (b.get_position() - n.get_position())
                            r = r_vec.get_magnitude()
                            if r != 0:
                                
                                f = r_vec*((n.get_mass()/(r+0.001)**2)*-1)
                                #print(bod.get_mass())
                                b.set_velocity(b.get_velocity()+f)
            
         #   for bod in bods:
                
        self._frame += 1
        self._frames.append([body.get_position() for body in self.get_bodies()])
        #print(calcs)


        
    def get_frames(self):
        return self._frames


    def get_bodies(self):
        return self._bodies

class NodeTree():

    def __init__(self,universe):

        self.universe = universe
        bodies = self.universe.get_bodies()
        self.bodies = bodies


        bodxs = [bod.get_position().get_x() for bod in self.bodies]
        bodys = [bod.get_position().get_y() for bod in self.bodies]
        max_x = max(bodxs)
        min_x = min(bodxs)
        max_y = max(bodys)
        min_y = min(bodys)
        
        self.max_x = max_x
        self.min_x = min_x
        
        self.max_y = max_y
        self.min_y = min_y
        self.tree = self.create_nodes()

    def create_nodes(self):
        self.node_tree = Node(
            self.universe,
            0,
            self.max_x, self.min_x,
            self.max_y,self.min_y,
        )

        for body in self.bodies:
            self.node_tree.add_body(body)
        return self.node_tree

    def show_nodes(self):
        tree = GCompound()
        tree.add(self.node_tree.show_node())
        return tree

    def search_nodes(self,d):
        depth = 1
        it = self.tree.get_children()
        old = []
        old_old = []
        while depth < d: 
            new_it = []
            all_none = True
            some_none = False
            for c in it:
                if c != None:
                    all_none = False
                    if None not in c.get_children():
                        new_it += c.get_children()
                        some_none = True
            depth += 1
            if all_none:
                return self.bodies
            if some_none:
                return self.bodies + it
            old_old = old[:]
            old = it[:]
            it = new_it
        return it

class Node(Body):

    def create_nodes(self):
        pass

    def __init__(self,uni,d,
        max_x,min_x,
        max_y,min_y,
        nw = None,ne = None,sw = None,se = None):
        """
        Input:
        uni - the universe where all the particles are
        d - the recursion depth. For the root, this will be zero.
        """
        Body.__init__(self,Vector2(0, 0),0,Vector2(0, 0))
        self.depth = d
        self.max_x = max_x
        self.max_y = max_y
        self.min_x = min_x
        self.min_y = min_y
        self.nw = nw
        self.ne = ne
        self.sw = sw
        self.se = se
        self.bodies = []

        self.cx = (max_x + min_x)/2
        self.cy = (max_y + min_y)/2
        
    def get_mass_distribution(self):
        center = None
        bodies = self.bodies
        mass = 0
        if len(bodies) == 0:
            center = Vector2(self.cx,self.cy)
        elif len(bodies) == 1:
            center = bodies[0].get_position()
            mass = bodies[0].get_mass()
        else:
            sum_mx = 0
            sum_my = 0
            sum_m = 0
            for body in bodies:
                x = body.get_position().get_x()
                y = body.get_position().get_y()
                m = body.get_mass()
                sum_mx += m*x
                sum_my += m*y
                sum_m += m
            avg_x = sum_mx/sum_m
            avg_y = sum_my/sum_m
            center = Vector2(avg_x, avg_y)
            mass = sum_m
            
        self.set_position(center)
        self.set_mass(mass) #recall that a node is a child of Body
        
    def add_body(self,body):
        """"""
        x = body.get_position().get_x()
        y = body.get_position().get_y()
        
        cx = self.cx
        cy = self.cy

        if body != None:
            if len(self.bodies) == 0:
                self.bodies.append(body)
            else:
                self.bodies.append(body)
                self.create_nodes()
                if x > cx and y > cy: # top right corner
                    self.ne.add_body(body)
                elif x > cx and y <= cy: # bottom right corner
                    self.se.add_body(body)
                elif x <= cx and y <= cy: # bottom left corner                    
                    self.sw.add_body(body)
                elif x <= cx and y > cy: # bottom left corner
                    self.nw.add_body(body)
    def create_nodes(self):
        cx = self.cx
        cy = self.cy
        max_x = self.max_x
        min_x = self.min_x
        max_y = self.max_y
        min_y = self.min_y

        if self.ne != None:
            pass
        else:
            self.ne = Node(uni, self.depth + 1, max_x, cx, max_y, cy)
            #self.ne.add_body(body)
        if self.se != None:
            pass
        else:
            self.se = Node(uni, self.depth + 1, max_x, cx, cy, min_y)
            #self.se.add_body(body)
        if self.sw != None:
            pass
        else:
            self.sw = Node(uni, self.depth + 1, cx, min_x, cy, min_y)
            #self.sw.add_body(body)
        if self.nw != None:
            pass
        else:
            self.nw = Node(uni, self.depth + 1, cx, min_x, max_y, cy)
            #self.nw.add_body(body)

    def get_children(self):
        return [self.ne,self.se,self.sw,self.nw]

                
    def show_node(self):

        #print(self.max_x)
        #print(self.min_x)
        #print(self.max_x-self.min_y)
        node = GCompound()
        box = GRect(self.min_x, self.min_y,
        self.max_x-self.min_x, 
        self.max_y - self.min_y
        )
        if len(self.bodies) == 1:
            box.set_color("Green")
        elif len(self.bodies) == 0:
            box.set_color("Red")
        node.add(box)
        if self.ne != None:
            node.add(self.ne.show_node())
        if self.se != None:
            node.add(self.se.show_node())
        if self.sw != None:
            node.add(self.sw.show_node())
        if self.nw != None:
            node.add(self.nw.show_node())
        return node
        

if __name__ == "__main__":
    print("compiled succesfully",pgl_exists)
    if pgl_exists:
        
        bods = []
        r = 2000
        #for i in range(100):
        #    rp = Vector2(random.randrange(-r,r), random.randrange(-r,r))
        #    x = rp.get_x()
         #   y = rp.get_y()
         #   if x**2 + y**2 < r**2:
         #       bods.append(Body(rp,0.1,Vector2(0,0)))
        def galaxy1():
            for r in range(1,50):
                for a in range(10):
                    rad = (r/10)**2*50
                    theta = a*math.pi/180*36+random.randrange(1,100)
                    p = Vector2(rad*math.cos(theta),rad*math.sin(theta))
                    coin = random.randrange(1,10)
                    if coin == 1:
                        bods.append(Body(p*10,random.randrange(2000,20000),Vector2(-r*10000*math.sin(theta),r*30000*math.cos(theta))))
        def galaxy2():
            for r in range(1,25):
                for a in range(10):
                    rad = (r/10)**2*50
                    theta = a*math.pi/180*36+random.randrange(1,10)
                    p = Vector2(rad*math.cos(theta),rad*math.sin(theta)-30000)
                    coin = random.randrange(1,50)
                    if coin == 1:
                        bods.append(Body(p*10,random.randrange(1000,10000),Vector2(200*math.sin(theta),-200*math.cos(theta)+100)))
        def stars():
            bods.append(Body(Vector2(0,0),10,Vector2(0,0)))
            for r in range(1,10):
                for a in range(10):
                    rad = r*10
                    theta = a*math.pi/180*36+random.randrange(1,10)
                    p = Vector2(rad*math.cos(theta),rad*math.sin(theta))
                    coin = random.randrange(1,10)
                    if coin == 1:
                        bods.append(Body(p,0.1,Vector2(-5/r*math.sin(theta),5/r*math.cos(theta))))

        galaxy1()
        #galaxy2()
        #stars()
        uni = Universe(bods)
        name = "frames/frames.txt"
        try:
            f = open(name,"x")
        except:
            print("data exists")
        iterations = 3000
        for i in range(iterations):
            timer = time.time()
            uni.calculate_frame()
            print(f'frame {i} calculated in {-(timer-time.time())} seconds')
        for frame in uni.get_frames():
            text = ""
            for pos in frame:
                x = pos.get_x()
                y = pos.get_y()
                text += f"/{x},{y}"
            f.write(text + '\n')

        gw = GWindow(800,800)
        gs = GState()
        gs.i = 0
        gs.last = GCompound()
        bg = GRect(800,800)
        bg.set_filled(True)
        gw.add(bg)
        gw.add(gs.last)
        def run():
            gw.remove(gs.last)
            gs.last = GCompound()
            frame = uni.get_frames()[gs.i % 100]
            #frame = a[gs.i%10]
            for pos in frame:
                p = GRect(pos.get_x()+400,pos.get_y()+400,1,1)
                p.set_color("Skyblue")
                #tree = NodeTree(uni)
                #gs.last.add(tree.show_nodes())
                gs.last.add(p)
            gw.add(gs.last)
            gs.i += 1
        gw.set_interval(run,1)
        #for body in uni.get_bodies():
        #    gw.add(body.draw())
        
        test = False
        if test:
            for n in tree.search_nodes(2):
                try:
                    n.get_mass_distribution()
                    
                    b = GRect(n.get_position().get_x()-(n.max_x-n.min_x)/2,
                    n.get_position().get_y()-(n.max_y-n.min_y)/2,n.max_y-n.min_y,n.max_y-n.min_y)
                    b.set_color("Blue")
                    gw.add(b)
                except:
                    b = GRect(n.get_position().get_x(),
                    n.get_position().get_y(),1,10)
                    b.set_color("Blue")
                    gw.add(b)
