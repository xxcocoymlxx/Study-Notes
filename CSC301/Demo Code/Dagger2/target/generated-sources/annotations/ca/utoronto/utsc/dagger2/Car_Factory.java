package ca.utoronto.utsc.dagger2;

import dagger.internal.Factory;
import javax.annotation.Generated;
import javax.inject.Provider;

@Generated(
  value = "dagger.internal.codegen.ComponentProcessor",
  comments = "https://google.github.io/dagger"
)
public final class Car_Factory implements Factory<Car> {
  private final Provider<Engine> engineProvider;

  private final Provider<Brand> brandProvider;

  public Car_Factory(Provider<Engine> engineProvider, Provider<Brand> brandProvider) {
    this.engineProvider = engineProvider;
    this.brandProvider = brandProvider;
  }

  @Override
  public Car get() {
    return provideInstance(engineProvider, brandProvider);
  }

  public static Car provideInstance(
      Provider<Engine> engineProvider, Provider<Brand> brandProvider) {
    return new Car(engineProvider.get(), brandProvider.get());
  }

  public static Car_Factory create(Provider<Engine> engineProvider, Provider<Brand> brandProvider) {
    return new Car_Factory(engineProvider, brandProvider);
  }

  public static Car newCar(Engine engine, Brand brand) {
    return new Car(engine, brand);
  }
}
