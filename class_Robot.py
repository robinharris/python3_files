class Robot:
 
    def __init__(self, name=None, build_year = None):
        self.name = name
        self.build_year = build_year
        
    def say_hi(self):
        if self.name and self.build_year:
            print("Hi, I am " + self.name, " and I was created in ", self.build_year)
        else:
            print("Hi, I am a robot without a name")
            
    def set_name(self, name):
        self.name = name
        
    def get_name(self):
        return self.name

    def set_build_year(self, build_year):
        self.build_year = build_year
        
    def get_build_year(self):
        return self.build_year
    

x = Robot()
x.set_name("Henry")
x.set_build_year(2017)
x.say_hi()
y = Robot()
y.set_name(x.get_name())
print("I am y :", x.get_name())