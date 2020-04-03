package ca.utoronto.utsc.dagger2;

import javax.inject.Singleton;

import dagger.Component;

/**
 * 
 * @author CYANG
 *
 * a component, which is an interface used to generate the injector
 * 
 * They are a way of telling Dagger what dependencies should
 * be bundled together and made available to a given instance
 * so they can be used.
 * 
 * They provide a way for a class to request dependencies
 * being injected through their @Inject annotation.
 * 
 * This is the class that will generate Car instances, injecting
 * dependencies provided by VehiclesModule.
 *
 * Simply put, we need a method signature that returns a Car and
 * we need to mark the class with the @Component annotation.
 *
 * Notice how we pass our module class as an argument to the
 * @Component annotation. If we didn’t do that, Dagger wouldn’t
 * know how to build the car’s dependencies.
 */


@Singleton
@Component(modules = VehiclesModule.class)
public interface VehiclesComponent {

	public Car buildCar();

}
