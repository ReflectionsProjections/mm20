package edu.acm.uiuc.mm20;

import java.util.ArrayList;

import com.google.gson.JsonElement;
import edu.acm.uiuc.mm20.objects.send.Archetypes;
import edu.acm.uiuc.mm20.objects.send.ConnectionData;
import edu.acm.uiuc.mm20.objects.send.NewPerson;


public class MM20AI {
	
	public void receivedMessage(String message) {
		System.out.print(message);
		
	}

	public ConnectionData makeTeam() {
		ArrayList<NewPerson> team= new ArrayList<NewPerson>();
		team.add(new NewPerson("java_lover", Archetypes.Coder));
		return new ConnectionData("Cool Java", team);
	}

}
