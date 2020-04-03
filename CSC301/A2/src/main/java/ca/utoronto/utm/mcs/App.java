package ca.utoronto.utm.mcs;

import java.io.IOException;
import java.net.InetSocketAddress;

import com.mongodb.client.MongoClient;
import com.sun.net.httpserver.HttpServer;
import java.net.URI;
import java.net.URISyntaxException;


import javax.inject.Inject;


public class App
{
    static int port = 8080;

    public static void main(String[] args) throws IOException
    {
    	Dagger service = DaggerDaggerComponent.create().buildMongoHttp();
    	
    	MongoClient db = service.getDb();
    	    	
    	//Create your server context here
    	service.getServer().createContext("/api/v1/post", new Endpoint(db));
    	
    	service.getServer().start();
    	System.out.printf("Server started on port %d", port);
    }
}
