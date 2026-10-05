import java.net.InetSocketAddress;
import java.util.Locale;
import java.util.concurrent.CountDownLatch;

import org.java_websocket.WebSocket;
import org.java_websocket.handshake.ClientHandshake;
import org.java_websocket.server.WebSocketServer;

public final class Server extends WebSocketServer {
    private static final String BIND_ADDRESS = "0.0.0.0";
    private static final int PORT = 5000;
    private static final String PATH = "/ws";

    private Server() {
        super(new InetSocketAddress(BIND_ADDRESS, PORT));
        setReuseAddr(true);
    }

    @Override
    public void onOpen(WebSocket connection, ClientHandshake handshake) {
        if (!PATH.equals(handshake.getResourceDescriptor())) {
            connection.close(1008, "Use o endpoint /ws");
            return;
        }
        System.out.println("Cliente WebSocket conectado: " + connection.getRemoteSocketAddress());
        connection.send("Bem-vindo! Envie uma mensagem (ou 'exit' para sair).");
    }

    @Override
    public void onMessage(WebSocket connection, String message) {
        if ("exit".equalsIgnoreCase(message.trim())) {
            connection.send("Tchau!");
            connection.close(1000, "Cliente encerrou a sessão");
            return;
        }
        connection.send("ECHO: " + message.toUpperCase(Locale.ROOT));
        System.out.println("Mensagem recebida: " + message);
    }

    @Override
    public void onClose(WebSocket connection, int code, String reason, boolean remote) {
        System.out.println("Cliente desconectado: " + connection.getRemoteSocketAddress());
    }

    @Override
    public void onError(WebSocket connection, Exception exception) {
        System.err.println("Erro WebSocket: " + exception.getMessage());
    }

    @Override
    public void onStart() {
        System.out.println("Servidor WebSocket pronto em ws://0.0.0.0:" + PORT + PATH);
    }

    public static void main(String[] args) throws InterruptedException {
        new Server().start();
        new CountDownLatch(1).await();
    }
}
