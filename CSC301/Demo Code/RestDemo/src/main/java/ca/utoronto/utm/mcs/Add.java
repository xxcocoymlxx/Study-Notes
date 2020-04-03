package ca.utoronto.utm.mcs;

import java.io.IOException;
import java.io.OutputStream;

import org.json.*;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;

public class Add implements HttpHandler
{
    private static Memory memory;

    public Add(Memory mem) {
        memory = mem;
    }

    //the class HttpExchange:
    //This class encapsulates a HTTP request received and a response 
    //to be generated in one exchange. It provides methods for examining 
    //the request from the client, and for building and sending the response.
    public void handle(HttpExchange r) {
        try {
        	//use getRequestMethod() to determine the command
            if (r.getRequestMethod().equals("GET")) {
            	//pass the HttpExchange object to handleGet() to do further processing
                handleGet(r);
            } else if (r.getRequestMethod().equals("POST")) {
                handlePost(r);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void handleGet(HttpExchange r) throws IOException, JSONException {
    	//getRequestBody() returns a InputStream for reading the request body. 
    	//After reading the request body, the stream is close.
        String body = Utils.convert(r.getRequestBody());//converts InputStream to String
        
        //把request body转化成JSON
        JSONObject deserialized = new JSONObject(body);

        long first = memory.getValue();
        long second = memory.getValue();

        //从JSON里面得到first 和 second number
        if (deserialized.has("firstNumber"))
            first = deserialized.getLong("firstNumber");

        if (deserialized.has("secondNumber"))
            second = deserialized.getLong("secondNumber");

        /* TODO: Implement the math logic */
        long answer = first + second;
        
        System.out.println(first+","+second+","+answer);
        
        //把answer转化成String
        String response = Long.toString(answer) + "\n";
        
        //sendResponseHeaders()
        //Starts sending the response back to the client using the current set of 
        //response headers and the numeric response code as specified in this method.
        //sendResponseHeaders(int rCode, long responseLength)
        r.sendResponseHeaders(200, response.length());
        
        //getResponseBody()
        //returns a stream to which the response body must be written.
        //我们不是得到一个有内容的response body，我们是得到了一个装response body的容器
        //我们要往里面写东西，把我们的response写进去
        //which means we're gonna write the response to this stream
        //sendResponseHeaders(int,long)) must be called prior to calling this method.
        OutputStream os = r.getResponseBody();
        os.write(response.getBytes());//write whatever bytes the response has
        os.close();//关掉这个stream
    }

    public void handlePost(HttpExchange r) throws IOException, JSONException{
        /* TODO: Implement this.
           Hint: This is very very similar to the get just make sure to save
                 your result in memory instead of returning a value.*/
    	
    	//converts InputStream to String
        String body = Utils.convert(r.getRequestBody());
        
      //把request body转化成JSON
        JSONObject deserialized = new JSONObject(body);

        long first = memory.getValue();
        long second = memory.getValue();

        if (deserialized.has("firstNumber"))
            first = deserialized.getLong("firstNumber");

        if (deserialized.has("secondNumber"))
            second = deserialized.getLong("secondNumber");

        /* TODO: Implement the math logic */
        long answer = first + second;
        
        memory.setValue(answer);
        System.out.println(memory.getValue());

        //sendResponseHeaders()	
        //Starts sending the response back to the client using the current set of 
        //response headers and the numeric response code as specified in this method.
        //sendResponseHeaders(int rCode, long responseLength)
        r.sendResponseHeaders(200, -1);
    }
}
