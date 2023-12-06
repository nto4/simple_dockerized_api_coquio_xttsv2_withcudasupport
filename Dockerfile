FROM python:3.10.12-slim

# Update base system
RUN apt-get update 
RUN apt-get upgrade -y 
RUN apt-get install -y --no-install-recommends ca-certificates git ffmpeg vim
RUN apt-get clean -y 

#User define
RUN apt-get install -yq sudo
RUN adduser --uid 1001 --disabled-password --gecos "" appuser
RUN adduser appuser sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER appuser
WORKDIR /home/appuser
# Define Path
ENV PATH="/home/appuser/.local/bin:${PATH}"
# Copy and change ownership of the directories and files
# Copy requirements.txt and install 
COPY --chown=appuser:appuser requirements.txt requirements.txt
RUN pip install --user -r requirements.txt
COPY --chown=appuser:appuser ./voices ./voices
# COPY --chown=appuser:appuser ./weights_0.17.5/tts ./.local/share/tts
RUN /usr/bin/yes | /home/appuser/.local/bin/tts --model_name tts_models/multilingual/multi-dataset/xtts_v2      --text "It took me."      --speaker_wav /home/appuser/voices/michael/Instaread_Audio.mp3      --language_idx en      --out_path /home/appuser/op1.wav 
RUN rm -rf /home/appuser/op1.wav 
RUN rm -rf /home/appuser/process_dir/*

COPY --chown=appuser:appuser ./ ./


RUN chown appuser:appuser ./entrypoint.sh 
RUN chmod 777 ./entrypoint.sh 

# Extra requirements

# Define Entrypoint
USER root
ENTRYPOINT [ "/home/appuser/entrypoint.sh" ]
#ENTRYPOINT [ "/bin/bash" ]