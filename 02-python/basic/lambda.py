people = [ # a list
    {"name": "Harry", "house": "Gryffindor"}, # ...of dictionaries
    {"name": "Cho", "house": "Ravenclaw"},
    {"name": "Draco", "house": "Slyterin"}
]

# Printing the original list
print(people)

# # creating another function to get the name
# def f(person):
#     return person["name"]

# people.sort(key=f)

# instead using a lambda function
people.sort(key=lambda person: person["name"])

# Printing the sorted list
print(people)