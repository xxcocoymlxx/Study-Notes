package ca.utoronto.utm.animal;

public class WaterAnimal extends Animal {
	
	public WaterAnimal(String name, int age){
		super(name,age);
	}
	
	public void swim(){
		System.out.println(this.getName()+" is swimming");
	}
	
	public String toString(){
		return super.toString()+", and a I love to swim";
	}
}
