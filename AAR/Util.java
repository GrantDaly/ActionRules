package aar;

public abstract class Util {

    protected static double twoDecPlaces(double number) {
    	int numInt = (int) ((number+0.005)*100.0);
	number = ((double) numInt)/100.0;
	return(number);
	}  
    public static double outputDuration(double time1, double time2, String message) {
        double duration = (time2-time1)/1000;
	System.out.println(message+ " Time millis= " + duration + " seconds (" + duration/60 + " mins)");
        
	// Return
	return(duration);
	}
}
