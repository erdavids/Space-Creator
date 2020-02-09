w, h = 2500, 1000

celestials = []
giants = []

grid_width = 100
grid_height = 100

cell_width = float(w)/grid_width
cell_height = float(h)/grid_height

color_palette = [(229, 115, 118), (235, 167, 114), (114, 178, 241), (211, 173, 223), (170, 198, 166), (215, 255, 218), (230, 215, 0)]

planet_colors = [(191, 96, 90), (170, 169, 187), (160, 198, 209), (107, 153, 168)]

# Set colors (no palette)
planet_outline_color = (255, 255, 255)

planet_fill_color = (0, 0, 0)


# System Variables

# Sun
sun_size = 1500

# Planets
planet_sep = 150
min_planet_size = 40
max_planet_size = 260
planet_stroke = 1

# Ring Systems
min_rings = 3
max_rings = 6
ring_stroke = 1
ring_chance = .3
realistic = True

# Moons
moon_sep = 5
min_moon_size = 5
max_moon_size = 25
moon_stroke = 4
moon_chance = .3

# Stars
add_stars = True
star_count = 16000
min_star_size = 1
max_star_size = 3
min_star_opacity = 0
max_star_opacity = 255
star_sep_star = 1
star_sep_planet = 6

add_star_colors = True
color_chance = .2

asteroid_max_size = 15
asteroid_min_size = 5



# Find and set a random color from predefined palette
def set_palette_fill():
    c = color_palette[int(random(len(color_palette)))]
    fill(c[0], c[1], c[2])
    
# Set the outline colors to a random color
def set_palette_stroke():
    c = color_palette[int(random(len(planet_colors)))]
    stroke(c[0], c[1], c[2])

# Convert pixel position to grid element
def get_grid_position(x, y):
    return x/cell_width + y/cell_height * grid_width 


class Celestial:
    def __init__(self, size):
        # self.position = (0, 0)
        self.size = size
        
    # Use this method if the circle is larger than the grid cell size
    def add_giant(self, position, rings):
        self.position = position
        valid = True
        for c in giants:
            distance = sqrt(pow(c.position[1] - self.position[1], 2) + pow(c.position[0] - self.position[0], 2))
            if (distance < (c.size/2 + self.size/2 + 2)):
                valid = False
                
        # if (self.position[0] + self.size/2 > w or self.position[0] - self.size/2 < 0 or self.position[1] + self.size/2 > h or self.position[1] - self.size/2 < 0):
        #     valid = False
        
        if (valid == True):
            if (rings == True and random(1) < ring_chance):
                self.display_with_rings()
                giants.append(self)
            else:
                fill(planet_fill_color[0], planet_fill_color[1], planet_fill_color[2])
                self.display()
                giants.append(self)
        
    # Circle isn't placed randomly and gets evaluated like a gridless object
    def place_manually(self, position):
        self.position = position
        gridless.append(self)
        self.display()
    
    def place_asteroid(self, position):
        
        strokeWeight(1)
        stroke(planet_outline_color[0], planet_outline_color[1], planet_outline_color[2])
        fill(planet_fill_color[0], planet_fill_color[1], planet_fill_color[2])
        
        points = []
        rad = 0.0
        while (rad < 2*PI):
            #point(250 + (random(80, 100) * cos(rad)), 250 + (random(80, 100) * sin(rad)))
            cos_r = random(asteroid_min_size, asteroid_max_size)
            sin_r = random(asteroid_min_size, asteroid_max_size)
            p = (position[0] + (cos_r * cos(rad)), position[1] + (sin_r * sin(rad)), rad, cos_r, sin_r)
            points.append(p)
            rad += .6
        
        beginShape()
        for p in points:
            curveVertex(p[0], p[1])
            
        curveVertex(points[0][0], points[0][1])
        curveVertex(points[1][0], points[1][1])
        curveVertex(points[2][0], points[2][1])
        endShape()
        
    # Probably used for the stars
    def add_random_valid(self):
        for i in range(20):
            self.position = (random(w), random(h))
            grid_position = int(self.get_grid_position())
            
            
            # Compare each smaller celestial (stars)
            compare_list = []
        
            for c in celestials[grid_position]:
                compare_list.append(c)
                
            if (grid_position % grid_width > 0):
                for c in celestials[grid_position - 1]:
                    compare_list.append(c)
                    
            if (grid_position % grid_width < grid_width - 1):
                for c in celestials[grid_position + 1]:
                    compare_list.append(c)
                    
            if (grid_position >= grid_width):
                for c in celestials[grid_position - grid_width]:
                    compare_list.append(c)
                    
            if (grid_position < (grid_width * grid_height) - grid_width):
                for c in celestials[grid_position + grid_width]:
                    compare_list.append(c)
                    
            if (grid_position % grid_width > 0 and grid_position > grid_width):
                for c in celestials[grid_position - grid_width - 1]:
                    compare_list.append(c)
                    
            if (grid_position % grid_width > 0 and grid_position < (grid_width * grid_height) - grid_width):
                for c in celestials[grid_position + grid_width - 1]:
                    compare_list.append(c)
                    
            if (grid_position % grid_width < grid_width - 1 and grid_position > grid_width):
                for c in celestials[grid_position - grid_width + 1]:
                    compare_list.append(c)
            
            if (grid_position % grid_width < grid_width - 1 and grid_position < (grid_width * grid_height) - grid_width):
                for c in celestials[grid_position + grid_width + 1]:
                    compare_list.append(c)
            
            valid = True
            for c in compare_list:
                distance = sqrt(pow(c.position[1] - self.position[1], 2) + pow(c.position[0] - self.position[0], 2))
                if (distance < (c.size/2 + self.size/2 + star_sep_star)):
                    valid = False
                    
            # Avoid placing stars too close to planets and sun
            compare_list = []
            
            for c in giants:
                compare_list.append(c)
            
            for c in compare_list:
                distance = sqrt(pow(c.position[1] - self.position[1], 2) + pow(c.position[0] - self.position[0], 2))
                if (distance < (c.size/2 + self.size/2 + star_sep_planet)):
                    valid = False
                    
                
                
                
            # Avoid the edges of the image
            if (self.position[0] + self.size/2 > w or self.position[0] - self.size/2 < 0 or self.position[1] + self.size/2 > h or self.position[1] - self.size/2 < 0):
                valid = False
                    
            if (valid == True):
                celestials[grid_position].append(self)
                self.display()
                break
            
    # Draws the rings and planet    
    def display_with_rings(self):
        strokeWeight(ring_stroke)
        if (len(giants) != 0):
            starting_height = random(self.size/4, self.size/2)
            starting_width = random(self.size*1.2, self.size*2)
            noFill()
            rotation = random(6)
            for i in range(int(random(min_rings, max_rings))):
                pushMatrix()
                translate(self.position[0], self.position[1])
                rotate(rotation)
                ellipse(0, 0, starting_height + i * 10, starting_width + i * 30)
                popMatrix()
                
        strokeWeight(planet_stroke)    
        pushMatrix()
        translate(self.position[0], self.position[1])
        rotate(rotation)
        fill(0, 0, 0, 0)
        circle(0, 0, self.size)
        fill(planet_fill_color[0], planet_fill_color[1], planet_fill_color[2])
        arc(0, 0, self.size, self.size, 1.5*PI, 2.5*PI);
        popMatrix()
    
    # Used for performance
    def get_grid_position(self):
        x = self.position[0]
        y = self.position[1]
        return int(x/cell_width) + int(y/cell_height) * grid_width 
        
    # Draw a planet without rings
    def display(self):
        strokeWeight(planet_stroke)
        circle(self.position[0], self.position[1], self.size)
            
        


