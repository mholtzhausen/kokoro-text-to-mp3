#!/usr/bin/env python3

import argparse
import os
import numpy as np
import soundfile as sf
from kokoro import KPipeline
import subprocess
from meta import american_voices, british_voices, all_english_voices
import warnings
import time

# Suppress specific PyTorch warnings
warnings.filterwarnings("ignore", message="dropout option adds dropout after all but last recurrent layer")
warnings.filterwarnings("ignore", message="`torch.nn.utils.weight_norm` is deprecated in favor of")

def process_text_file(text_file, voice='af_heart', format='mp3'):
    # Start timing the process
    start_time = time.time()
    
    # Determine language code based on voice prefix
    lang_code = 'a' if voice.startswith('a') else 'b'
    
    # Extract directory and filename from the input path
    file_dir = os.path.dirname(text_file)
    if not file_dir:
        file_dir = os.getcwd()
    base_name = os.path.splitext(os.path.basename(text_file))[0]
    
    # Read the text file
    with open(text_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    print(f"Processing file '{text_file}' with voice '{voice}'")
    
    # Create pipeline with appropriate language code
    pipeline = KPipeline(lang_code=lang_code, repo_id='hexgrad/Kokoro-82M')
    
    # Generate audio
    generator = pipeline(
        text, voice=voice,
        speed=1, split_pattern=r'\n\r\r\r\n\n\n\r\n+'
    )
    
    # Collect all audio segments and save individual files
    all_audio = []
    wav_files = []
    
    for i, (gs, ps, audio) in enumerate(generator):
        print(f"  Segment {i}: {gs[:30]}...")
        all_audio.append(audio)
        
        # Save individual wav file in the same directory as the text file
        # Prefix with voice name
        segment_file = os.path.join(file_dir, f"{voice} - {base_name}_{i:03d}.wav")
        sf.write(segment_file, audio, 24000)
        wav_files.append(segment_file)
        print(f"  Saved {segment_file}")
    
    # Concatenate all audio segments and save to combined wav file
    if all_audio:
        combined_audio = np.concatenate(all_audio)
        # Prefix combined wav with voice name
        combined_wav = os.path.join(file_dir, f"{voice} - {base_name}.wav")
        sf.write(combined_wav, combined_audio, 24000)
        print(f"  Saved combined audio to {combined_wav}")
        
        # Convert WAV to selected format using ffmpeg
        output_file = os.path.join(file_dir, f"{voice} - {base_name}.{format}")
        
        # Set ffmpeg quality based on format
        if format == 'mp3':
            quality_param = ['-q:a', '2']
        elif format in ['mp4', 'm4a']:
            quality_param = ['-c:a', 'aac', '-b:a', '192k']
        
        subprocess.run(['ffmpeg', '-i', combined_wav] + quality_param + [output_file])
        print(f"  Converted to {format.upper()}: {output_file}")
        
        # Remove intermediary audio files
        for wav_file in wav_files:
            os.remove(wav_file)
            print(f"  Removed intermediary file: {wav_file}")
        
        # Optionally remove the combined WAV file as well
        os.remove(combined_wav)
        print(f"  Removed combined WAV file: {combined_wav}")
        
        # Calculate timing information
        end_time = time.time()
        processing_time = end_time - start_time
        audio_duration = len(combined_audio) / 24000  # duration in seconds (sample rate is 24000)
        
        # Calculate and print the ratio
        speed_ratio = audio_duration / processing_time
        
        print(f"\nTotal processing time: {processing_time:.2f} seconds")
        print(f"Audio duration: {audio_duration:.2f} seconds ({audio_duration/60:.2f} minutes)")
        print(f"Encoded at {speed_ratio:.2f} × speech speed")

def main():
    parser = argparse.ArgumentParser(description="Convert text file to audio book")
    parser.add_argument("text_file", help="Path to the text file to convert")
    parser.add_argument("--voice", default="af_heart", choices=all_english_voices,
                      help="Voice to use for text-to-speech")
    parser.add_argument("--format", default="mp3", choices=["mp3", "mp4", "m4a"],
                      help="Output audio format (default: mp3)")
    args = parser.parse_args()
    
    # Check if the text file exists
    if not os.path.isfile(args.text_file):
        print(f"Error: Text file '{args.text_file}' not found")
        return
    
    process_text_file(args.text_file, args.voice, args.format)

if __name__ == "__main__":
    main()
