import pandas as pd
import openai
import os
import time

def openAI_request(text_to_analyze):
    openai.api_key = os.environ['api-key']
    result = None

    while result is None:
        try:
            prompt_for_openAI = f"""
            Please answer the following open answers from a questionnaire:
            
            1: What is the essence of this person's answer text in 5 to 10 words?: {text_to_analyze}?
            2. What category would you give this text? One or a couple of words.
            3: What is the sentiment? Positive, neutral or negative?
            
            Please answer in the following format:
            
            Answer 1:::
            Answer 2:::
            Answer 3:::
            """

            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt_for_openAI,
                temperature=0.9,
                max_tokens=150,
                top_p=1,
                frequency_penalty=0.0,
                presence_penalty=0.6,
                stop=[" Human:", " AI:"]
            )

            data = response['choices'][0]['text']
            result = data
            print("Data found!")
        except:
            time.sleep(5)
            print("Error, sleeping, zzz.")

    return data

df = pd.read_excel("amazon_reviews(1).xlsx")

for index, row in df.iterrows():
    # print(index, row["Sana commerce"])
    text = row["reviews.text"]
    if text != None:
        # print(f"Question on index {index}")
        # print(f"Text to analyze:\n{text}")

        data = str(openAI_request(text))

        replace_words = ["Answer 1", "Answer 2", "Answer 3"]
        for word in replace_words:
            data = data.replace(word, "")
            # print(data)
        data = data.strip().split(":::")

        print(data)
        print("\n")
        df.at[index, "OpenAI Answer 1"] = f"{data[1]}"
        df.at[index, "OpenAI Answer 2"] = f"{data[2]}"
        df.at[index, "OpenAI Answer 3"] = f"{data[3]}"

        df.to_csv("OpenAI_Answers.csv")
        df.to_excel("OpenAI_Answers.xlsx", index=False)

