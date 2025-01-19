from openai import OpenAI
import datetime
import os

expiry_key = os.environ.get('OPEN_EXPIRY')
if expiry_key:
    client = OpenAI(api_key=expiry_key)

def query(input_msg):
    sys_msg = "You are a model that predicts the expiry date of food items. Always provide a clear and accurate predicted expiry date in number of days. Dont provide anything else, just the integer for number of days. Ensure your predictions align with typical food storage and spoilage guidelines. return fail if the name of the input is not a food item."

    return client.chat.completions.create(
            model="ft:gpt-4o-mini-2024-07-18:personal:realfinalexppredict:ArLtLNiP",
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
                    "text": input_msg
                    }
                ]
                }
            ],
            temperature=1,
            max_completion_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0)



def expiryCreate(input):
    input_msg = input['name']
    purchase_date = input['purchase_date']
    dates = purchase_date.split("-")
    
    date_obj = datetime.date(int(dates[0]), int(dates[1]), int(dates[2]))

    try:
        output1 = datetime.timedelta(days=int(query(input_msg).choices[0].message.content))
    except:
        return {"error":"fail"}
    expiry_date = date_obj + output1

    return str(expiry_date.year) + "-" + str(expiry_date.month) + "-" + str(expiry_date.day)


