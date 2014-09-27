package edu.acm.uiuc.mm20.objects.send;

import java.util.List;

public class ConnectionData {
	public ConnectionData(String team_name, List<NewPerson> people) {
		super();
		this.team = team_name;
		this.members = people;
	}

	String team;
	List<NewPerson> members;
}
