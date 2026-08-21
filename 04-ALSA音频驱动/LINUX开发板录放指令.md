# LINUX开发板录放指令

arecord -D hw:0,0 -f S16_LE -r 16000 -c 2 -d 10 record.wav

或

arecord -D plughw:0,0 -f S16_LE -r 16000 -c 1 -d 10 record.wav

aplay record.wav

alsamixer

alsactl store