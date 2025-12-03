FROM paddlepaddle/paddle:2.5.2-gpu-cuda12.0-cudnn8.9-trt8.6
EXPOSE 8000

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install necessary operating system packages
RUN apt-get update \
    && apt-get install -y build-essential libssl-dev libffi-dev python3-dev poppler-utils \
                          tesseract-ocr ffmpeg libsm6 libxext6 unixodbc-dev curl apt-utils \
                          libmariadb-dev python3-tk pkg-config python3 python3-pip

# Clean up APT when done
RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt

WORKDIR /app
COPY . /app
COPY trained_models/extra_files/paddleocr.py /usr/local/lib/python3.10/dist-packages/paddleocr
COPY trained_models/extra_files/env.py /usr/local/lib/python3.10/dist-packages/paddlenlp/utils

# RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
# USER appuser

RUN python3 manage.py collectstatic --no-input

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "api_channel.wsgi:application", "-t", "300"]
# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
