# servidor.py
# Python 3.11

import socket
import threading

HOST = "0.0.0.0"
PORT = 5000


def atender_cliente(conexao, endereco):
    """
    Trata a comunicação com um cliente.
    Cada cliente é atendido em uma thread separada.
    """

    print(f"Cliente conectado: {endereco}")

    try:
        # makefile permite trabalhar com linhas,
        # de forma semelhante ao BufferedReader/PrintWriter do Java.
        entrada = conexao.makefile("r", encoding="utf-8")
        saida = conexao.makefile("w", encoding="utf-8")

        # Mensagem inicial
        saida.write(
            "Bem-vindo! Envie uma mensagem (ou 'exit' para sair).\n"
        )
        saida.flush()

        # Aguarda mensagens do cliente
        for linha in entrada:

            # Remove \n enviado pelo cliente
            mensagem = linha.rstrip("\r\n")

            # Verifica se o cliente deseja sair
            if mensagem.strip().lower() == "exit":
                saida.write("Tchau!\n")
                saida.flush()
                break

            # Echo com transformação para maiúsculas
            resposta = "ECHO: " + mensagem.upper()

            saida.write(resposta + "\n")
            saida.flush()

            print(f"Por {endereco}: {mensagem}")

    except (ConnectionResetError, BrokenPipeError, OSError) as erro:
        print(f"Conexão encerrada: {erro}")

    finally:
        conexao.close()
        print(f"Cliente desconectado: {endereco}")


def main():

    # Cria um socket IPv4/TCP
    servidor = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    # Permite reutilizar rapidamente a porta após reiniciar o servidor
    servidor.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    # Associa o socket à porta 5000
    servidor.bind((HOST, PORT))

    # Coloca o socket em modo de escuta
    servidor.listen()

    print(f"Servidor iniciado na porta {PORT} ...")

    try:
        while True:

            # Fica bloqueado aguardando um cliente
            conexao, endereco = servidor.accept()

            # Cria uma thread para atender o cliente
            thread = threading.Thread(
                target=atender_cliente,
                args=(conexao, endereco),
                daemon=True
            )

            thread.start()

    except KeyboardInterrupt:
        print("\nServidor encerrado.")

    finally:
        servidor.close()


if __name__ == "__main__":
    main()