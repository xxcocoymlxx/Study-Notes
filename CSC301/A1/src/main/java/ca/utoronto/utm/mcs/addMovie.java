package ca.utoronto.utm.mcs;
import java.io.IOException;
import java.io.OutputStream;
import java.nio.ByteBuffer;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;

import org.json.JSONException;
import org.json.JSONObject;
import org.neo4j.driver.v1.*;
import static org.neo4j.driver.v1.Values.parameters;

public class addMovie implements HttpHandler
{
	private static Driver dri;

    public addMovie(Driver d) {
        dri = d;
    }

    public void handle(HttpExchange r) {
        try {
        	handlePut(r);
        } catch (Exception e) {
        	e.printStackTrace();  
        }
    }

    public void handlePut(HttpExchange r) throws IOException, JSONException{
    	try (Session session = dri.session()){
        String body = Utils.convert(r.getRequestBody());
        //raises JSONException if String passed to make JSONObject invalid
        try {
        	JSONObject deserialized = new JSONObject(body);
        
        if (deserialized.has("movieId") && deserialized.has("name")) {
        	String mid = deserialized.getString("movieId");
        	String name = deserialized.getString("name");
        	
        	Map<String, Object> parameters = new HashMap<String, Object>();
        	parameters.put("name", name);
        	parameters.put("mid", mid);
        	
        	StatementResult match = session.run("MATCH (m:movie) WHERE m.id = $mid RETURN m.Name AS name", parameters("mid", mid));
        	if (match.hasNext()) {
        		r.sendResponseHeaders(400, -1);
        	}
        	else {
        		StatementResult result = session.run("CREATE (m:movie {id: $mid, Name: $name})",parameters);
        		 r.sendResponseHeaders(200, -1);
        	}
        }
        else{
        	r.sendResponseHeaders(400, -1);
        }
        }catch(JSONException j) {
        	r.sendResponseHeaders(400, -1);
        	}
    	}
    	catch(Exception e) {
    		r.sendResponseHeaders(500, -1);//INTERNAL SERVER ERROR
    	}
    }
}
