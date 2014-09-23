
package edu.acm.uiuc.mm20;

import javax.annotation.Generated;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;
import org.apache.commons.lang3.builder.EqualsBuilder;
import org.apache.commons.lang3.builder.HashCodeBuilder;
import org.apache.commons.lang3.builder.ToStringBuilder;

@Generated("org.jsonschema2pojo")
public class _0 {

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

    public void setStats(Stats stats) {
        this.stats = stats;
    }

    public _0 withStats(Stats stats) {
        this.stats = stats;
        return this;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public _0 withName(String name) {
        this.name = name;
        return this;
    }

    public Boolean getSitting() {
        return sitting;
    }

    public void setSitting(Boolean sitting) {
        this.sitting = sitting;
    }

    public _0 withSitting(Boolean sitting) {
        this.sitting = sitting;
        return this;
    }

    public String getActed() {
        return acted;
    }

    public void setActed(String acted) {
        this.acted = acted;
    }

    public _0 withActed(String acted) {
        this.acted = acted;
        return this;
    }

    public Double getHunger() {
        return hunger;
    }

    public void setHunger(Double hunger) {
        this.hunger = hunger;
    }

    public _0 withHunger(Double hunger) {
        this.hunger = hunger;
        return this;
    }

    public Long getTurnsCoding() {
        return turnsCoding;
    }

    public void setTurnsCoding(Long turnsCoding) {
        this.turnsCoding = turnsCoding;
    }

    public _0 withTurnsCoding(Long turnsCoding) {
        this.turnsCoding = turnsCoding;
        return this;
    }

    public Double getFatigue() {
        return fatigue;
    }

    public void setFatigue(Double fatigue) {
        this.fatigue = fatigue;
    }

    public _0 withFatigue(Double fatigue) {
        this.fatigue = fatigue;
        return this;
    }

    public String getLocation() {
        return location;
    }

    public void setLocation(String location) {
        this.location = location;
    }

    public _0 withLocation(String location) {
        this.location = location;
        return this;
    }

    public Long getTeam() {
        return team;
    }

    public void setTeam(Long team) {
        this.team = team;
    }

    public _0 withTeam(Long team) {
        this.team = team;
        return this;
    }

    public Long getPersonId() {
        return personId;
    }

    public void setPersonId(Long personId) {
        this.personId = personId;
    }

    public _0 withPersonId(Long personId) {
        this.personId = personId;
        return this;
    }

    public Boolean getAsleep() {
        return asleep;
    }

    public void setAsleep(Boolean asleep) {
        this.asleep = asleep;
    }

    public _0 withAsleep(Boolean asleep) {
        this.asleep = asleep;
        return this;
    }

    public String getArchetype() {
        return archetype;
    }

    public void setArchetype(String archetype) {
        this.archetype = archetype;
    }

    public _0 withArchetype(String archetype) {
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
