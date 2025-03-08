# Kokoro Text-to-Speech

Kokoro is a high-quality text-to-speech (TTS) system that converts text files into natural-sounding audiobooks using various AI voices. This project provides a simple interface for generating audio content from text with multiple voice options in both American and British English.

## Features

- Convert text files to audio in MP3, MP4, or M4A formats
- Choose from 28 different voices (20 American English, 8 British English)
- Automatic text splitting and processing
- High-quality neural text-to-speech synthesis

## Installation

### Prerequisites

The project requires ffmpeg and espeak-ng to be installed on your system. You can install these dependencies by running:

```bash
./start.sh
```

### Python Environment Setup

1. Create a Python virtual environment (optional but recommended):

```bash
python -m venv /path/to/kokoro
cd /path/to/kokoro
source bin/activate
```

2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Usage

### Converting Text to Audio

Use the `book.py` script to convert text files to audio:

```bash
python book.py path/to/textfile.txt [--voice VOICE] [--format FORMAT]
```

#### Parameters:

- `text_file`: Path to the text file you want to convert
- `--voice`: Voice to use for text-to-speech (default: "af_heart")
- `--format`: Output audio format - mp3, mp4, or m4a (default: mp3)

### Example:

```bash
python book.py books/Test.txt --voice af_nova --format mp3
```

### Testing Voices

To test all available voices and generate sample audio for each:

```bash
python voice_test.py
```

This will create WAV files for each voice saying a sample phrase.

## Available Voices

### American English Voices:

- af_heart, af_alloy, af_aoede, af_bella, af_jessica
- af_kore, af_nicole, af_nova, af_river, af_sarah
- af_sky, am_adam, am_echo, am_eric, am_fenrir
- am_liam, am_michael, am_onyx, am_puck, am_santa

### British English Voices:

- bf_alice, bf_emma, bf_isabella, bf_lily
- bm_daniel, bm_fable, bm_george, bm_lewis

Voice naming convention:

- First letter: 'a' for American, 'b' for British
- Second letter: 'f' for female, 'm' for male
- After underscore: voice name

## Project Structure

```
kokoro/
├── book.py           # Main script for converting text to audio
├── meta.py           # Lists of available voices
├── voice_test.py     # Script to test all voices
├── requirements.txt  # Python dependencies
├── start.sh          # Script to install system dependencies
└── books/            # Directory for text files to be converted
```

## Performance

The system will output timing information after processing, including:

- Total processing time
- Audio duration
- Processing speed relative to real-time speech

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.
