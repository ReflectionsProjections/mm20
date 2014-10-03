package edu.acm.uiuc.mm20;

import java.util.ArrayList;
import java.util.Random;

import com.google.gson.Gson;

import edu.acm.uiuc.mm20.objects.receive.ConnectionValidation;
import edu.acm.uiuc.mm20.objects.receive.GameState;
import edu.acm.uiuc.mm20.objects.receive.Person;
import edu.acm.uiuc.mm20.objects.receive.Room;
import edu.acm.uiuc.mm20.objects.send.Action;
import edu.acm.uiuc.mm20.objects.send.Archetypes;
import edu.acm.uiuc.mm20.objects.send.ConnectionData;
import edu.acm.uiuc.mm20.objects.send.NewPerson;
import edu.acm.uiuc.mm20.objects.send.actions.Move;

public class MM20AI {
	Gson gson = new Gson();
	ArrayList<String> teamMembers = new ArrayList<String>();
	Random generator = new Random();

	public ArrayList<Action> processTurn(GameState gamestate) {
		//if the game has ended quit cleanly
		if (gamestate.getWinner() != null){
			if(gamestate.getWinner()){
				System.out.println("You win :)");
			}
			System.out.println("Game over");;
			return null;
		}
		ArrayList<Action> actions = new ArrayList<Action>();
		// Begin Turn Logic
		
		for (String personID : teamMembers) {
			Person person = gamestate.getPerson(personID);
			Room location = gamestate.getRoom(person.getLocation());
			int randomIndex = generator.nextInt(location.getConnectedRooms().size());
			String targetName = location.getConnectedRooms().get(randomIndex);
			Move move = new Move(person.getPersonId(), targetName);
			actions.add(move);
		}
		
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
	
	public ArrayList<Action> firstTurn(ConnectionValidation connection) {
		ArrayList<Action> actions = new ArrayList<Action>();
		for (Person person: connection.team.values())
		{
			teamMembers.add(person.getPersonId().toString());
		}
		// Begin First Turn Logic
		
		for (Person person: connection.team.values())
		{
			Room location = connection.map.get(person.getLocation());
			int randomIndex = generator.nextInt(location.getConnectedRooms().size());
			String targetName = location.getConnectedRooms().get(randomIndex);
			Move move = new Move(person.getPersonId(), targetName);
			actions.add(move);
		}
		
		// End First Turn Logic
		return actions;
	}

}
