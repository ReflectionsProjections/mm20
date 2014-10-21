package edu.acm.uiuc.mm20.objects.send;

public abstract class Action {
	public String action;
	public long person_id;
	
	public Action(String action, long person_id) {
		this.action = action;
		this.person_id = person_id;
	}
}
