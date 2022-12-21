# Тестовое задание SHiFT

---

### Запуск:
`make docker_run`

### Запуск тестов:
`make docker_test`
<br/>
<br/>

## Endpoints

---

`GET /api/balance`

### Query params

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|address|query|string|true|Адрес аккаунта, баланс которого необходимо узнать|
|block_number|query|integer|false|Номер блока на момент которого получаем баланс (если не передано - вернется текущий баланс)|
|network|query|string|false|Сеть, допустимые значения: `avax/eth`|
### Response
```
int
```

---
`GET /api/contract_events`

### Query params

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|from_block|query|integer|true|Номер блока начиная с которого необходимо получить события|
|to_block|query|integer|false|Номер блока до которого необходимо получить события (если не передано - получаем события до текущего блока) |
|contract|query|string|false|Адрес контракта события которого необходимо получить (если не передано - получаем события для контракта из ТЗ)|

### Response

```json
[
  {
    "args": {},
    "event": "string",
    "logIndex": 0,
    "transactionIndex": 0,
    "transactionHash": "string",
    "address": "string",
    "blockHash": "string",
    "blockNumber": 0
  }
]
```
