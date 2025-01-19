from openai import OpenAI
import json
import os

api_key_open = os.getenv("API_KEY")

client = OpenAI(api_key = api_key_open)

def parseIngredients(ingredients):
    result = []
    for ingredientTuple in ingredients:
        result.append({"ingredient_name":ingredientTuple[0], "expiry_date":ingredientTuple[1], "quantity":ingredientTuple[2]})
    return {"ingredients" : result}


def query(restrictions, ingredients):
    return client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                "role": "system",
                "content": [
                    {
                    "text": "You are a award-winning chef ready to create new and exciting recipes! You will take a list of ingredients a customer gives you and produce multiple delicious recipes for them to make. Each ingredient has the date it was purchased so make sure to use the ones about to go bad! Feel free to add other common ingredients that you know will go well with the dish! The day today is Jan 18, 2025 and format the recipe in a JSON object!",
                    "type": "text"
                    }
                ]
                },
                {
                "role": "user",
                "content": [
                    {
                    "type": "text",
                    "text": "{\"ingredients\":[{\"ingredient_name\":\"Bananas\",\"expiry_date\":\"2023-09-25\",\"quantity\":\"a lot\"},{\"ingredient_name\":\"Whole Milk\",\"expiry_date\":\"2023-10-02\",\"quantity\":\"some\"},{\"ingredient_name\":\"Eggs\",\"expiry_date\":\"2023-09-30\",\"quantity\":\"a little\"},{\"ingredient_name\":\"Chicken Breast\",\"expiry_date\":\"2023-10-01\",\"quantity\":\"some\"},{\"ingredient_name\":\"Spinach\",\"expiry_date\":\"2023-09-28\",\"quantity\":\"a little\"}]}"
                    }
                ]
                }
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                "name": "recipe",
                "strict": True,
                "schema": {
                    "type": "object",
                    "required": [
                    "ingredients",
                    "steps",
                    "name"
                    ],
                    "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the recipe!"
                    },
                    "ingredients": {
                        "type": "array",
                        "items": {
                        "type": "object",
                        "required": [
                            "name",
                            "quantity"
                        ],
                        "properties": {
                            "name": {
                            "type": "string",
                            "description": "The name of the ingredient."
                            },
                            "quantity": {
                            "type": "string",
                            "description": "The quantity of the ingredient."
                            }
                        },
                        "additionalProperties": False
                        },
                        "description": "List of ingredients for the recipe."
                    },
                    "steps": {
                        "type": "array",
                        "items": {
                        "type": "object",
                        "required": [
                            "description",
                            "duration"
                        ],
                        "properties": {
                            "duration": {
                            "type": "string",
                            "description": "The time it takes to complete this step."
                            },
                            "description": {
                            "type": "string",
                            "description": "A description of the step."
                            }
                        },
                        "additionalProperties": False
                        },
                        "description": "List of steps to prepare the recipe."
                    }
                    },
                    "additionalProperties": False
                }
                }
            },
            temperature=1,
            max_completion_tokens=2048,
            top_p=1,
            frequency_penalty=0.31,
            presence_penalty=0
            )

def recipeCreate(input):
    restrictions = " ".join(input['prefrences']) # restrictions (listof string)
    ingredients = parseIngredients(input['ingredients']) # ingredients (listof tuple) (name, date, quantity)

    print(restrictions)
    print(ingredients)

    # outputSucceed = False
    # while not outputSucceed:
    #     try:
    #         output1 = json.loads(query(restrictions, ingredients).choices[0].message.content)
    #         outputSucceed = True
    #     except:
    #         pass
    


    # with open("output.json", "w") as file:
    #     json.dump(output1, file, indent=4)
    # print("Wrote to output.json")  


recipeCreate({"prefrences":["gluten_free"], "ingredients":[("banana", "2025-10-01", "a little"), ("banana", "2025-10-01", "a lot"), ("banana", "2025-10-01", "a little")]})
