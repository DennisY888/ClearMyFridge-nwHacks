from openai import OpenAI
import json
import os

FAIL_MSG = {"error": "fail"}
recipe_key = os.environ.get('OPEN_RECIPE')
client = OpenAI(api_key = recipe_key)

def parseIngredients(ingredients):
    result = []
    for ingredientTuple in ingredients:
        result.append({"ingredient_name":ingredientTuple[0], "expiry_date":ingredientTuple[1], "quantity":ingredientTuple[2]})
    return json.dumps({"ingredients" : result})


def query(restrictions, ingredients):
    sys_msg = "You are a award-winning chef ready to create new and exciting recipes! You will take a list of ingredients a customer gives you and produce a delicious recipe for them to make. Each ingredient has the date it's gonna expire so make sure to use the ones about to go bad! Make sure you remember you don't need to use every ingredient. Feel free to add other common ingredients that you know will go well with the dish! Also keep in mind each ingredient has a associated quantity. The day today is Jan 18, 2025 and format the recipe in a JSON object. Dietary restrictions of the customer: {}.".format(restrictions)

    return client.chat.completions.create(
            model="ft:gpt-4o-mini-2024-07-18:personal:my-recipe-v3:ArGz3Idy",
            messages=[
                {
                "role": "system",
                "content": [
                    {
                    "text": sys_msg,
                    "type": "text"
                    }
                ]
                },
                {
                "role": "user",
                "content": [
                    {
                    "type": "text",
                    "text": ingredients
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
    restrictions = ",".join(input['preferences']) # restrictions (listof string)
    ingredients = parseIngredients(input['ingredients']) # ingredients (listof tuple) (name, date, quantity) 
    
    outputSucceed = False
    try:
        output1 = json.loads(query(restrictions, ingredients).choices[0].message.content)
        outputSucceed = True
    except:
        pass

    if not outputSucceed:
        return FAIL_MSG

    return output1