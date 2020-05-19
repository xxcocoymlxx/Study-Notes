package ca.utoronto.utm.dice;

import java.util.Observable;
import java.util.Random;

public class DiceModel extends Observable {
	private Random randomSource=new Random();
	private int diceValue1;
	private int diceValue2;
	public DiceModel(){
		this.roll();
	}
	public void roll(){
		this.diceValue1=randomSource.nextInt(6)+1; // 0..5->1..6
		this.diceValue2=randomSource.nextInt(6)+1; // 0..5->1..6
		this.setChanged();
		this.notifyObservers();
	}
	public int getDiceValue1(){
		return this.diceValue1;
	}
	public int getDiceValue2(){
		return this.diceValue2;
	}
}
