path = "/var/www/html/audios/"

mp3_options = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192'}],
    'outtmpl': path + '%(extractor)s:_%(title)s(%(id)s).%(ext)s',
    'quiet': True}

ogg_options = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'ogg',
        'preferredquality': '192'}],
    'outtmpl': path + '%(extractor)s:_%(title)s(%(id)s).%(ext)s',
    'quiet': True}

wav_options = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '192'}],
    'outtmpl': path + '%(extractor)s:_%(title)s(%(id)s).%(ext)s',
    'quiet': True}

m4a_options = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
        'preferredquality': '192'}],
    'outtmpl': path + '%(extractor)s:_%(title)s(%(id)s).%(ext)s',
    'quiet': True}