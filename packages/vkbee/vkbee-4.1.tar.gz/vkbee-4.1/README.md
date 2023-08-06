﻿![vkbee](https://github.com/vkbee/vkbee/raw/master/logo.png)
<h1 align="center">VKBee - простая в использовании библиотека для взаимодействия с API ВКонтакте</h1>
<p align="center">
    <img alt="Made with Python" src="https://img.shields.io/badge/Made%20with-Python-%23FFD242?logo=python&logoColor=white">
    <img alt="Downloads" src="https://pepy.tech/badge/vkbee">
    <img alt="License" src="https://img.shields.io/github/license/asyncvk/vkbee?style=flat-square)">
</p>

## Установка
Из PyPI:
```bash
$ pip install vkbee
```
Из GitHub (рекомендуется):
```bash
$ pip install https://github.com/vkbee/vkbee/archive/master.zip
```
> Минимальная версия Python - 3.6

## Пример использования
```python
import asyncio
import vkbee

from vkbee.longpoll import BotLongpoll, Session
from vkbee import API

async def main(loop):
    vk_session = Session(token='token', loop=loop)
    longpoll = BotLongpoll(vk_session, 'groupid', 10)

    async for event in longpoll.events():
        user_id = event['object']['message']['from_id']
        message_text = event['object']['message']['text']
        
        await API.call(vk_session, 'messages.send', {'user_id': user_id, 'message': message_text, 'random_id': 0})

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
```

Более расширенное использование описано в [документации](https://github.com/vkbee/vkbee/blob/master/docs/docs.md)

# Сообщество
Soon
