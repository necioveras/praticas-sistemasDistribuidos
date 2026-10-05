// Server.java (Java 8)
import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;

public class Server {
    private static final int PORT = 5000;

    public static void main(String[] args) {
        System.out.println("Servidor iniciado na porta " + PORT + " ...");
        try (ServerSocket serverSocket = new ServerSocket(PORT)) {
            while (true) {
                Socket client = serverSocket.accept(); // espera um cliente
                System.out.println("Cliente conectado: " + client.getRemoteSocketAddress());
                // atende cada cliente em uma thread
                new Thread(new ClientHandler(client)).start();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // Trata um cliente por vez
    static class ClientHandler implements Runnable {
        private final Socket socket;

        ClientHandler(Socket socket) {
            this.socket = socket;
        }

        @Override
        public void run() {
            try (
                BufferedReader in = new BufferedReader(
                    new InputStreamReader(socket.getInputStream(), StandardCharsets.UTF_8));
                PrintWriter out = new PrintWriter(
                    new OutputStreamWriter(socket.getOutputStream(), StandardCharsets.UTF_8), true)
            ) {
                out.println("Bem-vindo! Envie uma mensagem (ou 'exit' para sair).");
                String line;
                while ((line = in.readLine()) != null) {
                    if ("exit".equalsIgnoreCase(line.trim())) {
                        out.println("Tchau!");
                        break;
                    }
                    // Simples “echo” com transformação
                    String resposta = "ECHO: " + line.toUpperCase();
                    out.println(resposta);
                    System.out.println("Por " + socket.getRemoteSocketAddress() + " : " + line);
                }
            } catch (IOException e) {
                System.out.println("Conexão encerrada: " + e.getMessage());
            } finally {
                try { socket.close(); } catch (IOException ignored) {}
            }
        }
    }
}
