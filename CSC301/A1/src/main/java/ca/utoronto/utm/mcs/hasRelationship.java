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

public class hasRelationship implements HttpHandler{
	private static Driver driver;
	
	public hasRelationship(Driver dri) {
		driver = dri;
	}

    public void handle(HttpExchange r) {
        try {
            if (r.getRequestMethod().equals("GET")) {
            	handleGet(r);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    
    public void handleGet(HttpExchange r) throws IOException, JSONException {

        String body = Utils.convert(r.getRequestBody());//converts InputStream to String  
        String mid = null;
        String aid = null;
        try {
        	JSONObject deserialized = new JSONObject(body);

        //get movie id from JSON
        if (deserialized.has("movieId")) {
            mid = deserialized.getString("movieId");
        } else {
        	r.sendResponseHeaders(400, -1);//BAD REQUEST
        }
        
      //get actor id from JSON
        if (deserialized.has("actorId")) {
            aid = deserialized.getString("actorId");
        } else {
        	r.sendResponseHeaders(400, -1);//BAD REQUEST
        }

        JSONObject response_body = new JSONObject();
        
        try (Session session = driver.session())
        {   
        	//checking if an actor exists in database
        	StatementResult checkactor = session.run("MATCH (a:actor) WHERE a.id= $aid RETURN a.Name AS name", parameters("aid", aid));
        	if (!checkactor.hasNext()) {
        		r.sendResponseHeaders(404, -1);//NOT FOUND
        	}

        	//checking if an movie exists in database
        	StatementResult checkmovie = session.run("MATCH (m:movie) WHERE m.id = $mid RETURN m.Name AS name", parameters("mid", mid));
        	if (!checkmovie.hasNext()) {
        		r.sendResponseHeaders(404, -1);//NOT FOUND
        	}
        	
        	Map<String, Object> parameters = new HashMap<String, Object>();
        	parameters.put("mid", mid);
        	parameters.put("aid", aid);
        	
        	StatementResult result = session.run(
                    "MATCH (m:movie), (a:actor) WHERE m.id=$mid AND a.id=$aid RETURN EXISTS ((m)-[:ACTED_IN]-(a)) AS bool",
                    parameters);
        	
            // Each Cypher execution returns a stream of records.
            if (result.hasNext())

            {        	
                Record record = result.next();
                Boolean bool = record.get("bool").asBoolean();            
                
                //add to json
                response_body.put("movieId", mid);
                response_body.put("actorId", aid);
                response_body.put("hasRelationship", bool);
                
            } else {
            	//when there is no relationship between movie and actor
                response_body.put("movieId", mid);
                response_body.put("actorId", aid);
                response_body.put("hasRelationship", "false");
            }
           
        r.sendResponseHeaders(200, response_body.toString().length());
        
        OutputStream os = r.getResponseBody();
        os.write(response_body.toString().getBytes());
        os.close();
        
        } catch (Exception e) {
        	r.sendResponseHeaders(500, -1);//INTERNAL SERVER ERROR
        }
        }catch(JSONException j) {
        	r.sendResponseHeaders(400, -1);
        }
    }
}
