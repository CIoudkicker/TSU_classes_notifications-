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

### Интеграционное тестирование
1. [kafka-connection-test](https://github.com/CIoudkicker/TSU_classes_notifications-/blob/test/tsu-schedule-backend/kafka-connection-test.md)   (Протестируйте соединение с Кафкой ), для .js ([kafka-connection-test.js](https://github.com/CIoudkicker/TSU_classes_notifications-/blob/test/tsu-schedule-backend/kafka-connection-test.js))
2. [message-production-consumption-test](https://github.com/CIoudkicker/TSU_classes_notifications-/blob/test/tsu-schedule-backend/message-production-consumption-test.md)    (Производство и потребление тестовых сообщений),для .js ([message-production-consumption-test.js](https://github.com/CIoudkicker/TSU_classes_notifications-/blob/test/tsu-schedule-backend/message-production-consumption-test.js))
3. [kafka-performance-test](https://github.com/CIoudkicker/TSU_classes_notifications-/blob/test/tsu-schedule-backend/kafka-performance-test.md)     (кафка тест производительности),Нет файла .js, в результате получается файл .md
4. [Kafka startup process](https://github.com/CIoudkicker/TSU_classes_notifications-/blob/test/tsu-schedule-backend/Kafka-startup-process.md) ( процесс запуска Kafka в Docker Compose),Нет файла .js, в результате получается файл .md. Эта проблема была исправлена ​​с разработчиком
### модульный тест
5. [unit-test-report.md](https://github.com/CIoudkicker/TSU_classes_notifications-/blob/test/tsu-schedule-backend/unit-test-report.md),для .js path "/tsu-schedule-backend/controller/controllers" 1. ([userController-getSchedulestat.test.js](https://github.com/CIoudkicker/TSU_classes_notifications-/blob/test/tsu-schedule-backend/controller/controllers/userController-getSchedulestat.test.js))  2.([userController-login.test.js](https://github.com/CIoudkicker/TSU_classes_notifications-/blob/test/tsu-schedule-backend/controller/controllers/userController-login.test.js))

### тест интерфейса
6.  [Login-interface-test](https://github.com/CIoudkicker/TSU_classes_notifications-/blob/test/tsu-schedule-backend/Login-interface-test.md)  (Логин-интерфейс-тест),Нет файла .js, в результате получается файл .md
7. [Test-interface-getschedule](https://github.com/CIoudkicker/TSU_classes_notifications-/blob/test/tsu-schedule-backend/Test-interface-getschedule.md) (тест интерфейса showSchedule,получение информации об учебной программе),Нет файла .js, в результате получается файл .md