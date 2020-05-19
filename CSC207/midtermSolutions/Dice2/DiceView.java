package ca.utoronto.utm.dice2;
import java.util.Observable;
import java.util.Observer;
import javax.swing.JTextField;

public class DiceView implements Observer {
	private JTextField tfDie1;
	private JTextField tfDie2;
	public DiceView(JTextField tfDie1, JTextField tfDie2) {
		this.tfDie1=tfDie1;
		this.tfDie2=tfDie2;
	}
	@Override
	public void update(Observable o, Object arg) {
		DiceModel dice = (DiceModel)o;
		tfDie1.setText(""+dice.getDiceValue1());
		tfDie2.setText(""+dice.getDiceValue2());
	}
}
