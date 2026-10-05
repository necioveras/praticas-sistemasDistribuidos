import asyncio
import websockets

HOST = "127.0.0.1"
PORT = 5000


async def atender_cliente(websocket):
    cliente = websocket.remote_address

    print(f"Cliente conectado: {cliente}")

    try:
        # Mensagem inicial
        await websocket.send(
            "Bem-vindo! Envie uma mensagem (ou 'exit' para sair)."
        )

        # Aguarda mensagens
        async for mensagem in websocket:

            print(f"Por {cliente}: {mensagem}")

            if mensagem.strip().lower() == "exit":
                await websocket.send("Tchau!")
                break

            resposta = "ECHO: " + mensagem.upper()

            await websocket.send(resposta)

    except websockets.exceptions.ConnectionClosed:
        print(f"Conexão perdida: {cliente}")

    finally:
        print(f"Conexão encerrada: {cliente}")


async def main():

    print(f"Servidor WebSocket iniciado em {HOST}:{PORT} ...")

    async with websockets.serve(
        atender_cliente,
        HOST,
        PORT
    ):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())