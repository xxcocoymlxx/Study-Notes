package ca.utoronto.utm.animal;

public class FlyingSquirrel extends LandAnimal implements CanFly {
	
	public FlyingSquirrel(String name, int age){
		super(name,age);
	}
	
	@Override
	public void fly() {
		System.out.println(this.getName()+" is flying");
	}
}
