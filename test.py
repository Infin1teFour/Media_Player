from mutagen.wave import WAVE
from mutagen.oggvorbis import OggVorbis

audio = WAVE("media/test.wav")
print(audio.info.length)

audio = OggVorbis("media/test.ogg")
print(audio.info.length)