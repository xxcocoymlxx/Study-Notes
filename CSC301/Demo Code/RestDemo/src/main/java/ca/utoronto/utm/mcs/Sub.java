package ca.utoronto.utm.mcs;

import java.io.IOException;
import java.io.OutputStream;

import org.json.*;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;


public class Sub implements HttpHandler
{
    private static Memory memory;

    public Sub(Memory mem) {
        memory = mem;
    }

    public void handle(HttpExchange r) {
        try {
            if (r.getRequestMethod().equals("GET")) {
                handleGet(r);
            } else if (r.getRequestMethod().equals("POST")) {
                handlePost(r);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void handleGet(HttpExchange r) throws IOException, JSONException {
        String body = Utils.convert(r.getRequestBody());
        JSONObject deserialized = new JSONObject(body);

        long first = memory.getValue();
        long second = memory.getValue();

        if (deserialized.has("firstNumber"))
            first = deserialized.getLong("firstNumber");

        if (deserialized.has("secondNumber"))
            second = deserialized.getLong("secondNumber");

        /* TODO: Implement the math logic */
        long answer = first - second;

        String response = Long.toString(answer) + "\n";
        r.sendResponseHeaders(200, response.length());
        OutputStream os = r.getResponseBody();
        os.write(response.getBytes());
        os.close();
    }

    public void handlePost(HttpExchange r) throws IOException, JSONException{
        /* TODO: Implement this.
           Hint: This is very very similar to the get just make sure to save
                 your result in memory instead of returning a value.*/
        String body = Utils.convert(r.getRequestBody());
        JSONObject deserialized = new JSONObject(body);

        long first = memory.getValue();
        long second = memory.getValue();

        if (deserialized.has("firstNumber"))
            first = deserialized.getLong("firstNumber");

        if (deserialized.has("secondNumber"))
            second = deserialized.getLong("secondNumber");

        /* TODO: Implement the math logic */
        long answer = first - second;
        memory.setValue(answer);

        r.sendResponseHeaders(200, -1);
    }
}
