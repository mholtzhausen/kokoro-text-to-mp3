from kokoro import KPipeline
import soundfile as sf
import numpy as np
from meta import american_voices, british_voices, all_english_voices

# American English voices


# You can also access all English voices combined if needed

def process_voice(voice, lang_code):
    # Create pipeline with appropriate language code
    pipeline = KPipeline(lang_code=lang_code)
    
    # Create text with the voice name inserted
    text = f'''
Hello this is {voice}. I am a text-to-speech voice. This is a voice-test.
'''
    
    print(f"Processing {voice} with language code {lang_code}")
    
    # Generate audio
    generator = pipeline(
        text, voice=voice,
        speed=1, split_pattern=r'\nJuStAsTrInGtHaTwIlLnEvErOcCuR\n+'
    )
    
    # Collect all audio segments
    all_audio = []
    for i, (gs, ps, audio) in enumerate(generator):
        print(f"  Segment {i}: {gs[:30]}...")
        print(f"  Phonemes: {ps[:30]}...")
        all_audio.append(audio)
    
    # Concatenate all audio segments and save to file
    if all_audio:
        combined_audio = np.concatenate(all_audio)
        sf.write(f'{voice}.wav', combined_audio, 24000)
        print(f"  Saved {voice}.wav")

# Process American English voices
print("\nProcessing American English voices...")
for voice in american_voices:
    process_voice(voice, 'a')

# Process British English voices
print("\nProcessing British English voices...")
for voice in british_voices:
    process_voice(voice, 'b')
