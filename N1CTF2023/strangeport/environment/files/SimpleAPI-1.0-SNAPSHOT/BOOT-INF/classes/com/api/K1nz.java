package api;

import com.google.gson.Gson;
import java.nio.charset.StandardCharsets;
import java.util.Base64;

public class K1nz {

    public static void main(String[] args) throws ClassNotFoundException {
        Gson gson = new Gson();
        Class<?> personClass = Class.forName("api.Person");
        Person persons = (Person) gson.fromJson(new String(Base64.getDecoder().decode("eyJuYW1lIjoidXNlciIsImFnZSI6IjIwIn0="), StandardCharsets.UTF_8), personClass);
        System.out.println(persons);

    }
}
