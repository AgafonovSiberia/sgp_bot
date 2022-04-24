#берём образ с докерхаба
FROM python:3.10-slim-bullseye as compile-image

#создаём виртуальное окружение внутри контейра
RUN python -m venv /opt/venv

#берём именно версию, которая лежит в окружении
ENV PATH="/opt/venv/bin:$PATH"

#устанавливаем все пакеты и зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Итоговый образ, в котором будет работать бот
FROM python:3.10-slim-bullseye
COPY --from=compile-image /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
COPY data/access_keys /app/data/access_keys
COPY bot /app/bot
CMD ["python", "-m", "bot"]


