FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    # wget \
    # curl \
    # unzip \
    # ca-certificates \
    # fontconfig \
    # libglib2.0-0 \
    # libnss3 \
    # libxss1 \
    # libgdk-pixbuf2.0-0 \
    # libdbus-1-3 \
    # libxtst6 \
    # libx11-xcb1 \
    # libxcomposite1 \
    # libxdamage1 \
    # libatk-bridge2.0-0 \
    # libatk1.0-0 \
    # libgbm1 \
    # libasound2 \
    # libepoxy0 \
    # x11-utils \
    # libxrandr2 \
    # libxv1 \
    # xvfb \

    python3-tk \

    && apt-get clean

# RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

# RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

# RUN pip install selenium

RUN pip install requests bs4

WORKDIR /app

COPY . /app

CMD ["python", "app.py"]