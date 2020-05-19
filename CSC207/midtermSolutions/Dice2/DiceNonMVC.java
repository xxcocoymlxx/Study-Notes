package ca.utoronto.utm.dice2;
import java.awt.FlowLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Random;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JTextField;

public class DiceNonMVC implements ActionListener {
	public static void main(String[] args) {
		javax.swing.SwingUtilities.invokeLater(new Runnable() {
			public void run() {
				new DiceNonMVC();
			}
		});
	}

	private Random randomSource=new Random();
	private JButton roll = new JButton("roll");
	private JTextField tfDie1 = new JTextField(3);
	private JTextField tfDie2 = new JTextField(3);
	public DiceNonMVC() {
		JFrame frame = new JFrame("Dice"); 
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.getContentPane().setLayout(new FlowLayout());
		JButton roll = new JButton("roll");
		frame.getContentPane().add(roll);
		frame.getContentPane().add(tfDie1);
		frame.getContentPane().add(tfDie2);
		roll.addActionListener(this);
		frame.pack();
		frame.setVisible(true);
	}
	@Override
	public void actionPerformed(ActionEvent e) {
		int die1=randomSource.nextInt(6)+1; // 0..5->1..6
		int die2=randomSource.nextInt(6)+1; // 0..5->1..6
		tfDie1.setText(""+die1);
		tfDie2.setText(""+die2);
	}
}