def setup():
    size(w, h)
    pixelDensity(2)
    
    background(0, 0, 0)
    strokeWeight(planet_stroke)
    stroke(planet_outline_color[0], planet_outline_color[1], planet_outline_color[2])
    fill(planet_fill_color[0], planet_fill_color[1], planet_fill_color[2])
    
    center = -(sun_size/4)
    last_size = sun_size
    sun = Celestial(sun_size)
    sun.add_giant((center, h/2), False)
    
    for i in range(15):
        next_planet_size = random(min_planet_size, max_planet_size)
        center = center + last_size/2 + planet_sep + next_planet_size/2
        if (next_planet_size/2 + center > w):
            break
        
        strokeWeight(planet_stroke)
        fill(planet_fill_color[0], planet_fill_color[1], planet_fill_color[2])
        
        # Add the current planet
        planet = Celestial(next_planet_size)
        planet.add_giant((center, h/2), True)
        
        # Add moons for the planet
        moons = []
        moon_y = h - h/4
        if (random(1) < moon_chance):
            for i in range(int(random(1, 8))):
                moon = Celestial(random(min_moon_size, max_moon_size))
                moons.append(moon)
            
            # Calculate length of moons
            total_length = 0
            for m in moons:
                total_length += m.size
                total_length += moon_sep
            total_length -= moon_sep
            
            # Draw the moons
            strokeWeight(moon_stroke)
            moon_start = center - total_length/2
            for m in moons:
                moon_start += m.size/2
                m.add_giant((moon_start, moon_y), False)
                
                moon_start += m.size/2 + moon_sep
                
        
        # Update tracking variable
        last_size = next_planet_size
    
    # Add the stars
    for i in range(grid_width * grid_height):
        celestials.append([])
        
    # planet = Celestial(400)
    # planet.place_asteroid((w/2, h/2))
        
    noStroke()
    fill(255, 255, 255, random(min_star_opacity, max_star_opacity))
    
    # Add all the stars using circle packing method
    if (add_stars == True):
        for x in range(star_count):
            if (random(1) < color_chance and add_star_colors == True):
                c = color_palette[int(random(len(color_palette)))]
                fill(c[0], c[1], c[2], random(min_star_opacity, max_star_opacity))
            else:
                fill(255, 255, 255, random(min_star_opacity, max_star_opacity))
            star = Celestial(random(min_star_size, max_star_size))
            star.add_random_valid()
    

    save("Examples/test.png")
