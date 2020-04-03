package ca.utoronto.utsc.dagger2;

import dagger.internal.Factory;
import dagger.internal.Preconditions;
import javax.annotation.Generated;

@Generated(
  value = "dagger.internal.codegen.ComponentProcessor",
  comments = "https://google.github.io/dagger"
)
public final class VehiclesModule_ProvideEngineFactory implements Factory<Engine> {
  private final VehiclesModule module;

  public VehiclesModule_ProvideEngineFactory(VehiclesModule module) {
    this.module = module;
  }

  @Override
  public Engine get() {
    return provideInstance(module);
  }

  public static Engine provideInstance(VehiclesModule module) {
    return proxyProvideEngine(module);
  }

  public static VehiclesModule_ProvideEngineFactory create(VehiclesModule module) {
    return new VehiclesModule_ProvideEngineFactory(module);
  }

  public static Engine proxyProvideEngine(VehiclesModule instance) {
    return Preconditions.checkNotNull(
        instance.provideEngine(), "Cannot return null from a non-@Nullable @Provides method");
  }
}
