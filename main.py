from openai import OpenAI
from transformers import pipeline
from google.cloud import language_v1
import google.generativeai as gemini


def chat_gpt_completion():
    client = OpenAI(
        api_key=
        "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"
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "How can I connect the ChatGPT API with Python?"
            }
        ],
        model="gpt-3.5-turbo",
    )

    print(chat_completion.choices[0].message['content'])



def huggingface_gpt_completion():
    #model: EleutherAI/gpt-neo-2.7B
    generator = pipeline('text-generation', model='gpt2')

    result = generator("¿Que es apache spark?", max_length=150, do_sample=True,
                       num_return_sequences=1)

    print('result:', result)
    print("message: '", result[0]['generated_text'], "'")


def analyze_sentiment(text_to_analyse):
    # Crear un cliente de la API de Google Cloud Natural Language
    client = language_v1.LanguageServiceClient()

    # Crear un documento con el texto a analizar
    document = language_v1.Document(content=text_to_analyse, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Realizar el análisis de sentimiento
    response = client.analyze_sentiment(request={'document': document})

    # Obtener el sentimiento del texto
    sentiment = response.document_sentiment

    print(f"Score: {sentiment.score}, Magnitude: {sentiment.magnitude}")


def gemini_generative_text(player, cpu):
    gemini.configure(api_key='AIzaSyCJY0k_toVwRUSoAWgi4pL3tRrxAY9v48c')
    model = gemini.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Teniendo en cuenta la siguiente puntuacion y como si se siguiera jugando," +
                                      " genera un muy breve texto de aliento o felicitaciones " +
                                      "(sin incluir el puntaje en la respuesta), segun corresponda. " +
                                      f"Jugador: {player}, cpu: {cpu}")
    print(response.text)


if __name__ == '__main__':
    text = "Google Cloud Natural Language API es muy útil para el análisis de texto."
    # analyze_sentiment(text)
    gemini_generative_text(40, 15)
