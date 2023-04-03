class Point():
    def __init__(self, x, y): # what happens when the Point is called?, a new instance is initiated
        self.x = x
        self.y = y

p = Point(2, 8)

print(p.x)
print(p.y)

# Define a class 'Flight'
class Flight(): 
    def __init__(self, capacity): # def the init function - this happens when a new instance is created
        self.capacity = capacity
        self.passengers = []

    def add_passenger(self, name): # def a function that adds a person to flight, after checking for room
        if not self.open_seats():
            return False
        self.passengers.append(name)
        return True

    def open_seats(self): # def a function that checks if there are free seats
        return self.capacity - len(self.passengers)

flight = Flight(3)

people = ["Harry", "Ron", "Hermione", "Ginny"]
for person in people:
    success = flight.add_passenger(person)
    if success:
        print(f"Added {person} to flight successfully.")
    else:
        print(f"No available seat for {person}.")