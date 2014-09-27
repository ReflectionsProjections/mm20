package edu.acm.uiuc.mm20.objects.receive;

import javax.annotation.Generated;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;
import org.apache.commons.lang3.builder.EqualsBuilder;
import org.apache.commons.lang3.builder.HashCodeBuilder;
import org.apache.commons.lang3.builder.ToStringBuilder;

@Generated("org.jsonschema2pojo")
public class Events {

	@SerializedName("DEPLETEDSNACKTABLE")
	@Expose
	private String dEPLETEDSNACKTABLE;

	public String getDEPLETEDSNACKTABLE() {
		return dEPLETEDSNACKTABLE;
	}

	public void setDEPLETEDSNACKTABLE(String dEPLETEDSNACKTABLE) {
		this.dEPLETEDSNACKTABLE = dEPLETEDSNACKTABLE;
	}

	public Events withDEPLETEDSNACKTABLE(String dEPLETEDSNACKTABLE) {
		this.dEPLETEDSNACKTABLE = dEPLETEDSNACKTABLE;
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
