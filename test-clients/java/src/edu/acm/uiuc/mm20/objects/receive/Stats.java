package edu.acm.uiuc.mm20.objects.receive;

import javax.annotation.Generated;
import com.google.gson.annotations.Expose;
import org.apache.commons.lang3.builder.EqualsBuilder;
import org.apache.commons.lang3.builder.HashCodeBuilder;
import org.apache.commons.lang3.builder.ToStringBuilder;

@Generated("org.jsonschema2pojo")
public class Stats {

	@Expose
	private Long spy;
	@Expose
	private Long theorize;
	@Expose
	private Long refactor;
	@Expose
	private Long codingProwess;
	@Expose
	private Long test;
	@Expose
	private Long optimize;

	public Long getSpy() {
		return spy;
	}

	public void setSpy(Long spy) {
		this.spy = spy;
	}

	public Stats withSpy(Long spy) {
		this.spy = spy;
		return this;
	}

	public Long getTheorize() {
		return theorize;
	}

	public void setTheorize(Long theorize) {
		this.theorize = theorize;
	}

	public Stats withTheorize(Long theorize) {
		this.theorize = theorize;
		return this;
	}

	public Long getRefactor() {
		return refactor;
	}

	public void setRefactor(Long refactor) {
		this.refactor = refactor;
	}

	public Stats withRefactor(Long refactor) {
		this.refactor = refactor;
		return this;
	}

	public Long getCodingProwess() {
		return codingProwess;
	}

	public void setCodingProwess(Long codingProwess) {
		this.codingProwess = codingProwess;
	}

	public Stats withCodingProwess(Long codingProwess) {
		this.codingProwess = codingProwess;
		return this;
	}

	public Long getTest() {
		return test;
	}

	public void setTest(Long test) {
		this.test = test;
	}

	public Stats withTest(Long test) {
		this.test = test;
		return this;
	}

	public Long getOptimize() {
		return optimize;
	}

	public void setOptimize(Long optimize) {
		this.optimize = optimize;
	}

	public Stats withOptimize(Long optimize) {
		this.optimize = optimize;
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
