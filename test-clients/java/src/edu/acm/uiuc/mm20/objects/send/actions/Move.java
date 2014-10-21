package edu.acm.uiuc.mm20.objects.send.actions;

import edu.acm.uiuc.mm20.objects.send.Action;

public class Move extends Action {
	public String room;
	
	public Move(long person_id, String room)
	{
		super("move", person_id);
		this.room = room;
	}
}
