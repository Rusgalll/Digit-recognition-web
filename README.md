
# Распознавание рукописных цифр через сверточную нейронную сеть
## Загрузка внешних зависимостей
```
pip install -r requirements.txt
```
## Запуск
Все команды выполняются з родительской директории "app"
### Запуск сервера
```
uvicorn app.main:app
```
### Запуск клиента
```
python -m http.server 63342
```
Адрес клиента:
http://localhost:63342/app/frontend/
## Пример
![Example](https://github.com/Rusgalll/Digit-recognition-web/assets/88139430/7aecf557-3884-4a5e-af67-b1efa01b14c7)


