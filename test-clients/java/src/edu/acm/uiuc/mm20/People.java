
package edu.acm.uiuc.mm20;

import javax.annotation.Generated;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;
import org.apache.commons.lang3.builder.EqualsBuilder;
import org.apache.commons.lang3.builder.HashCodeBuilder;
import org.apache.commons.lang3.builder.ToStringBuilder;

@Generated("org.jsonschema2pojo")
public class People {

    @SerializedName("0")
    @Expose
    private edu.acm.uiuc.mm20._0 _0;
    @SerializedName("1")
    @Expose
    private edu.acm.uiuc.mm20._1 _1;
    @SerializedName("2")
    @Expose
    private edu.acm.uiuc.mm20._2 _2;
    @SerializedName("3")
    @Expose
    private edu.acm.uiuc.mm20._3 _3;
    @SerializedName("4")
    @Expose
    private edu.acm.uiuc.mm20._4 _4;
    @SerializedName("5")
    @Expose
    private edu.acm.uiuc.mm20._5 _5;

    public edu.acm.uiuc.mm20._0 get0() {
        return _0;
    }

    public void set0(edu.acm.uiuc.mm20._0 _0) {
        this._0 = _0;
    }

    public People with0(edu.acm.uiuc.mm20._0 _0) {
        this._0 = _0;
        return this;
    }

    public edu.acm.uiuc.mm20._1 get1() {
        return _1;
    }

    public void set1(edu.acm.uiuc.mm20._1 _1) {
        this._1 = _1;
    }

    public People with1(edu.acm.uiuc.mm20._1 _1) {
        this._1 = _1;
        return this;
    }

    public edu.acm.uiuc.mm20._2 get2() {
        return _2;
    }

    public void set2(edu.acm.uiuc.mm20._2 _2) {
        this._2 = _2;
    }

    public People with2(edu.acm.uiuc.mm20._2 _2) {
        this._2 = _2;
        return this;
    }

    public edu.acm.uiuc.mm20._3 get3() {
        return _3;
    }

    public void set3(edu.acm.uiuc.mm20._3 _3) {
        this._3 = _3;
    }

    public People with3(edu.acm.uiuc.mm20._3 _3) {
        this._3 = _3;
        return this;
    }

    public edu.acm.uiuc.mm20._4 get4() {
        return _4;
    }

    public void set4(edu.acm.uiuc.mm20._4 _4) {
        this._4 = _4;
    }

    public People with4(edu.acm.uiuc.mm20._4 _4) {
        this._4 = _4;
        return this;
    }

    public edu.acm.uiuc.mm20._5 get5() {
        return _5;
    }

    public void set5(edu.acm.uiuc.mm20._5 _5) {
        this._5 = _5;
    }

    public People with5(edu.acm.uiuc.mm20._5 _5) {
        this._5 = _5;
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
