package ca.utoronto.utm.mcs;

import dagger.internal.Preconditions;
import javax.annotation.Generated;

@Generated(
  value = "dagger.internal.codegen.ComponentProcessor",
  comments = "https://google.github.io/dagger"
)
public final class DaggerDaggerComponent implements DaggerComponent {
  private DaggerModule daggerModule;

  private DaggerDaggerComponent(Builder builder) {
    initialize(builder);
  }

  public static Builder builder() {
    return new Builder();
  }

  public static DaggerComponent create() {
    return new Builder().build();
  }

  @SuppressWarnings("unchecked")
  private void initialize(final Builder builder) {
    this.daggerModule = builder.daggerModule;
  }

  @Override
  public Dagger buildMongoHttp() {
    return new Dagger(
        DaggerModule_ProvideHttpServerFactory.proxyProvideHttpServer(daggerModule),
        DaggerModule_ProvideMongoClientFactory.proxyProvideMongoClient(daggerModule));
  }

  public static final class Builder {
    private DaggerModule daggerModule;

    private Builder() {}

    public DaggerComponent build() {
      if (daggerModule == null) {
        this.daggerModule = new DaggerModule();
      }
      return new DaggerDaggerComponent(this);
    }

    public Builder daggerModule(DaggerModule daggerModule) {
      this.daggerModule = Preconditions.checkNotNull(daggerModule);
      return this;
    }
  }
}
