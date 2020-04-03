package ca.utoronto.utm.mcs;
import java.io.IOException;
import java.io.OutputStream;
import java.nio.ByteBuffer;
import java.util.ArrayList;
import java.util.List;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;

import org.json.JSONException;
import org.json.JSONObject;
import org.neo4j.driver.v1.*;
import static org.neo4j.driver.v1.Values.parameters;

public class getMovie implements HttpHandler{
	private static Driver driver;
	
	public getMovie(Driver dri) {
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
    
    public void handleGet(HttpExchange r) throws IOException, JSONException{

        String body = Utils.convert(r.getRequestBody());//converts InputStream to String  
        String mid = null;
        try {
        	JSONObject deserialized = new JSONObject(body);

      //  get movie id from JSON
        if (deserialized.has("movieId")) {
            mid = deserialized.getString("movieId");
        } else {
        	r.sendResponseHeaders(400, -1);//BAD REQUEST
        }

        JSONObject response_body = new JSONObject();
        
        try (Session session = driver.session())
        {              	
        	StatementResult result = session.run(
                    "MATCH (m:movie) WHERE m.id= $mid RETURN m.Name AS name",
                    parameters("mid", mid));
        	
         //    Each Cypher execution returns a stream of records.
            if (result.hasNext())
            {
                Record record = result.next();
                String mName = record.get("name").asString();
                
                response_body.put("movieId", mid);
                response_body.put("name", mName);
            } else {
            //	either no such movie or the mid is wrong
            	r.sendResponseHeaders(404, -1);//NOT FOUND
            }
//------------------------------------------------------------------------------------------------      
          //  get list of actors' id
            StatementResult ActorResult = session.run(
                "MATCH (m:movie { id: $mid })<-[:ACTED_IN]-(actor) RETURN actor.id",
                parameters("mid", mid));
        
            List<String> actors = new ArrayList<>();

            while (ActorResult.hasNext())
            {
            	Record record = ActorResult.next();
            	String actorID = record.get("actor.id").asString();
            	actors.add(actorID);
            }
           
         //   add to json
            response_body.put("actors", actors);
        

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


