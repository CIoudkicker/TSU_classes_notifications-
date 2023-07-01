# Usage

## Docker Compose

Make sure you have Docker and Docker Compose installed on your machine.

Open a terminal and navigate to the project directory.

Run the following command to build and start the containers:

``
docker-compose up --build
``

## Run producer

Make sure you have NodeJS installed on your machine.

``npm run start:producer`` 

## Run consumer

``npm run start:consumer`` 


## Ниже приведен тестовый файл
1. [Тестовые примери](https://github.com/CIoudkicker/TSU_classes_notifications-/blob/test/tsu-schedule-backend/test%20case.md) всех тестовых заданий прикреплены в отдельном файле (пока обновляются)
2. Для одного и того же имени файла файл `.md` является отчетом о тестировании, а файл` .js` — файлом тестовой программы.

## Вот тесты, которые были сделаны:
1. [kafka-connection-test](https://github.com/CIoudkicker/TSU_classes_notifications-/blob/test/tsu-schedule-backend/kafka-connection-test.md)   (Протестируйте соединение с Кафкой )
2. [message-production-consumption-test](https://github.com/CIoudkicker/TSU_classes_notifications-/blob/test/tsu-schedule-backend/message-production-consumption-test.md)    (Производство и потребление тестовых сообщений)
3. [kafka-performance-test](https://github.com/CIoudkicker/TSU_classes_notifications-/blob/test/tsu-schedule-backend/kafka-performance-test.md)     (кафка тест производительности)
4. Kafka startup process ( процесс запуска Kafka в Docker Compose)