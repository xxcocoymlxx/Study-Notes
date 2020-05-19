package ca.utoronto.utm.dice;

public class DiceApp {
	public static void main(String [] args){
		javax.swing.SwingUtilities.invokeLater(new Runnable() {
			public void run() {
				// Create the model, view and controller, and hook
				// them up
				DiceModel model=new DiceModel();
				DiceController controller = new DiceController(model);
				DiceView view=new DiceView(controller);
				model.addObserver(view);
			}
		});		
	}
}
