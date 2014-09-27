package edu.acm.uiuc.mm20.objects.receive;

import javax.annotation.Generated;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;
import org.apache.commons.lang3.builder.EqualsBuilder;
import org.apache.commons.lang3.builder.HashCodeBuilder;
import org.apache.commons.lang3.builder.ToStringBuilder;

@Generated("org.jsonschema2pojo")
public class Person {

	@Expose
	private Stats stats;
	@Expose
	private String name;
	@Expose
	private Boolean sitting;
	@Expose
	private String acted;
	@Expose
	private Double hunger;
	@SerializedName("turns_coding")
	@Expose
	private Long turnsCoding;
	@Expose
	private Double fatigue;
	@Expose
	private String location;
	@Expose
	private Long team;
	@SerializedName("person_id")
	@Expose
	private Long personId;
	@Expose
	private Boolean asleep;
	@Expose
	private String archetype;

	public Stats getStats() {
		return stats;
	}

	public String getName() {
		return name;
	}

	public Boolean getSitting() {
		return sitting;
	}

	public void setSitting(Boolean sitting) {
		this.sitting = sitting;
	}

	public String getActed() {
		return acted;
	}

	public Double getHunger() {
		return hunger;
	}

	public Long getTurnsCoding() {
		return turnsCoding;
	}

	public Double getFatigue() {
		return fatigue;
	}

	public String getLocation() {
		return location;
	}

	public Long getTeam() {
		return team;
	}

	public Long getPersonId() {
		return personId;
	}

	public Boolean getAsleep() {
		return asleep;
	}

	public String getArchetype() {
		return archetype;
	}

	@Override
	public String toString() {
		return ToStringBuilder.reflectionToString(this);
	}

	@Override
	public int hashCode() {
		return HashCodeBuilder.reflectionHashCode(this);
	}

	@Override
	public boolean equals(Object other) {
		return EqualsBuilder.reflectionEquals(this, other);
	}

}
