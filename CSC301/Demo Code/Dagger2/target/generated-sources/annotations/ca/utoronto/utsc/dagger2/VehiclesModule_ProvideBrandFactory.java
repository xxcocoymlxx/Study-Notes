package ca.utoronto.utsc.dagger2;

import dagger.internal.Factory;
import dagger.internal.Preconditions;
import javax.annotation.Generated;

@Generated(
  value = "dagger.internal.codegen.ComponentProcessor",
  comments = "https://google.github.io/dagger"
)
public final class VehiclesModule_ProvideBrandFactory implements Factory<Brand> {
  private final VehiclesModule module;

  public VehiclesModule_ProvideBrandFactory(VehiclesModule module) {
    this.module = module;
  }

  @Override
  public Brand get() {
    return provideInstance(module);
  }

  public static Brand provideInstance(VehiclesModule module) {
    return proxyProvideBrand(module);
  }

  public static VehiclesModule_ProvideBrandFactory create(VehiclesModule module) {
    return new VehiclesModule_ProvideBrandFactory(module);
  }

  public static Brand proxyProvideBrand(VehiclesModule instance) {
    return Preconditions.checkNotNull(
        instance.provideBrand(), "Cannot return null from a non-@Nullable @Provides method");
  }
}
