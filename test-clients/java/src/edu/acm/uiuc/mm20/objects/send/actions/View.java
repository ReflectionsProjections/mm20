package edu.acm.uiuc.mm20.objects.send.actions;

import edu.acm.uiuc.mm20.objects.send.Action;

public class View extends Action {
	public View(long person_id) {
		super("view", person_id);
	}
}
