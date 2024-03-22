# mindsupport API Documentation

Essa é a API do projeto mindsupport de terapia coletiva.

## Getting Started

Para usar a API do mindsupport:

1. Instale as dependências(`pip install -r requirements.txt`).
2. Adicione as configurações, coloque o arquivo do firebase no diretório de `api` e mude o caminho em `firebase_config.py`.
3. Rode o servidor(`python manage.py runserver`).

## Endpoints

Os seguintes endpoints estão disponíveis na API:

- `/api/v1/register/ - POST`: Cria um usuário. 
    Payload: {
        "email": "example@example.com",
        "password": "okayeg"
    }

- `/api/v1/register/moderator/ - POST`: Cria um usuário. 
    Payload: {
        "email": "example@example.com",
        "password": "okayeg",
        "reason": "razão qualquer"
    }

- `/api/v1/login/ - POST`: Faz login do usuário. 
    Payload: {
        "email": "example@example.com",
        "password": "okayeg"
    }
    
- `/api/v1/themes/ - GET e POST`: Pega/Cria os temas que salas podem ter. 
    Payload: [
	{
		"id": 1,
		"name": "Ansiedade"
	}
]
- `/api/v1/rooms/ - GET e POST`: Pega/Cria as salas podem ter. 
    Payload: [
	{
		"id": 1,
		"theme": 1,
		"room_capacity": 0
	},
	{
		"id": 2,
		"theme": 1,
		"room_capacity": 0
	}
]
- `/api/v1/addUser/ - POST`: Usuário se adiciona a uma sala. 
    Payload: 
        {
            "sala": 1
        }
- `/api/v1/removeUser/ - POST`: Usuário se remove de uma sala. 
    Payload: 
        {
            "sala": 1
        }
- `/api/v1/user/ - GET e POST`: Obtém informações de um usuário. 
    Payload: 
        {
            "id": 9,
            "username": "SpeederVintage77",
            "is_moderator": false,
            "created_at": "Mar 21"
        }
- `/api/v1/user/ - GET e POST`: Obtém informações de um usuário. 
Payload: 
    {
        "id": 9,
        "username": "SpeederVintage77",
        "is_moderator": false,
        "created_at": "Mar 21"
    }
- `/api/v1/denounce/ - POST`: Denuncia um usuário. 
    Payload: 
    {
        "user": 2,
        "block_reason": "É um fuleragi"
    }
- `/api/v1/roomMessages/ - GET`: Pega as mensagens de uma sala. 
    Payload: 
    [
        {
            "message": "",
            "room": 1,
            "timestamp": "Mar 22",
            "audio": "https://storage.googleapis.com/mindsupport-5da6e.appspot.com/124-1-2024-03-22%2021%3A47%3A45.775171.mp3?Expires=1742680069&GoogleAccessId=firebase-adminsdk-jtayr%40mindsupport-5da6e.iam.gserviceaccount.com&Signature=ShABXguBXHVwtYhAJIz1lNNfZslfnvoNslRr5A5sYITQtPHHAbhPnWYFLonfrpyhDemPfeKjLiMVjy1JZgZXYG6B0rO1dTSkqpFg8qTFu472iSeAgjkh4HYkFmGMEoBc0WHZ0uavNJ9te54txkwWht4KoFPRgwTIi0Jf%2BmtmzD%2FFD%2BUPUBiCV9PqXEaWPo%2BuPT68SK31XYaBEWuywlEP3g8uGBwwAXzNLQOV8ZQB5dKACCCddABZf%2BvFUICOG42nyHP425cg3yjOiAxgHkmEL4QjXKC5rw7iQy6H7nPuHFJsdRLcwcsmyZN9VVBq6ghHUTSxwQ6RfHPkHemYDa9zBQ%3D%3D",
            "username": "124",
            "hour": "21:47:49"
        },
        {
            "message": "hahahah",
            "room": 1,
            "timestamp": "Mar 22",
            "audio": "",
            "username": "124",
            "hour": "21:47:24"
        }
    ]

## Web Sockets

WebSockets são usadas para os chats dentro das salas.
Para isso, com o backend rodando conecte-se a ws://127.0.0.1:8000/ws/<room-number>/

O formato da payload é 

{
    "username": "124",
    "user_id": 6,
    "message": "",
    "audio": "/path/to/file"
}
