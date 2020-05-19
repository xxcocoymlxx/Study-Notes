package ca.utoronto.utm.dice;
import java.awt.FlowLayout;
import java.awt.event.ActionListener;
import java.util.Observable;
import java.util.Observer;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JTextField;

public class DiceView implements Observer {
	private JButton roll = new JButton("roll");
	private JTextField tfDie1 = new JTextField(3);
	private JTextField tfDie2 = new JTextField(3);
	public DiceView(ActionListener controller) {
		JFrame frame = new JFrame("Dice"); 
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.getContentPane().setLayout(new FlowLayout());
		frame.getContentPane().add(roll);
		frame.getContentPane().add(tfDie1);
		frame.getContentPane().add(tfDie2);
		roll.addActionListener(controller);
		frame.pack();
		frame.setVisible(true);
	}
	@Override
	public void update(Observable o, Object arg) {
		DiceModel dice = (DiceModel)o;
		tfDie1.setText(""+dice.getDiceValue1());
		tfDie2.setText(""+dice.getDiceValue2());
	}
}
