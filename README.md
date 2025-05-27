# Web service de uma loja de confecções

## Descrição

Esse web service foi projetado para ser consumido por uma aplicação front-end.
Contendo informações sobre os clientes, produtos e pedidos feitos para a loja entregar.
O objetivo do projeto foi facilitar o gerencimento dessas informações e criar endpoints para que, integrando o serviço com o front-end, a aplicação funcione da maneira esperada.

## Funcionalidades

- **Segurança:** Os endpoints da API são restritos á usuários logados no serviços, logados por meio de token de segurança.
- **Validações:** Os dados inseridos passam por validações.
- **Filtros:** O serviço oferece diversos tipos de filtros para obter melhores informações dos dados armazenados.
- **Deploy** O serviço foi hospedado na url: https://backend-teste-ck2n.onrender.com/ usando o dockerHub para fazer deploy no render.

## Tecnologias Utilizadas

- **Backend:** Python, FastAPI
- **Banco de Dados:** SQLite
- **Outros:** Postman, Docker, Render
