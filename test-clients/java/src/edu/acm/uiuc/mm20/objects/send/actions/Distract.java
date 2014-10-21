package edu.acm.uiuc.mm20.objects.send.actions;

import edu.acm.uiuc.mm20.objects.send.Action;

public class Distract extends Action {
	public int victim;
	
	public Distract(long person_id, int victim) {
		super("distract", person_id);
		this.victim = victim;
	}
}
