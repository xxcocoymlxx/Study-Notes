package ca.utoronto.utsc.dagger2;

public class UseCars {

	public static void main(String[] args) {
		//initialize the injector
		VehiclesComponent component = DaggerVehiclesComponent.create();
		 
		//perform the injection by calling buildCar()
		//buildCar() knows that it needs to return a Car object
	    Car carOne = component.buildCar();
	    Car carTwo = component.buildCar();
	    
	    System.out.println(carOne.getBrand().getName());
	    System.out.println(carTwo.getBrand().getName());
	}
	
	
}
