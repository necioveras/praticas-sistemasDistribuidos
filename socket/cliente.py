# Client.py (Python 3.11)

import socket
import sys


def main():
    # Recupera host e porta dos argumentos da linha de comando.
    # Caso não sejam informados, utiliza os valores padrão.
    host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 5000

    print(f"Conectando em {host}:{port} ...")

    try:
        # Cria o socket TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

            # Conecta ao servidor
            sock.connect((host, port))

            # Cria interfaces de leitura e escrita em UTF-8
            server_in = sock.makefile(
                "r",
                encoding="utf-8"
            )

            server_out = sock.makefile(
                "w",
                encoding="utf-8"
            )

            # Lê a mensagem de boas-vindas do servidor
            mensagem = server_in.readline()

            if mensagem:
                print(mensagem.strip())

            while True:

                # Lê uma mensagem digitada pelo usuário
                try:
                    user_input = input("> ")
                except EOFError:
                    break

                # Envia ao servidor
                server_out.write(user_input + "\n")
                server_out.flush()

                # Aguarda a resposta
                resposta = server_in.readline()

                # String vazia indica que o servidor
                # encerrou a conexão
                if not resposta:
                    print("(Servidor encerrou a conexão)")
                    break

                print(resposta.strip())

                # Encerra caso o usuário tenha digitado exit
                if user_input.strip().lower() == "exit":
                    break

            server_in.close()
            server_out.close()

    except OSError as e:
        print(f"Erro: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()