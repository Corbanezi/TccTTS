import openai
import speech_recognition as sr
import pyttsx3
import time

openai.api_key = ""
falar = True
escolher_stt = "google"
tempo_limite_inatividade_segundos = 600  # 10 minutos

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

r = sr.Recognizer()
mic = sr.Microphone()

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('rate', 180)
voz = 0
engine.setProperty('voice', voices[voz].id)

mensagens = [{"role": "system", "content": "Você é um assistente gente boa."}]

print("Fale com o assistente!")

ajustar_ambiente_noise = True
inatividade_start_time = time.time()

while True:
    question = ""

    try:
        with mic as fonte:
            if ajustar_ambiente_noise:
                r.adjust_for_ambient_noise(fonte)
                ajustar_ambiente_noise = False
            print("Faça sua pergunta")
            audio = r.listen(fonte)
            print("Reconhecendo...")
            question = r.recognize_google(audio, language="pt-BR")
    except sr.UnknownValueError:
        print("Não foi possível reconhecer a fala. Aguardando mais uma tentativa...")
        continue

    if time.time() - inatividade_start_time >= tempo_limite_inatividade_segundos:
        print("Tempo limite de inatividade atingido. O aplicativo está em espera.")
        continue

    if question.startswith("assistente desligar"):
        print(question, "te vejo uma outra hora!")
        if falar:
            talk("Okay...até mais")
        break
    elif question == "":
        print("No sound")
        continue
    elif question.startswith("assistente"):
        print("Eu:", question)
        mensagens.append({"role": "user", "content": str(question)})

        answer = generate_answer(mensagens)

        print("Resposta chatFHO:", answer[0])

        mensagens.append({"role": "assistant", "content": answer[0]})

        if falar:
            talk(answer[0])

        inatividade_start_time = time.time()

print("chatFHO: Até a próxima!")