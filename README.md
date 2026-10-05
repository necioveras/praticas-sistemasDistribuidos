# Servidor Java e cliente Python WebSocket

O servidor Java WebSocket escuta em `0.0.0.0:5000/ws`. O cliente interativo é
Python 3.11 e usa a biblioteca `websockets`. No Replit, a porta interna 5000 é
encaminhada para HTTPS público, permitindo conexões seguras (`wss`).

## Executar

O botão Run inicia o servidor Java. Também é possível iniciá-lo no terminal:

```sh
bash run.sh
```

Por padrão, esse comando inicia o servidor WebSocket em `src/socket/`. Para
iniciar o servidor de chat RMI (`ServidorImpl`, em `src/chat/`), use:

```sh
bash run.sh chat
```

O modo `socket` também pode ser informado explicitamente:

```sh
bash run.sh socket
```

Em outra máquina com Python 3.11, instale a dependência e inicie o cliente:

```sh
python3.11 -m pip install "websockets>=17.2"
python3.11 src/socket/client.py wss://<dominio-publico-do-replit>/ws
```

Para testar localmente no mesmo computador do servidor:

```sh
python3.11 src/socket/client.py
```

Também é possível iniciar o cliente pelo script do projeto:

```sh
bash run.sh client wss://<dominio-publico-do-replit>/ws
```

O servidor precisa permanecer em execução. O cliente recebe uma saudação,
envia mensagens e encerra a sessão com `exit`.
