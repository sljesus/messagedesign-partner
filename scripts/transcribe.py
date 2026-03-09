import subprocess

# Asegúrate de que el video esté en el mismo directorio, nombrado 'demo_video.mp4'
# Instala Whisper si no lo tienes: pip install openai-whisper
# Ejecuta: python transcribe.py

subprocess.run(['python', '-m', 'whisper', '696f99eeeb392b34c9fb4c9e.mp4', '--language', 'es', '--output_format', 'txt'])
