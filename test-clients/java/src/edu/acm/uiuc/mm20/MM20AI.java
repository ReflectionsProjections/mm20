package edu.acm.uiuc.mm20;

import java.util.ArrayList;

import com.google.gson.Gson;
import com.google.gson.JsonElement;

import edu.acm.uiuc.mm20.objects.send.Archetypes;
import edu.acm.uiuc.mm20.objects.send.ConnectionData;
import edu.acm.uiuc.mm20.objects.send.NewPerson;


public class MM20AI {
	Gson gson = new Gson();
	
	public void receivedMessage(String message) {
		System.out.print(message);
		
	}
	public String connect(){
		return gson.toJson(this.makeTeam());
	}
	
	public ConnectionData makeTeam() {
		ArrayList<NewPerson> team= new ArrayList<NewPerson>();
		team.add(new NewPerson("java_lover", Archetypes.Coder));
		return new ConnectionData("Cool Java", team);
	}

}
