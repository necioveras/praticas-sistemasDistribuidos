// Client.java (Java 8)
import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;

public class Client {
    public static void main(String[] args) {
        String host = (args.length > 0) ? args[0] : "127.0.0.1";
        int port = (args.length > 1) ? Integer.parseInt(args[1]) : 5000;

        System.out.println("Conectando em " + host + ":" + port + " ...");

        try (
            Socket socket = new Socket(host, port);
            BufferedReader serverIn = new BufferedReader(
                new InputStreamReader(socket.getInputStream(), StandardCharsets.UTF_8));
            PrintWriter serverOut = new PrintWriter(
                new OutputStreamWriter(socket.getOutputStream(), StandardCharsets.UTF_8), true);
            BufferedReader console = new BufferedReader(
                new InputStreamReader(System.in, StandardCharsets.UTF_8))
        ) {
            // Lê a mensagem de boas-vindas do servidor
            System.out.println(serverIn.readLine());

            String userInput;
            System.out.print("> ");
            while ((userInput = console.readLine()) != null) {
                serverOut.println(userInput);             // envia ao servidor
                String resposta = serverIn.readLine();    // lê a resposta
                if (resposta == null) {
                    System.out.println("(Servidor encerrou a conexão)");
                    break;
                }
                System.out.println(resposta);
                if ("exit".equalsIgnoreCase(userInput.trim())) break;
                System.out.print("> ");
            }
        } catch (IOException e) {
            System.err.println("Erro: " + e.getMessage());
        }
    }
}
