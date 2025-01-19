from datetime import datetime
import json

# Get current date and time
now = datetime.now()

returned_json = "output.json"

with open('output.json', 'r') as file:
    returned_json = json.load(file)

# Format date
ingredient_list = []
for ingredient in returned_json['ingredients']:
    ingredient_str = ingredient['name'] + ": " + ingredient['quantity']
    ingredient_list.append(ingredient_str)

step_list = []
for step in returned_json['steps']:
    step_str = step['duration'] + ": " + step['description']
    step_list.append(step_str)



ingredient_str = ";".join(ingredient_list)
step_str = ";".join(step_list)

print(ingredient_str)
print(step_str)