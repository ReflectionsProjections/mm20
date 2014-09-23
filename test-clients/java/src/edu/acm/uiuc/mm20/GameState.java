
package edu.acm.uiuc.mm20;

import java.util.ArrayList;
import java.util.List;
import javax.annotation.Generated;
import com.google.gson.annotations.Expose;
import org.apache.commons.lang3.builder.EqualsBuilder;
import org.apache.commons.lang3.builder.HashCodeBuilder;
import org.apache.commons.lang3.builder.ToStringBuilder;

@Generated("org.jsonschema2pojo")
public class GameState {

    @Expose
    private AiStats aiStats;
    @Expose
    private Map map;
    @Expose
    private List<Object> errors = new ArrayList<Object>();
    @Expose
    private People people;
    @Expose
    private List<Message> messages = new ArrayList<Message>();
    @Expose
    private Events events;

    public AiStats getAiStats() {
        return aiStats;
    }

    public void setAiStats(AiStats aiStats) {
        this.aiStats = aiStats;
    }

    public GameState withAiStats(AiStats aiStats) {
        this.aiStats = aiStats;
        return this;
    }

    public Map getMap() {
        return map;
    }

    public void setMap(Map map) {
        this.map = map;
    }

    public GameState withMap(Map map) {
        this.map = map;
        return this;
    }

    public List<Object> getErrors() {
        return errors;
    }

    public void setErrors(List<Object> errors) {
        this.errors = errors;
    }

    public GameState withErrors(List<Object> errors) {
        this.errors = errors;
        return this;
    }

    public People getPeople() {
        return people;
    }

    public void setPeople(People people) {
        this.people = people;
    }

    public GameState withPeople(People people) {
        this.people = people;
        return this;
    }

    public List<Message> getMessages() {
        return messages;
    }

    public void setMessages(List<Message> messages) {
        this.messages = messages;
    }

    public GameState withMessages(List<Message> messages) {
        this.messages = messages;
        return this;
    }

    public Events getEvents() {
        return events;
    }

    public void setEvents(Events events) {
        this.events = events;
    }

    public GameState withEvents(Events events) {
        this.events = events;
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
