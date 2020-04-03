package ca.utoronto.utsc.dagger2;

public class Brand {

	private String name;


	public Brand(String name) {
		this.name = name;
	}
	
	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

}