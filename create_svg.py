import math

# Each svg_editor object can edit one file
class svg():

    file = None

    def __init__(self, name):
        self.file  = open("{0}.svg".format(name), "w")


    def write(self, x):
        self.file.write(x)

    def start_svg(self,  width, height):
        self.write('<svg width="{0}" height="{1}" style="background-color: #fff">\n'.format(width,height))

    def start_mask(self, r):
        self.write('<mask id="hole{0}">\n'.format(r))

    def end_svg(self):
        self.write('</svg>\n')

    def end_mask(self):
        self.write('</mask>\n')

    def draw_rect(self, x, y, width, height):
        self.write('<rect x="{0}" y="{1}" width="{2}" height="{3}" stroke="black" stroke-width="5" fill="none"/>\n'.format(x, y, width, height))


    def draw_circle(self, x, y, r):
        self.write('<circle cx="{0}" cy="{1}" r="{2}" stroke-width="2" fill="none" stroke="black"  />\n'
        .format(x, y, r))

    def add_circle_with_offset(self, center, r, thick):
        self.start_mask(r)
        #draw the smaller circle 
        self.write('<rect width="100%" height="100%" fill="white"/>\n')
        self.draw_circle(center, center, r - thick)
        self.end_mask()
        self.write('<circle cx="{0}" cy="{1}" r="{2}" stroke-width="1" fill="black" mask="url(#hole{2})"/>\n'
        .format(center, center, r))



    def draw_line(self, x1, y1, x2, y2):
        self.write('<line x1="{0}" y1="{1}" x2="{2}" y2="{3}" style="stroke:black;stroke-width:3" />\n'
        .format(x1, y1, x2, y2))

    def get_coordinates(self,angle, center, big_r, little_r):
        angle = -(angle + 180)
        x1 = big_r * math.sin(math.radians(angle)) + center
        x2 = little_r * math.sin(math.radians(angle)) + center

        y1 = big_r * math.cos(math.radians(angle)) + center
        y2 = little_r * math.cos(math.radians(angle)) + center

        return [x1,y1,x2,y2]
    
    def get_int_coordinates(self, angle, center, big_r, little_r):
        r = little_r + ((big_r - little_r)/2)
        angle = -(angle + 180)
        x1 = r * math.sin(math.radians(angle)) + center

        y1 = r * math.cos(math.radians(angle)) + center

        return [x1-8, y1+6]


    def start_group(self):
        self.write('<g>\n')   

    def end_group(self):
        self.write('</g>\n')  

    def add_font(self, font_name, font_data):
        #Adds a base64 font
        self.write('<style>\n@font-face {{\n font-family: "{0}"\nscr: url("{1}")\n}}\n</style>'''.format(font_name, font_data))       
        # self.write('''<style>\n@font-face {\n font-family: "{0}"\nscr: url("{1}")\n}\n</style>'''.format(font_name, font_data))       

    def add_text(self, text, font, x, y, size):
        self.write('<text font-size="{4}" font-family="{0}" x="{1}" y="{2}">\n{3}\n</text>'.format(font, x, y, text, size))

    def add_sideways_text(self, text, font, x, y, size):
        self.write('<text dominant-baseline="middle" text-anchor="end" font-size="{4}" transform="rotate(-90)" font-family="{0}" x="{1}" y="{2}">\n{3}\n</text>'.format(font, x, y, text, size))

def main():
    file = open("test.svg", "w")
    canvas_size = 300
    center = canvas_size / 2
    self.start_svg(file, canvas_size, canvas_size)

    daily_chores_count = 4
    weekly_chores_count = 1

    days = 31
    


    number_of_chores = daily_chores_count + weekly_chores_count


    space = 10
    count = number_of_chores + 1
    buffer = 20
    thick = 2
    self.start_group(file)
    for i in range(count, 0, -1):
        draw_circle(file, center, center, i*space+buffer)



    # template
    big_r = count * space + buffer
    little_r = space + buffer

    start_degree = 0
    c = get_coordinates(start_degree, center, big_r, little_r)
    draw_line(file, c[0], c[1], c[2], c[3])

    end_degree = 300
    c = get_coordinates(end_degree, center, big_r, little_r)
    draw_line(file, c[0], c[1], c[2], c[3])


    #daily chores

    big_r = count*space + buffer
    little_r = (count - daily_chores_count) * space + buffer

    increment = ((end_degree - start_degree) // days)
    remainder = ((end_degree - start_degree) % days)
    print('increment={0}'.format(increment))
    print('remainder = {0}'.format(remainder))
    angle = 0
    for day in range(days - 1):
        if remainder > 1:
            angle = angle + 1
            remainder -= 1
            print('remainder = {0}'.format(remainder))
        angle = angle + increment
        print(angle)
        c = get_coordinates(angle, center, big_r, little_r)
        draw_line(file, c[0], c[1], c[2], c[3])

    #weekly chores

    big_r = (count - daily_chores_count) * space + buffer
    little_r = (count - daily_chores_count - weekly_chores_count) * space + buffer

    increment = ((end_degree - start_degree) // 4)
    remainder = ((end_degree - start_degree) % 4)
    print('increment={0}'.format(increment))
    print('remainder = {0}'.format(remainder))
    angle = 0
    for week in range(4 - 1):
        if remainder > 1:
            angle = angle + 1
            remainder -= 1
            print('remainder = {0}'.format(remainder))
        angle = angle + increment
        print(angle)
        c = get_coordinates(angle, center, big_r, little_r)
        draw_line(file, c[0], c[1], c[2], c[3])






    end_group(file)
    end_svg(file)
    file.close()


"""
<text font-family="Janda" x="40" y="40">
hi
</text>"""
