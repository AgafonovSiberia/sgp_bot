![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)


1. <code><b>git clone ...</b></code>
2. В диретории bot cоздать виртуальное окружение (<code><b>cd bot/ python3.10 -m venv venv</b></code>)
3. Активировать окружение (<code><b>source venv/bin/activate</b></code>)
4. Установить все пакеты (<code><b>pip install -r requirements.txt</b></code>)
5. Заполнить <code>.env_example</code> данными и переименовать в <code>.env_dev</code>
6. Смонтировать образ <code>make build</code>
7. Запустить контейнер <code>make run</code>


Сборка образа через kaniko: <code>make build_kaniko</code>

Запуск образа kaniko: <code>make run_kaniko</code>
