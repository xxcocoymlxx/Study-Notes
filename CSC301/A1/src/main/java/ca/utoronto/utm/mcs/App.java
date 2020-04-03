package ca.utoronto.utm.mcs;

import java.io.IOException;

import org.neo4j.driver.v1.*;
import java.net.InetSocketAddress;
import com.sun.net.httpserver.HttpServer;

public class App 
{
    static int PORT = 8080;
    
    
    public static void main(String[] args) throws IOException
    {
    	
        HttpServer server = HttpServer.create(new InetSocketAddress("0.0.0.0", PORT), 0);
        
        
        Driver driver = GraphDatabase.driver("bolt://localhost:7687", AuthTokens.basic("neo4j","1234"));
        
        server.createContext("/api/v1/addMovie", new addMovie(driver));
        server.createContext("/api/v1/addActor", new addActor(driver));
        server.createContext("/api/v1/addRelationship", new addRelationship(driver));
        
        server.createContext("/api/v1/getActor", new getActor(driver));
        server.createContext("/api/v1/getMovie", new getMovie(driver));
        server.createContext("/api/v1/hasRelationship", new hasRelationship(driver));
        
        server.createContext("/api/v1/computeBaconNumber", new computeBaconNumber(driver));        
        server.createContext("/api/v1/computeBaconPath", new computeBaconPath(driver));
        
        
        server.start();
        System.out.printf("Server started on port %d...\n", PORT);
    }
}
