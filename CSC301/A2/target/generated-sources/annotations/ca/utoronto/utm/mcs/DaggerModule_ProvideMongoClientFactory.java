package ca.utoronto.utm.mcs;

import com.mongodb.client.MongoClient;
import dagger.internal.Factory;
import dagger.internal.Preconditions;
import javax.annotation.Generated;

@Generated(
  value = "dagger.internal.codegen.ComponentProcessor",
  comments = "https://google.github.io/dagger"
)
public final class DaggerModule_ProvideMongoClientFactory implements Factory<MongoClient> {
  private final DaggerModule module;

  public DaggerModule_ProvideMongoClientFactory(DaggerModule module) {
    this.module = module;
  }

  @Override
  public MongoClient get() {
    return provideInstance(module);
  }

  public static MongoClient provideInstance(DaggerModule module) {
    return proxyProvideMongoClient(module);
  }

  public static DaggerModule_ProvideMongoClientFactory create(DaggerModule module) {
    return new DaggerModule_ProvideMongoClientFactory(module);
  }

  public static MongoClient proxyProvideMongoClient(DaggerModule instance) {
    return Preconditions.checkNotNull(
        instance.provideMongoClient(), "Cannot return null from a non-@Nullable @Provides method");
  }
}
