package edu.acm.uiuc.mm20.objects.receive;

import javax.annotation.Generated;
import com.google.gson.annotations.Expose;
import org.apache.commons.lang3.builder.EqualsBuilder;
import org.apache.commons.lang3.builder.HashCodeBuilder;
import org.apache.commons.lang3.builder.ToStringBuilder;

@Generated("org.jsonschema2pojo")
public class AiStats {

	@Expose
	private Double stability;
	@Expose
	private Double implementation;
	@Expose
	private Double complexity;
	@Expose
	private Double optimization;
	@Expose
	private Double theory;

	public Double getStability() {
		return stability;
	}

	public void setStability(Double stability) {
		this.stability = stability;
	}

	public AiStats withStability(Double stability) {
		this.stability = stability;
		return this;
	}

	public Double getImplementation() {
		return implementation;
	}

	public void setImplementation(Double implementation) {
		this.implementation = implementation;
	}

	public AiStats withImplementation(Double implementation) {
		this.implementation = implementation;
		return this;
	}

	public Double getComplexity() {
		return complexity;
	}

	public void setComplexity(Double complexity) {
		this.complexity = complexity;
	}

	public AiStats withComplexity(Double complexity) {
		this.complexity = complexity;
		return this;
	}

	public Double getOptimization() {
		return optimization;
	}

	public void setOptimization(Double optimization) {
		this.optimization = optimization;
	}

	public AiStats withOptimization(Double optimization) {
		this.optimization = optimization;
		return this;
	}

	public Double getTheory() {
		return theory;
	}

	public void setTheory(Double theory) {
		this.theory = theory;
	}

	public AiStats withTheory(Double theory) {
		this.theory = theory;
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
