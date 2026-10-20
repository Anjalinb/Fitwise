from google import genai
import os
from dotenv import load_dotenv
load_dotenv()

api_key=os.getenv('api_key')

client=genai.Client(api_key=api_key)

def get_diet_plan(response_data):

    monthly_total=response_data.get("monthly_total")
    monthly_summary=response_data.get("monthly_summary")
    monthly_summary_text=""

    for di in monthly_summary:
        monthly_summary_text+=f".{di.get('meal_type')} : {di.get('total')}\n"
    print(monthly_summary_text)

    prompt = f"""
                Act as an expert health advisor specializing in diet plans  in Kerala, India.

                Here is my monthly calorie summary for last month:
                - Total caories consumed: ₹{monthly_total:,}
                - Category Breakdown:{monthly_summary_text}
            

                Based on this data, please provide a practical 1-month  diet plan:
                """

    response=client.models.generate_content(
        model="gemini-3.7-flash",
        contents=prompt
    )

    return response.text