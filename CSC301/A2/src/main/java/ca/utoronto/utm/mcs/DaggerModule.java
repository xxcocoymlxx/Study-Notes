package ca.utoronto.utm.mcs;

import java.io.IOException;
import java.net.InetSocketAddress;
import com.sun.net.httpserver.HttpServer;
import java.util.Arrays;

import dagger.Module;
import dagger.Provides;

import com.mongodb.MongoClientSettings;
import com.mongodb.ServerAddress;
import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;

//It's like VehiclesModule.java
//a module, which is a class that provides or builds the objects’ dependencies
//A Module class is annotated with the @Module annotation,
//indicating that it can make dependencies available to the container.
//Then, we need to add the @Provides annotation on methods that construct our dependencies

@Module
public class DaggerModule {

	private static HttpServer server;
	private static MongoClient db;
	static int PORT = 8080;
	
    @Provides 
    public MongoClient provideMongoClient() {
    	this.db = MongoClients.create();
    	return this.db;
    }

    @Provides 
    public HttpServer provideHttpServer() {
    	try {
    		
    		if (this.server == null)this.server = HttpServer.create(new InetSocketAddress("0.0.0.0", PORT), 0);
    		else return this.server;
    		
		} catch (IOException e) {

			e.printStackTrace();
		}
        return this.server;
    }
 
}
