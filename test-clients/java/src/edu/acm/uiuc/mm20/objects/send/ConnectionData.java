package edu.acm.uiuc.mm20.objects.send;

import java.util.List;

public class ConnectionData {
	public ConnectionData(String team_name, List<NewPerson> people) {
		super();
		this.team_name = team_name;
		this.people = people;
	}

	String team_name;
	List<NewPerson> people;
}
