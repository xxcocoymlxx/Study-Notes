package ca.utoronto.utm.mcs;

import com.sun.net.httpserver.HttpServer;
import dagger.internal.Factory;
import dagger.internal.Preconditions;
import javax.annotation.Generated;

@Generated(
  value = "dagger.internal.codegen.ComponentProcessor",
  comments = "https://google.github.io/dagger"
)
public final class DaggerModule_ProvideHttpServerFactory implements Factory<HttpServer> {
  private final DaggerModule module;

  public DaggerModule_ProvideHttpServerFactory(DaggerModule module) {
    this.module = module;
  }

  @Override
  public HttpServer get() {
    return provideInstance(module);
  }

  public static HttpServer provideInstance(DaggerModule module) {
    return proxyProvideHttpServer(module);
  }

  public static DaggerModule_ProvideHttpServerFactory create(DaggerModule module) {
    return new DaggerModule_ProvideHttpServerFactory(module);
  }

  public static HttpServer proxyProvideHttpServer(DaggerModule instance) {
    return Preconditions.checkNotNull(
        instance.provideHttpServer(), "Cannot return null from a non-@Nullable @Provides method");
  }
}
