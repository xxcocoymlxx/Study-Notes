package ca.utoronto.utsc.dagger2;

import javax.inject.Inject;

public class Car {
	 
    private Engine engine;
    private Brand brand;
 
    @Inject
    public Car(Engine engine, Brand brand) {
        this.engine = engine;
        this.brand = brand;
    }
    
    public Brand getBrand() {
    	return this.brand;
    }
 
    // getters and setters
 
}
