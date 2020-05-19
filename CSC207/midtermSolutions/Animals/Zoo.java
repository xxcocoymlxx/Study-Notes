package ca.utoronto.utm.animal;

public class Zoo {
	public static void main(String [] args){
		Animal a=new Animal("a", 1);
		LandAnimal l=new LandAnimal("b", 2);
		WaterAnimal w=new WaterAnimal("c", 3);
		FlyingSquirrel f=new FlyingSquirrel("d", 4);
		
		System.out.println(a);
		System.out.println(l);
		l.walk();
		System.out.println(w);
		w.swim();
		System.out.println(f);
		f.walk();
		f.fly();
	}
}
