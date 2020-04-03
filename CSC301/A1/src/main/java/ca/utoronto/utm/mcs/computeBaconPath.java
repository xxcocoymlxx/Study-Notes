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

public class computeBaconPath implements HttpHandler{
	private static Driver driver;
	
	public computeBaconPath(Driver dri) {
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
        
        try {
        	JSONObject deserialized = new JSONObject(body);
        
        
        String aid = null;
      
      //get actor id from JSON
        if (deserialized.has("actorId")) {
            aid = deserialized.getString("actorId");
            
        } else {
        	r.sendResponseHeaders(400, -1);//BAD REQUEST
        }
        
        //the response body is a JSON:
        //1. baconNumber : String
        //2. List of JSON, where each JSON consists of a actorId and movieId
        JSONObject response_body = new JSONObject();  

        try (Session session = driver.session()){
        	
        	//if aid corresponds to actor in database
        	StatementResult validActor = session.run("MATCH (a:actor) WHERE a.id = $aid return a", parameters("aid", aid));
         	if (validActor.hasNext()){
        	
        	List<JSONObject> path = new ArrayList<>();
        	
        	//if the actor is Kevin Bacon, return 0 as the baconNumber and 1 movie of his at random.
        	if (aid.equals("nm0000102")) {
        		
                StatementResult result = session.run(
        				"MATCH (a:actor {id: 'nm0000102'})-[act]-(movie) RETURN movie.id");
                	JSONObject baconJSON= new JSONObject();  
                
                
                //get the first movie Kevin Bacon acted in
                Record record = result.next();
                String movieID = record.get("movie.id").asString();
                
                baconJSON.put("actorId", "nm0000102");
                baconJSON.put("movieId", movieID);
                //String baconJSONstr = baconJSON.toString();//convert the JSON to a string
                
                //add bacon's JSON to list of path
                path.add(baconJSON);
                
                response_body.put("baconNumber", "0");
                response_body.put("baconPath", path);//list of strings of JSON is added to the response body
                
                	
            //if the actor is NOT Kevin Bacon
             } else {
            	 int baconCount = 0;
             
        		StatementResult result = session.run(
        				"MATCH (a1:actor { id : 'nm0000102' }),(a2:actor { id: $aid }), path = shortestPath((a1)-[*]-(a2)) UNWIND nodes (path) as n RETURN { id : n.id, name :n.Name} as node;",
        				parameters("aid",aid));
        		
        		//if no path was found
        		if (!(result.hasNext())){
        			response_body.put("baconNumber", "undefined");
        		}

        		// Each Cypher execution returns a stream of records.
        		String actorID = null;
        		String movieID = null;
        		while (result.hasNext()){
        			Record currRecord = result.next();
        			
        			//get id of an actor or movie node
        			actorID = currRecord.get("node").get("id").asString();
        			
        			//check if there's a movie next
        			if (result.hasNext()) {
        				currRecord = result.next();
        				movieID = currRecord.get("node").get("id").asString();
        			}
        			//addJSONObject to path
        			
    				path.add(new JSONObject().put("actorId", actorID).put("movieId", movieID));
    				
        			//add to json
        			baconCount++;
        			}
        		//if while loop above was entered, sets baconNumber as baconCount
        		if (baconCount != 0) {
        			response_body.put("baconNumber", baconCount-1);
        		}
        		response_body.put("baconPath", path);
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

