w, h = 2500, 1000

celestials = []
giants = []

grid_width = 30
grid_height = 30

cell_width = float(w)/grid_width
cell_height = float(h)/grid_height

color_palette = [(229, 115, 118), (235, 167, 114), (114, 178, 241), (211, 173, 223), (170, 198, 166)]

# Set colors (no palette)
planet_outline_color = (255, 255, 255)

planet_fill_color = (0, 0, 0)


# System Variables

sun_size = 1500

planet_sep = 150
min_planet_size = 40
max_planet_size = 260
planet_stroke = 8

min_rings = 2
max_rings = 6
ring_stroke = 4

moon_sep = 5
min_moon_size = 5
max_moon_size = 25
moon_stroke = 4

# Stars
add_stars = True


# Find and set a random color from predefined palette
def set_palette_color():
    c = color_palette[int(random(len(color_palette)))]
    fill(c[0], c[1], c[2])

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
            if (rings == True):
                self.add_rings()
            giants.append(self)
            fill(planet_fill_color[0], planet_fill_color[1], planet_fill_color[2])
            self.display()
        
    # Circle isn't placed randomly and gets evaluated like a gridless object
    def place_manually(self, position):
        self.position = position
        gridless.append(self)
        self.display()
        
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
                if (distance < (c.size/2 + self.size/2 + 1)):
                    valid = False
                    
            # Avoid placing stars too close to planets and sun
            compare_list = []
            
            for c in giants:
                compare_list.append(c)
            
            for c in compare_list:
                distance = sqrt(pow(c.position[1] - self.position[1], 2) + pow(c.position[0] - self.position[0], 2))
                if (distance < (c.size/2 + self.size/2 + 20)):
                    valid = False
                    
                
                
                
            # Avoid the edges of the image
            if (self.position[0] + self.size/2 > w or self.position[0] - self.size/2 < 0 or self.position[1] + self.size/2 > h or self.position[1] - self.size/2 < 0):
                valid = False
                    
            if (valid == True):
                celestials[grid_position].append(self)
                self.display()
                break
                
    def add_rings(self):
        strokeWeight(ring_stroke)
        if (len(giants) != 0 and random(1) < .2):
            starting_height = random(self.size/4, self.size/2)
            starting_width = random(self.size*1.2, self.size*2)
            rotation = random(6)
            noFill()
            for i in range(int(random(min_rings, max_rings))):
                pushMatrix()
                translate(self.position[0], self.position[1])
                rotate(rotation)
                ellipse(0, 0, starting_height + i * 10, starting_width + i * 30)
                popMatrix()
            
    def get_grid_position(self):
        x = self.position[0]
        y = self.position[1]
        return int(x/cell_width) + int(y/cell_height) * grid_width 
        
    def display(self):
        circle(self.position[0], self.position[1], self.size)
        


def setup():
    size(w, h)
    pixelDensity(2)
    
    background(0, 0, 0)
    strokeWeight(5)
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
        planet = Celestial(next_planet_size)
        planet.add_giant((center, h/2), True)
        
        # Add moons for the planet
        moons = []
        moon_y = h - h/4
        if (random(1) < .3):
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
                
        
        last_size = next_planet_size
    
    # Add the stars
    for i in range(grid_width * grid_height):
        celestials.append([])
        
    noStroke()
    fill(255, 255, 255, random(0, 255))
    if (add_stars == True):
        for x in range(6000):
            star = Celestial(random(1, 3))
            star.add_random_valid()
        
    

    save("Examples/test.png")
