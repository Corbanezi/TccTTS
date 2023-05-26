import openai 
import speech_recognition as sr  
import whisper 
import pyttsx3  
import os

openai.api_key = ""

sem_palavra_ativadora = True

debug_custo = False

debugar = False
# escolher_stt = "whisper"
escolher_stt = "google"
entrada_por_texto = False
falar = True

if entrada_por_texto:
    sem_palavra_ativadora = True

def generate_answer(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1000,
        temperature=0.5
    )
    return [response.choices[0].message.content, response.usage]


def talk(texto):
    engine.say(texto)
    engine.runAndWait()
    engine.stop()


def save_file(dados):
    with open(path + filename, "wb") as f:
        f.write(dados)
        f.flush()

r = sr.Recognizer()
mic = sr.Microphone()
model = whisper.load_model("base")

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('rate', 180)
voz = 0  
engine.setProperty('voice', voices[voz].id)

mensagens = [{"role": "system", "content": "Você é um assistente gente boa. E meu nome é Bob!"}]

path = os.getcwd()
filename = "audio.wav"

print("Fale com o assistente!")

ajustar_ambiente_noise = True

while True:
    text = ""
    question = ""

    if entrada_por_texto:
        question = input("Tire suas dúvidas com o CHATGPT / Para sair -> (\"sair\"): ")
    else:
        with mic as fonte:
            if ajustar_ambiente_noise:
                r.adjust_for_ambient_noise(fonte)
                ajustar_ambiente_noise = False
            print("Faça sua pergunta")
            audio = r.listen(fonte)
            print("Reconhecendo...")

            if escolher_stt == "google":
                question = r.recognize_google(audio, language="pt-BR")
            elif escolher_stt == "whisper":
                save_file(audio.get_wav_data())

        if escolher_stt == "whisper":
            text = model.transcribe(path + filename, language='pt', fp16=False)
            question = text["text"]

    if ("desligar" in question and "assistente" in question) or question.startswith("sair"):
        print(question, "Saindo.")
        if falar:
            talk("Okay...até mais")
        break
    elif question == "":
        print("No sound")
        continue
    elif question.startswith("Assistente") or question.startswith("assistente") or question.startswith(
            "chat GPT") or sem_palavra_ativadora:
        print("Eu:", question)
        mensagens.append({"role": "user", "content": str(question)})

        answer = generate_answer(mensagens)

        print("Resposta ChatGPT:", answer[0])

        if debug_custo:
            print("Cost:\n", answer[1])

        mensagens.append({"role": "assistant", "content": answer[0]})

        if falar:
            talk(answer[0])
    else:
        print("No message")
        continue

    if debugar:
        print("Mensages", mensagens, type(mensagens))
print("Até a próxima!")
