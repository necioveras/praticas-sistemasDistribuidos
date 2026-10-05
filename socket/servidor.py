# server.py
# Python 3.11

import socket
import threading

HOST = "0.0.0.0"
PORT = 8081


def atender_cliente(client_socket, client_address):
    """
    Trata a comunicação com um cliente.
    Esta função será executada em uma thread separada.
    """

    print(f"Cliente conectado: {client_address}")

    try:
        # Cria uma interface semelhante ao BufferedReader/PrintWriter do Java.
        # Facilita trabalhar com mensagens terminadas por \n.
        with client_socket.makefile(
            "r",
            encoding="utf-8",
            newline="\n"
        ) as entrada:

            with client_socket.makefile(
                "w",
                encoding="utf-8",
                newline="\n"
            ) as saida:

                saida.write(
                    "Bem-vindo! Envie uma mensagem "
                    "(ou 'exit' para sair).\n"
                )
                saida.flush()

                # Equivalente ao:
                # while ((line = in.readLine()) != null)
                for linha in entrada:

                    linha = linha.strip()

                    if linha.lower() == "exit":
                        saida.write("Tchau!\n")
                        saida.flush()
                        break

                    # Echo com transformação
                    resposta = "ECHO: " + linha.upper()

                    saida.write(resposta + "\n")
                    saida.flush()

                    print(
                        f"Por {client_address}: {linha}"
                    )

    except (ConnectionResetError, BrokenPipeError):
        print(f"Cliente {client_address} desconectou abruptamente.")

    except OSError as erro:
        print(f"Erro na conexão com {client_address}: {erro}")

    finally:
        client_socket.close()
        print(f"Conexão encerrada: {client_address}")


def main():

    # AF_INET  -> IPv4
    # SOCK_STREAM -> TCP
    with socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    ) as servidor:

        # Permite reutilizar rapidamente a porta após reiniciar o servidor
        servidor.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
        )

        servidor.bind((HOST, PORT))

        servidor.listen()

        print(f"Servidor iniciado na porta {PORT} ...")

        while True:

            # Bloqueia até algum cliente conectar
            client_socket, client_address = servidor.accept()

            # Cria uma thread para atender o cliente
            thread = threading.Thread(
                target=atender_cliente,
                args=(client_socket, client_address),
                daemon=True
            )

            thread.start()


if __name__ == "__main__":
    main()