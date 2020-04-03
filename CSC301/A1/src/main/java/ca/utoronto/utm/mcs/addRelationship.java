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

public class addRelationship implements HttpHandler
{
	private static Driver dri;

    public addRelationship(Driver d) {
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
        try {
        	JSONObject deserialized = new JSONObject(body);
        
        
        //if user provides a movieId and actorId
        if (deserialized.has("movieId") && deserialized.has("actorId")) {
        	String mid = deserialized.getString("movieId");
        	String aid = deserialized.getString("actorId");
        	
        	Map<String, Object> parameters = new HashMap<String, Object>();
        	parameters.put("aid", aid);
        	parameters.put("mid", mid);
        	
        	//if movieId and actorId given by user exists
        	StatementResult validMovieAndId = session.run("MATCH (m:movie), (a:actor) WHERE m.id = $mid AND a.id = $aid RETURN (m)", parameters);
        	if (validMovieAndId.hasNext()) {
        		//if there's already a relationship for this
        		StatementResult match = session.run("MATCH (m:movie), (a:actor) WHERE m.id = $mid AND a.id = $aid AND EXISTS ((m)-[:ACTED_IN]-(a)) RETURN (m)",
                        parameters);
            	if (match.hasNext()) {
            		r.sendResponseHeaders(400, -1);
            	}
            	else {
            		StatementResult result = session.run("MATCH (a:actor),(m:movie) WHERE a.id = $aid AND m.id = $mid CREATE (a)-[r:ACTED_IN]->(m)", parameters);
            		r.sendResponseHeaders(200, -1);
            	}
        	}
        	else {
        		r.sendResponseHeaders(404, -1);
        	}
        	}
        else{
        	r.sendResponseHeaders(400, -1);
        }
        }catch(JSONException j) {
        	r.sendResponseHeaders(400, -1);
        }
        }catch(Exception e) {
    		r.sendResponseHeaders(500, -1);//INTERNAL SERVER ERROR
    	}
    }
}
