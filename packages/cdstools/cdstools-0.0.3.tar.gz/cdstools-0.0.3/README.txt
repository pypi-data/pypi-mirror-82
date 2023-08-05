This package offers users simple tools designed for Credit Default Swap (CDS) data. 
Included in this package is a hazard rate bootstrapping function which 
implements the JP Morgan model for determining hazard rate curves, and spread calculators
for both vanilla and binary CDSs. All functions linearly interpolate/extrapolate yield
curve values wherever necessary.

To be included in future releases will be a function that prices Credit Default 
Swaptions (options on CDSs). Also, later editions of this package will offer the users
options for interpolating/extrapolating yield curve values. 

Bootstrapping Function:
This function implements the so-called JP Morgan model. This model makes the 
assumptions that the interest rate process is independent of the default process
and that default leg pays at the end of each accrual period. Typically, regular
fee payments occur at the end of each period. To that end, this model assumes
that defaults occur midway buring each payment period. And finally, this model
assumes that the hazard rate is piecewise constant on the intervals that correspond
to the maturities of the CDS contracts.

CDS pricing function:
This function calculates the "fair" spread of a vanilla CDS, i.e. the spread that 
makes the value of the default/floating leg equal to the value of the payment/fixed 
leg. This is accomplished by using a given yield curve and given credit curve.

Binary CDS pricing function:
Similar to the previous function, this one calculates the "fair" spread of a binary CDS
by finding the spread that equates the value of the default/floating leg equal to
the value of the payment/fixed leg. This is also accomplished using a provided
yield curve and credit curve

