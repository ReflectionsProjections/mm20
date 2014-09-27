package edu.acm.uiuc.mm20.objects.send;

public class NewPerson {
	private Object archetype;
	private String name;

	public NewPerson(String name, Archetypes archetype){
		this.name = name;
		this.archetype = archetype;
	}
}
