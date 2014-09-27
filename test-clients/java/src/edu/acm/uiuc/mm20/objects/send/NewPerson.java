package edu.acm.uiuc.mm20.objects.send;

public class NewPerson {
	private Object archetype;
	private String name;

	public NewPerson(String name, Archetypes archetype) {
		this.setName(name);
		this.setArchetype(archetype);
	}

	public Object getArchetype() {
		return archetype;
	}

	public void setArchetype(Object archetype) {
		this.archetype = archetype;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}
}
