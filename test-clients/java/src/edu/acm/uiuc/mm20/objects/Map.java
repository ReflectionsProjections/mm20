
package edu.acm.uiuc.mm20.objects;

import javax.annotation.Generated;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;
import org.apache.commons.lang3.builder.EqualsBuilder;
import org.apache.commons.lang3.builder.HashCodeBuilder;
import org.apache.commons.lang3.builder.ToStringBuilder;

@Generated("org.jsonschema2pojo")
public class Map {

    @SerializedName("7")
    @Expose
    private edu.acm.uiuc.mm20.objects._7 _7;

    public edu.acm.uiuc.mm20.objects._7 get7() {
        return _7;
    }

    public void set7(edu.acm.uiuc.mm20.objects._7 _7) {
        this._7 = _7;
    }

    public Map with7(edu.acm.uiuc.mm20.objects._7 _7) {
        this._7 = _7;
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
