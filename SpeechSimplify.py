import openai
import re
from speechtotext import SpeechToText


# Simplify text subclass
class SimplifyText(SpeechToText):
    def __init__(self, model_task='transcribe'):
        super().__init__(model_task)
        # openai.api_key = os.getenv("OPENAI_API_KEY") #OpenAI API key from environment

    def transcribe(self):
        super().transcribe()
        original_text = ''.join(self.transcription)
        print(f'\n\n{original_text}\n\n')
        original_text.replace('\n', '. ')
        original_text.replace('\\\\', '')
        # re.sub("(\\\\n)|(\\\\)", '', original_text)
        prompt = f"Simplify this text for non-native English speakers:\n\n'{original_text}'"

        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You simplify text for better understanding"},
                    {"role": "user", "content": prompt}
                ]
            )
            simplified_text = response.choices[0].message.content
        except Exception as error:
            simplified_text = f"Error: {str(error)}"

        print(f'original: {original_text}\n\nsimplified: {simplified_text}')
        
        # return {"original_text": original_text, "simplified_text": simplified_text}
    


    ##########FOR TESTING ONLY####################

# if __name__ == "__main__":
#     simplifier = SimplifyText()
#     dummy_audio_input_1 = "The hackathon project is moving along well, but we're struggling to implement all the features we initially planned, causing it to not go as smooth as we would have liked, but its okay because we are working hard on getting back on the smooth track"
#     dummy_audio_input_2 = "To be, or not to be, that is the question: Whether 'tis nobler in the mind to suffer The slings and arrows of outrageous fortune, Or to take arms against a sea of troubles And, by opposing, end them. To die, to sleep; No more; and by a sleep to say we end The heart-ache and the thousand natural shocks That flesh is heir to. To die, to sleep; To sleep: perchance to dream: ay, there's the rub; For in that sleep of death what dreams may come When we have shuffled off this mortal coil, Must give us pause: there's the respect That makes calamity of so long life."
#
#     #####Displaying Tested Results###########
#     result_1 = simplifier.speech_to_simplified_text(dummy_audio_input_1)
#     print("Test Case 1 - Original Text: ")
#     print(result_1["original_text"])
#     print("\nSimplified Text:")
#     print(result_1["simplified_text"])
#     print("\n" + "="*40 + "\n")
#
#     result_2 = simplifier.speech_to_simplified_text(dummy_audio_input_2)
#     print("Test Case 2 - Original Text: ")
#     print(result_2["original_text"])
#     print("\nSimplified Text:")
#     print(result_2["simplified_text"])

    
