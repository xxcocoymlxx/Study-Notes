package ca.utoronto.utm.dice2;
import java.awt.FlowLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JTextField;

public class DiceController implements ActionListener {
	private DiceModel dice;
	
	public static void main(String [] args){
		DiceModel dice = new DiceModel();
		
		JFrame frame = new JFrame("Dice"); 
		JButton roll = new JButton("roll");
		JTextField tfDie1 = new JTextField(3);
		JTextField tfDie2 = new JTextField(3);
		
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.getContentPane().setLayout(new FlowLayout());
		frame.getContentPane().add(roll);
		frame.getContentPane().add(tfDie1);
		frame.getContentPane().add(tfDie2);
		
		DiceView view=new DiceView(tfDie1, tfDie2); 
		roll.addActionListener(new DiceController(dice));
		dice.addObserver(view);
		
		frame.pack();
		frame.setVisible(true);
		
	}
	public DiceController(DiceModel dice) {
		this.dice=dice;		
	}
	@Override
	public void actionPerformed(ActionEvent e) {
		this.dice.roll();
	}
}
