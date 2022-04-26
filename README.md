


1. Git clone ...
2. В диретории bot cоздать виртуальное окружение (cd bot/ python3.10 -m venv venv)
3. Активировать окружение (source venv/bin/activate)
4. Установить все пакеты (pip install -r requirements.txt)
5. Заполнить .env_example данными и переименовать в .env_dev
6. Смонтировать образ make build
7. Запустить контейнер make run


Сборка образа через kaniko: make build_kaniko
Запуск образа kaniko: make run_kaniko
