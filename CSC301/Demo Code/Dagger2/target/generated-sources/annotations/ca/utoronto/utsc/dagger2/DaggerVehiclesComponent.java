package ca.utoronto.utsc.dagger2;

import dagger.internal.DoubleCheck;
import dagger.internal.Preconditions;
import javax.annotation.Generated;
import javax.inject.Provider;

@Generated(
  value = "dagger.internal.codegen.ComponentProcessor",
  comments = "https://google.github.io/dagger"
)
public final class DaggerVehiclesComponent implements VehiclesComponent {
  private VehiclesModule vehiclesModule;

  private Provider<Brand> provideBrandProvider;

  private DaggerVehiclesComponent(Builder builder) {
    initialize(builder);
  }

  public static Builder builder() {
    return new Builder();
  }

  public static VehiclesComponent create() {
    return new Builder().build();
  }

  @SuppressWarnings("unchecked")
  private void initialize(final Builder builder) {
    this.vehiclesModule = builder.vehiclesModule;
    this.provideBrandProvider =
        DoubleCheck.provider(VehiclesModule_ProvideBrandFactory.create(builder.vehiclesModule));
  }

  @Override
  public Car buildCar() {
    return new Car(
        VehiclesModule_ProvideEngineFactory.proxyProvideEngine(vehiclesModule),
        provideBrandProvider.get());
  }

  public static final class Builder {
    private VehiclesModule vehiclesModule;

    private Builder() {}

    public VehiclesComponent build() {
      if (vehiclesModule == null) {
        this.vehiclesModule = new VehiclesModule();
      }
      return new DaggerVehiclesComponent(this);
    }

    public Builder vehiclesModule(VehiclesModule vehiclesModule) {
      this.vehiclesModule = Preconditions.checkNotNull(vehiclesModule);
      return this;
    }
  }
}
