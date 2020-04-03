package ca.utoronto.utm.mcs;

import com.mongodb.client.MongoClient;
import com.sun.net.httpserver.HttpServer;
import dagger.internal.Factory;
import javax.annotation.Generated;
import javax.inject.Provider;

@Generated(
  value = "dagger.internal.codegen.ComponentProcessor",
  comments = "https://google.github.io/dagger"
)
public final class Dagger_Factory implements Factory<Dagger> {
  private final Provider<HttpServer> serverProvider;

  private final Provider<MongoClient> dbProvider;

  public Dagger_Factory(Provider<HttpServer> serverProvider, Provider<MongoClient> dbProvider) {
    this.serverProvider = serverProvider;
    this.dbProvider = dbProvider;
  }

  @Override
  public Dagger get() {
    return provideInstance(serverProvider, dbProvider);
  }

  public static Dagger provideInstance(
      Provider<HttpServer> serverProvider, Provider<MongoClient> dbProvider) {
    return new Dagger(serverProvider.get(), dbProvider.get());
  }

  public static Dagger_Factory create(
      Provider<HttpServer> serverProvider, Provider<MongoClient> dbProvider) {
    return new Dagger_Factory(serverProvider, dbProvider);
  }

  public static Dagger newDagger(HttpServer server, MongoClient db) {
    return new Dagger(server, db);
  }
}
