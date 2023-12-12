# drf_project

# README для создания и запуска Docker-образа из Dockerfile

Этот README объяснит, как создать и запустить Docker-образ с использованием Dockerfile. Dockerfile - это текстовый файл, который содержит инструкции для создания Docker-образа, и это удобный способ упаковать и распространить приложение со всеми его зависимостями.

## Шаг 1: Установка Docker

Прежде чем начать, убедитесь, что у вас установлен Docker. Если у вас его нет, следуйте инструкциям на [официальном сайте Docker](https://docs.docker.com/get-docker/) для установки Docker на вашей операционной системе.

## Шаг 2: Сборка Docker-образа

1. Откройте терминал и перейдите в папку вашего проекта:

   ```bash
   cd /path/to/my-docker-project
   ```

2. Выполните команду сборки Docker-образа:

   ```bash
   docker build -t my-docker-image .
   ```

   Где `my-docker-image` - это имя, которое вы хотите присвоить вашему образу, а `.` означает текущую директорию (где находится Dockerfile).

## Шаг 3: Запуск Docker-контейнера

1. После успешной сборки образа можно запустить Docker-контейнер:

   ```bash
   docker run -d --name my-container my-docker-image
   ```

   Где `my-container` - это имя контейнера, которое вы хотите использовать, а `my-docker-image` - имя вашего Docker-образа.

2. Теперь ваш Docker-контейнер запущен, и ваше приложение должно быть доступно. Вы можете проверить его логи или выполнить другие действия с контейнером, используя команды Docker.
