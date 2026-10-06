# cliente.py
# Python 3.11

import socket
import sys


# Host informado pela linha de comando.
# Se não for informado, utiliza localhost.
HOST = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"

# Porta informada pela linha de comando.
# Se não for informada, utiliza 5000.
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 5000


def main():

    print(f"Conectando em {HOST}:{PORT} ...")

    try:
        # Cria um socket IPv4 utilizando TCP
        with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        ) as cliente:

            # Conecta ao servidor
            cliente.connect((HOST, PORT))

            # Cria streams de leitura e escrita em UTF-8
            entrada = cliente.makefile(
                "r",
                encoding="utf-8"
            )

            saida = cliente.makefile(
                "w",
                encoding="utf-8"
            )

            # Recebe a mensagem inicial do servidor
            mensagem = entrada.readline()

            if not mensagem:
                print("(Servidor encerrou a conexão)")
                return

            print(mensagem.rstrip("\r\n"))

            # Comunicação com o servidor
            while True:

                # Lê mensagem digitada pelo usuário
                user_input = input("> ")

                # Envia para o servidor
                saida.write(user_input + "\n")
                saida.flush()

                # Aguarda resposta do servidor
                resposta = entrada.readline()

                if not resposta:
                    print("(Servidor encerrou a conexão)")
                    break

                print(resposta.rstrip("\r\n"))

                # Encerra caso o usuário tenha digitado exit
                if user_input.strip().lower() == "exit":
                    break

    except ConnectionRefusedError:
        print("Erro: conexão recusada pelo servidor.")

    except socket.gaierror:
        print("Erro: endereço do servidor não encontrado.")

    except OSError as erro:
        print(f"Erro: {erro}")


if __name__ == "__main__":
    main()