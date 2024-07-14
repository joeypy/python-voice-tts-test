from TTS.api import TTS
from pydub import AudioSegment
import torch
import os

# Diccionario para clasificar las voces por género
# Nota: Esta es una clasificación aproximada y puede no ser 100% precisa
gender_dict = {
    'p225': 'Mujer', 'p226': 'Mujer', 'p227': 'Hombre', 'p228': 'Hombre', 'p229': 'Mujer',
    'p230': 'Mujer', 'p231': 'Mujer', 'p232': 'Hombre', 'p233': 'Mujer', 'p234': 'Mujer',
    'p236': 'Mujer', 'p237': 'Hombre', 'p238': 'Hombre', 'p239': 'Mujer', 'p240': 'Mujer',
    'p241': 'Mujer', 'p243': 'Hombre', 'p244': 'Hombre', 'p245': 'Hombre', 'p246': 'Hombre',
    'p247': 'Hombre', 'p248': 'Mujer', 'p249': 'Mujer', 'p250': 'Mujer', 'p251': 'Hombre',
    'p252': 'Hombre', 'p253': 'Mujer', 'p254': 'Hombre', 'p255': 'Mujer', 'p256': 'Hombre',
    'p257': 'Mujer', 'p258': 'Hombre', 'p259': 'Mujer', 'p260': 'Mujer', 'p261': 'Mujer',
    'p262': 'Mujer', 'p263': 'Hombre', 'p264': 'Mujer', 'p265': 'Hombre', 'p266': 'Mujer',
    'p267': 'Hombre', 'p268': 'Mujer', 'p269': 'Mujer', 'p270': 'Mujer', 'p271': 'Hombre',
    'p272': 'Mujer', 'p273': 'Hombre', 'p274': 'Hombre', 'p275': 'Hombre', 'p276': 'Mujer',
    'p277': 'Mujer', 'p278': 'Hombre', 'p279': 'Hombre', 'p280': 'Mujer', 'p281': 'Mujer',
    'p282': 'Mujer', 'p283': 'Hombre', 'p284': 'Hombre', 'p285': 'Hombre', 'p286': 'Mujer',
    'p287': 'Hombre', 'p288': 'Mujer', 'p292': 'Hombre', 'p293': 'Mujer', 'p294': 'Mujer',
    'p295': 'Hombre', 'p297': 'Mujer', 'p298': 'Mujer', 'p299': 'Mujer', 'p300': 'Mujer',
    'p301': 'Mujer', 'p302': 'Hombre', 'p303': 'Mujer', 'p304': 'Hombre', 'p305': 'Mujer',
    'p306': 'Mujer', 'p307': 'Mujer', 'p308': 'Mujer', 'p310': 'Mujer', 'p311': 'Hombre',
    'p312': 'Mujer', 'p313': 'Mujer', 'p314': 'Mujer', 'p316': 'Mujer', 'p317': 'Mujer',
    'p318': 'Mujer', 'p323': 'Mujer', 'p326': 'Hombre', 'p329': 'Mujer', 'p330': 'Mujer',
    'p333': 'Mujer', 'p334': 'Hombre', 'p335': 'Mujer', 'p336': 'Mujer', 'p339': 'Mujer',
    'p340': 'Mujer', 'p341': 'Mujer', 'p343': 'Mujer', 'p345': 'Hombre', 'p347': 'Hombre',
    'p351': 'Hombre', 'p360': 'Mujer', 'p361': 'Mujer', 'p362': 'Mujer', 'p363': 'Hombre',
    'p364': 'Hombre', 'p374': 'Hombre', 'p376': 'Hombre'
}

def get_speaker_choice(speakers):
    if not speakers:
        return None
    
    print("Hablantes disponibles:")
    for i, speaker in enumerate(speakers):
        gender = gender_dict.get(speaker, "Desconocido")
        print(f"{i+1}. {speaker} - {gender}")
    
    while True:
        try:
            choice = int(input("Elige el número del hablante que deseas usar: ")) - 1
            if 0 <= choice < len(speakers):
                return speakers[choice]
            else:
                print(f"Por favor, elige un número entre 1 y {len(speakers)}")
        except ValueError:
            print("Por favor, ingresa un número válido")

def main():
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"Usando dispositivo: {device}")

    # Elegir idioma
    while True:
        language = input("Elige el idioma (en para inglés, es para español latino): ").lower()
        if language in ['en', 'es']:
            break
        print("Por favor, elige 'en' o 'es'.")

    # Inicializar TTS con el modelo correspondiente
    if language == 'en':
        tts = TTS("tts_models/en/vctk/vits").to(device)
    else:
        tts = TTS("tts_models/es/css10/vits").to(device)

    # Obtener lista de hablantes y elegir uno si está disponible
    speakers = tts.speakers
    chosen_speaker = get_speaker_choice(speakers) if speakers else None

    # Texto para sintetizar
    text = input("Introduce el texto que quieres convertir a voz: ")

    # Control de velocidad
    speed = float(input("Introduce la velocidad del habla (1.0 es normal, menor es más lento, mayor es más rápido): "))

    # Genera el audio en WAV
    wav_path = f"output_{language}.wav"
    if chosen_speaker:
        tts.tts_to_file(text=text, file_path=wav_path, speaker=chosen_speaker, speed=speed)
    else:
        tts.tts_to_file(text=text, file_path=wav_path, speed=speed)
    
    # Convierte WAV a MP3
    mp3_path = f"output_{language}.mp3"
    audio = AudioSegment.from_wav(wav_path)
    audio.export(mp3_path, format="mp3")
    
    os.remove(wav_path)

    print(f"El audio se ha guardado en '{mp3_path}'")

if __name__ == "__main__":
    main()