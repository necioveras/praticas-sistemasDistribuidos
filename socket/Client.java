import java.io.BufferedReader;
import java.io.ByteArrayInputStream;
import java.io.InputStreamReader;
import java.net.URI;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.KeyStore;
import java.security.cert.Certificate;
import java.security.cert.CertificateFactory;
import java.util.Base64;
import java.util.List;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.TimeUnit;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import javax.net.SocketFactory;
import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLSocketFactory;
import javax.net.ssl.TrustManagerFactory;

import org.java_websocket.client.WebSocketClient;
import org.java_websocket.handshake.ServerHandshake;

public final class Client extends WebSocketClient {
    private final BlockingQueue<String> messages = new LinkedBlockingQueue<>();

    private Client(URI serverUri) {
        super(serverUri);
    }

    @Override
    public void onOpen(ServerHandshake handshake) {
        // A saudação chega como uma mensagem WebSocket separada.
    }

    @Override
    public void onMessage(String message) {
        messages.offer(message);
    }

    @Override
    public void onClose(int code, String reason, boolean remote) {
        // O encerramento é tratado pelo laço de entrada do cliente.
    }

    @Override
    public void onError(Exception exception) {
        System.err.println("Erro WebSocket: " + exception.getMessage());
    }

    public static void main(String[] args) throws Exception {
        String endpoint = args.length > 0 ? args[0] : "ws://127.0.0.1:5000/ws";
        URI serverUri = URI.create(endpoint);
        String scheme = serverUri.getScheme();
        if (!"ws".equalsIgnoreCase(scheme) && !"wss".equalsIgnoreCase(scheme)) {
            throw new IllegalArgumentException("Use uma URL ws:// ou wss://");
        }

        Client client = new Client(serverUri);
        if ("wss".equalsIgnoreCase(scheme)) {
            client.setSocketFactory(systemTrustSocketFactory());
        }
        try {
            if (!client.connectBlocking()) {
                throw new IllegalStateException("Não foi possível conectar ao servidor WebSocket.");
            }

            String greeting = client.messages.poll(10, TimeUnit.SECONDS);
            if (greeting == null) {
                throw new IllegalStateException("O servidor não enviou a saudação.");
            }
            System.out.println(greeting);

            BufferedReader console = new BufferedReader(new InputStreamReader(System.in));
            String input;
            System.out.print("> ");
            while ((input = console.readLine()) != null) {
                client.send(input);
                String response = client.messages.poll(10, TimeUnit.SECONDS);
                if (response == null) {
                    System.out.println("(Sem resposta do servidor)");
                    break;
                }
                System.out.println(response);
                if ("exit".equalsIgnoreCase(input.trim())) {
                    break;
                }
                System.out.print("> ");
            }
        } finally {
            if (client.isOpen()) {
                client.closeBlocking();
            }
        }
    }

    private static SocketFactory systemTrustSocketFactory() throws Exception {
        String configuredBundle = System.getenv("SSL_CERT_FILE");
        List<Path> candidates = configuredBundle == null || configuredBundle.isBlank()
            ? List.of(
                Path.of("/etc/ssl/certs/ca-certificates.crt"),
                Path.of("/etc/pki/tls/certs/ca-bundle.crt")
            )
            : List.of(Path.of(configuredBundle));

        Path caBundle = candidates.stream()
            .filter(Files::isRegularFile)
            .findFirst()
            .orElse(null);
        if (caBundle == null) {
            return SSLSocketFactory.getDefault();
        }

        KeyStore trustStore = KeyStore.getInstance(KeyStore.getDefaultType());
        trustStore.load(null, null);
        CertificateFactory certificateFactory = CertificateFactory.getInstance("X.509");
        String pemBundle = Files.readString(caBundle, StandardCharsets.ISO_8859_1);
        Matcher certificateBlocks = Pattern.compile(
            "-----BEGIN CERTIFICATE-----\\s*(.*?)\\s*-----END CERTIFICATE-----",
            Pattern.DOTALL
        ).matcher(pemBundle);
        int index = 0;
        while (certificateBlocks.find()) {
            byte[] encodedCertificate = Base64.getMimeDecoder().decode(certificateBlocks.group(1));
            Certificate certificate = certificateFactory.generateCertificate(
                new ByteArrayInputStream(encodedCertificate)
            );
            trustStore.setCertificateEntry("system-ca-" + index++, certificate);
        }
        if (index == 0) {
            throw new IllegalStateException("O arquivo de autoridades certificadoras está vazio: " + caBundle);
        }

        TrustManagerFactory trustManagers = TrustManagerFactory.getInstance(
            TrustManagerFactory.getDefaultAlgorithm()
        );
        trustManagers.init(trustStore);
        SSLContext sslContext = SSLContext.getInstance("TLS");
        sslContext.init(null, trustManagers.getTrustManagers(), null);
        return sslContext.getSocketFactory();
    }
}
