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

public class getActor implements HttpHandler{
	private static Driver driver;
	
	public getActor(Driver dri) {
        driver = dri;
	}

    //the class HttpExchange:
    //This class encapsulates a HTTP request received and a response 
    //to be generated in one exchange. It provides methods for examining 
    //the request from the client, and for building and sending the response.
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
    	//getRequestBody() returns a InputStream for reading the request body. 
    	//After reading the request body, the stream is closed.
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
        
        try (Session session = driver.session())
        {              	
        	//A StatementResult object offers hasNext() and next() that you 
        	//need to use to get the results from your queries.
        	StatementResult result = session.run(
                    "MATCH (a:actor) WHERE a.id= $aid RETURN a.Name AS name",
                    parameters("aid", aid));
        	
            // Each Cypher execution returns a stream of records.
            if (result.hasNext())
            {
                Record record = result.next();
                String aName = record.get("name").asString();
                // Values can be extracted from a record by index or name.
                //System.out.println(aid);
                //System.out.println(aName);
                response_body.put("actorId", aid);
                response_body.put("name", aName);
            } else {
            	//either no such actor or the aid is wrong
            	r.sendResponseHeaders(404, -1);//NOT FOUND
            }
//------------------------------------------------------------------------------------------------      
            StatementResult MovieResult = session.run(
                "MATCH (a:actor {id: $aid})-[act]-(movie) RETURN movie.id",
                parameters("aid", aid));
        
            List<String> movies = new ArrayList<>();

            while (MovieResult.hasNext())
            {
            	Record record = MovieResult.next();
            	String movieID = record.get("movie.id").asString();
            	movies.add(movieID);
            }
           
            //add to json
            response_body.put("movies", movies);
        
        
        //sendResponseHeaders()
        //Starts sending the response back to the client using the current set of 
        //response headers and the numeric response code as specified in this method.
        //sendResponseHeaders(int rCode, long responseLength)
        r.sendResponseHeaders(200, response_body.toString().length());
        
        //getResponseBody()
        //returns a stream to which the response body must be written.
        //which means we're gonna write the response to this stream
        //sendResponseHeaders(int,long)) must be called prior to calling this method.
        OutputStream os = r.getResponseBody();
        os.write(response_body.toString().getBytes());//write whatever bytes the response has
        os.close();
        } catch (Exception e) {
        	r.sendResponseHeaders(500, -1);//INTERNAL SERVER ERROR
        }
    }catch(JSONException j) {
    	r.sendResponseHeaders(400, -1);
    }
    }
}
