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


//TO DO: return proper error code
//1. when an actor does not exist in the database
//2. when an actor exists in the database but does not have relationship with Kevin Bacon 


public class computeBaconNumber implements HttpHandler{
	private static Driver driver;
	
	public computeBaconNumber(Driver dri) {
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
        String aid = null;
        try {
        	JSONObject deserialized = new JSONObject(body);
      
      //get actor id from JSON
        if (deserialized.has("actorId")) {
            aid = deserialized.getString("actorId");
        } else {
        	r.sendResponseHeaders(400, -1);//BAD REQUEST
        }
        
        JSONObject response_body = new JSONObject();    

        try (Session session = driver.session()){
        	//if aid corresponds to actor in database
            StatementResult validActor = session.run("MATCH (a:actor) WHERE a.id = $aid return a", parameters("aid", aid));
        	if (validActor.hasNext()){
        		
        	//if the actor is Kevin Bacon, return baconNum: 0
        	if (aid.equals("nm0000102")) {
                response_body.put("baconNumber", "0");
                	
            //if the actor is NOT Kevin Bacon
             } else {
        		StatementResult result = session.run(
        				"MATCH (a1:actor { id : 'nm0000102' }),(a2:actor { id: $aid }), path = shortestPath((a1)-[*]-(a2)) RETURN (LENGTH (path) / 2) AS num",
        				parameters("aid",aid));

        		// Each Cypher execution returns a stream of records.
        		if (result.hasNext())
        		{

        			Record record = result.next();
        			String baconNum = record.get("num").toString();
        			
        			//System.out.println("bacon number is:");
        			//System.out.println(baconNum);

        			//add to json
        			response_body.put("baconNumber", baconNum);

        		} else {
        			//either no such movie or the mid is wrong
        			response_body.put("baconNumber", "undefined");
        		}
             }

        		r.sendResponseHeaders(200, response_body.toString().length());

        		OutputStream os = r.getResponseBody();
        		os.write(response_body.toString().getBytes());
        		os.close();
        	
        	}else {
        		r.sendResponseHeaders(400, -1);
        	}
        	
        } catch (Exception e) {
        		r.sendResponseHeaders(500, -1);//INTERNAL SERVER ERROR
        }   
        }catch(JSONException j) {
        	r.sendResponseHeaders(400, -1);
        }
    }
}

