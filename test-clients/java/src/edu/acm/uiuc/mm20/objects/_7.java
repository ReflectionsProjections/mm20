
package edu.acm.uiuc.mm20.objects;

import java.util.ArrayList;
import java.util.List;
import javax.annotation.Generated;
import com.google.gson.annotations.Expose;
import org.apache.commons.lang3.builder.EqualsBuilder;
import org.apache.commons.lang3.builder.HashCodeBuilder;
import org.apache.commons.lang3.builder.ToStringBuilder;

@Generated("org.jsonschema2pojo")
public class _7 {

    @Expose
    private List<Long> peopleInRoom = new ArrayList<Long>();
    @Expose
    private String room;
    @Expose
    private List<String> resources = new ArrayList<String>();
    @Expose
    private List<String> connectedRooms = new ArrayList<String>();

    public List<Long> getPeopleInRoom() {
        return peopleInRoom;
    }

    public void setPeopleInRoom(List<Long> peopleInRoom) {
        this.peopleInRoom = peopleInRoom;
    }

    public _7 withPeopleInRoom(List<Long> peopleInRoom) {
        this.peopleInRoom = peopleInRoom;
        return this;
    }

    public String getRoom() {
        return room;
    }

    public void setRoom(String room) {
        this.room = room;
    }

    public _7 withRoom(String room) {
        this.room = room;
        return this;
    }

    public List<String> getResources() {
        return resources;
    }

    public void setResources(List<String> resources) {
        this.resources = resources;
    }

    public _7 withResources(List<String> resources) {
        this.resources = resources;
        return this;
    }

    public List<String> getConnectedRooms() {
        return connectedRooms;
    }

    public void setConnectedRooms(List<String> connectedRooms) {
        this.connectedRooms = connectedRooms;
    }

    public _7 withConnectedRooms(List<String> connectedRooms) {
        this.connectedRooms = connectedRooms;
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
