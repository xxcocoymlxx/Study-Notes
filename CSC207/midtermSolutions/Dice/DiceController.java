package ca.utoronto.utm.dice;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class DiceController implements ActionListener {
	private DiceModel dice;
	public DiceController(DiceModel dice) {
		this.dice=dice;
	}
	@Override
	public void actionPerformed(ActionEvent e) {
		this.dice.roll();
	}
}
