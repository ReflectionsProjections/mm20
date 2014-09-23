
package edu.acm.uiuc.mm20.objects;

import javax.annotation.Generated;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;
import org.apache.commons.lang3.builder.EqualsBuilder;
import org.apache.commons.lang3.builder.HashCodeBuilder;
import org.apache.commons.lang3.builder.ToStringBuilder;

@Generated("org.jsonschema2pojo")
public class _2 {

    @Expose
    private Stats__ stats;
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

    public Stats__ getStats() {
        return stats;
    }

    public void setStats(Stats__ stats) {
        this.stats = stats;
    }

    public _2 withStats(Stats__ stats) {
        this.stats = stats;
        return this;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public _2 withName(String name) {
        this.name = name;
        return this;
    }

    public Boolean getSitting() {
        return sitting;
    }

    public void setSitting(Boolean sitting) {
        this.sitting = sitting;
    }

    public _2 withSitting(Boolean sitting) {
        this.sitting = sitting;
        return this;
    }

    public String getActed() {
        return acted;
    }

    public void setActed(String acted) {
        this.acted = acted;
    }

    public _2 withActed(String acted) {
        this.acted = acted;
        return this;
    }

    public Double getHunger() {
        return hunger;
    }

    public void setHunger(Double hunger) {
        this.hunger = hunger;
    }

    public _2 withHunger(Double hunger) {
        this.hunger = hunger;
        return this;
    }

    public Long getTurnsCoding() {
        return turnsCoding;
    }

    public void setTurnsCoding(Long turnsCoding) {
        this.turnsCoding = turnsCoding;
    }

    public _2 withTurnsCoding(Long turnsCoding) {
        this.turnsCoding = turnsCoding;
        return this;
    }

    public Double getFatigue() {
        return fatigue;
    }

    public void setFatigue(Double fatigue) {
        this.fatigue = fatigue;
    }

    public _2 withFatigue(Double fatigue) {
        this.fatigue = fatigue;
        return this;
    }

    public String getLocation() {
        return location;
    }

    public void setLocation(String location) {
        this.location = location;
    }

    public _2 withLocation(String location) {
        this.location = location;
        return this;
    }

    public Long getTeam() {
        return team;
    }

    public void setTeam(Long team) {
        this.team = team;
    }

    public _2 withTeam(Long team) {
        this.team = team;
        return this;
    }

    public Long getPersonId() {
        return personId;
    }

    public void setPersonId(Long personId) {
        this.personId = personId;
    }

    public _2 withPersonId(Long personId) {
        this.personId = personId;
        return this;
    }

    public Boolean getAsleep() {
        return asleep;
    }

    public void setAsleep(Boolean asleep) {
        this.asleep = asleep;
    }

    public _2 withAsleep(Boolean asleep) {
        this.asleep = asleep;
        return this;
    }

    public String getArchetype() {
        return archetype;
    }

    public void setArchetype(String archetype) {
        this.archetype = archetype;
    }

    public _2 withArchetype(String archetype) {
        this.archetype = archetype;
        return this;
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
