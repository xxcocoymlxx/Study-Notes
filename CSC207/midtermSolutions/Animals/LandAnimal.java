package ca.utoronto.utm.animal;

public class LandAnimal extends Animal {
	
	public LandAnimal(String name, int age){
		super(name,age);
	}
	
	public void walk(){
		System.out.println(this.getName()+" is walking");
	}
	
	public String toString(){
		return super.toString()+", and a land animal";//必考点
	}
}
