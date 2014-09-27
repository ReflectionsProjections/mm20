package edu.acm.uiuc.mm20.objects.send.actions;

import edu.acm.uiuc.mm20.objects.send.Action;

public class WakeUp extends Action {
	public int victim;
	
	public WakeUp(long person_id, int victim) {
		super("wake", person_id);
		this.victim = victim;
	}
}
