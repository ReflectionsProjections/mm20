package edu.acm.uiuc.mm20.objects.send.actions;

import edu.acm.uiuc.mm20.objects.send.Action;

public class Code extends Action {
	public String type;
	
	public Code(long person_id, String type) {
		super("code", person_id);
		this.type = type;
	}
}
