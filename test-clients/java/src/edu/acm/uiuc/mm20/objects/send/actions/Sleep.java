package edu.acm.uiuc.mm20.objects.send.actions;

import edu.acm.uiuc.mm20.objects.send.Action;

public class Sleep extends Action{
	public Sleep(long person_id) {
		super("sleep", person_id);
	}
}
