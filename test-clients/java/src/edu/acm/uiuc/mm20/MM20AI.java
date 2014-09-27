package edu.acm.uiuc.mm20;

import java.util.ArrayList;

import com.google.gson.Gson;
import edu.acm.uiuc.mm20.objects.receive.GameState;
import edu.acm.uiuc.mm20.objects.send.Action;
import edu.acm.uiuc.mm20.objects.send.Archetypes;
import edu.acm.uiuc.mm20.objects.send.ConnectionData;
import edu.acm.uiuc.mm20.objects.send.NewPerson;

public class MM20AI {
	Gson gson = new Gson();
	GameState gameState;

	public ArrayList<Action> processTurn(GameState gamestate) {
		this.gameState = gamestate;
		ArrayList<Action> actions = new ArrayList<Action>();
		// Begin Turn Logic
		// End Turn Logic
		return actions;
	}

	public ConnectionData makeTeam() {
		ArrayList<NewPerson> team = new ArrayList<NewPerson>();
		team.add(new NewPerson("java_lover", Archetypes.Coder));
		team.add(new NewPerson("java_maniac", Archetypes.Theorist));
		team.add(new NewPerson("java_fanataic", Archetypes.Architect));
		return new ConnectionData("Cool Java", team);
	}

	public void joinedGameMessage(String message,
			NetCommunicator netCommunicator) {
		// TODO make object to unpack values into
		// then check to make sure connection succeeded
		//if so make first move, if not throw an exception.
		boolean connectionSuccsefull = true;
		
		if (connectionSuccsefull){
			ArrayList<Action> actions = new ArrayList<Action>();
			// ToDo: add some actions to the arraylist
			netCommunicator.sendMessage(gson.toJson(actions));
		}
	}

}
