package aar;
import java.io.*;
import java.lang.reflect.Array;
import java.util.*;

public class AAR {
   public enum Type { CLASS, FLEXIBLE, STABLE}
   public List<HashMap<String, String>> rules= new ArrayList<HashMap<String, String>>();
   public static List<Attribute> atts= new ArrayList<Attribute>();
   public static List<Atomic> atomicRules= new ArrayList<Atomic>();
   public static int numRules;
   public static int numAtt;
   public static int minSupp;
   public static double minConf;
   public static String from;
   public static String into;
   public static boolean originalSupport;
   //Ryan Add
   public static String outputStem;
   public static boolean tomConfMeas;
   //End Ryan Add
   
   public static void main(String[] args) throws IOException {
		Properties ini = new Properties();
		ini.load(new FileInputStream("default.properties"));
		String filename= ini.getProperty("file");
		//Ryan Add
		outputStem = ini.getProperty("stem");
		FileWriter ofTrace= new FileWriter(outputStem + ".taar");
		BufferedWriter trace = new BufferedWriter(ofTrace);
		//End Ryan Add
	    AAR apriori=new AAR();
	    FileInputStream fstream = new FileInputStream(filename);
		from= ini.getProperty("from");
		into= ini.getProperty("into");
		minSupp=Integer.parseInt(ini.getProperty("MinSupp"));
		minConf=Double.parseDouble(ini.getProperty("MinConf"));
		originalSupport=Boolean.parseBoolean(ini.getProperty("originalSupport"));
		//Ryan Add
		String tempReadIn = ini.getProperty("tomConf");
		if (tempReadIn == null)
		{
			tomConfMeas = false;
		}
		else
		{
			tomConfMeas = Boolean.parseBoolean(tempReadIn);
		}
		//End Ryan Add
	    // Get the object of DataInputStream
	    DataInputStream in = new DataInputStream(fstream);
	    BufferedReader br = new BufferedReader(new InputStreamReader(in));
	    String line;
	    int pos=0;
	    boolean meta= true;
//		System.out.println("=================================================");
//		System.out.println("Step: Loading Data from "+filename);
//		System.out.println("Min Support is "+minSupp);
//		System.out.println("Min Confidence is "+minConf);
//		System.out.println("Target decision ["+ini.getProperty("decision")+","+from+"->"+into+"]");
//		System.out.println("Using orignal support: "+originalSupport);
//		System.out.println("=================================================");
		trace.write("=================================================\n");
		trace.write("Step: Loading Data from "+filename+"\n");
		trace.write("Min Support is "+minSupp+"\n");
		trace.write("Min Confidence is "+minConf+"\n");
		trace.write("Target decision ["+ini.getProperty("decision")+","+from+"->"+into+"]\n");
		trace.write("Using orignal support: "+originalSupport+"\n");
		trace.write("=================================================\n");
	    //Read File Line By Line
	    while ((line = br.readLine()) != null)   
	    {
	      if(line.equals("@data"))
	      {
	    	  meta= false;
	    	  continue;
	      }
	      if(meta)
	      /* Add the Stable attribute */
	      {
	    	  Type type = null;
	    	  String[] ar= line.split(" ");
                  system.out.println(ar);
	    	  if(ar[0].equalsIgnoreCase("@stable"))
	    		  type= Type.STABLE;
	    	  if(ar[0].equalsIgnoreCase("@class"))
	    		  type= Type.CLASS;
	    	  if(ar[0].equalsIgnoreCase("@flexible"))
	    		  type= Type.FLEXIBLE;
	    	  String[] temp= ar[1].split(":");
	    	  String att_name=temp[0];
	    	  String[] values= temp[1].split(",");
	    	  Attribute a= new Attribute(att_name, Arrays.asList(values), type, pos);
	    	  pos++;
	    	  atts.add(a);
	      }
	      else
	      /* Add the Rule */
	      {
	    	  String[] ar= line.split(",");
		      HashMap<String, String> tr=new HashMap<String, String>();
		      for(int i=0; i< ar.length; i++)
		      {
		    	  tr.put(getAttName(i),ar[i]);
		      }
		      apriori.rules.add(tr);
		      numRules++;
	      }	      
	      //System.out.println(line);
	    }
	    numAtt= pos;
	    // Printing the Attributes
	    //System.out.println("Start:");
	    trace.write("Start:\n");
	    makeAtomicRules();
	    // For Debug purpose
	    /*
	    Iterator<Atomic> ita= atomicRules.iterator();
	    while(ita.hasNext())
	    {
	    	Atomic c=(Atomic) ita.next();
	    	if(c.out=="-")
	    		System.out.println("@attribute {"+c.att+","+c.in+"}");
	    	else	    	
	    		System.out.println("@attribute {"+c.att+","+c.in+"->"+c.out+"}");
	    }
	    */
	    /*
	    Iterator<HashMap<String, String>> it= rules.iterator();
	    System.out.println("Transactions");
	    while(it.hasNext())
	    {
	    	HashMap m= (HashMap<String, String>)it.next();
	    	System.out.println(m);
	    }
	    System.out.println("Number of transactions = "+numRules+" Att number="+numAtt+" Minimum Support="+minSupp);
	    */
	    double time1 = (double) System.currentTimeMillis();
	    apriori.runApriori(trace);
		outputDuration(time1,(double)System.currentTimeMillis(), trace);
		trace.write("End of Timing!");
		trace.flush();
		trace.close();
   }
   public static void makeAtomicRules()
   {
	   for(Attribute at: atts)
	   {
		   Atomic a;
		   for(String in: at.values)
		   {
			   if(at.type!=Type.CLASS)
			   {
				   a= new Atomic(at.att);
				   a.type= at.type;
				   a.position=at.position;
				   a.in= in;
				   a.out= "-";
				   atomicRules.add(a);
			   }
			   if(at.type==Type.FLEXIBLE)
			   {
				   for(String out: at.values)
					   if(!out.equals(in))
					   {
						   Atomic b;
						   b= new Atomic(at.att);
						   b.type= at.type;
						   b.position=at.position;
				   		   b.in=in;
				   		   b.out=out;
				   		   atomicRules.add(b);
					   }
			   }
			   if(at.type==Type.CLASS && in.equalsIgnoreCase(from))
			   {
				   for(String out: at.values)
					   if(!out.equals(in) && out.equalsIgnoreCase(into))
					   {
						   Atomic b;
						   b= new Atomic(at.att);
						   b.position=at.position;
						   b.type= at.type;
				   		   b.in=in;
				   		   b.out=out;
				   		   atomicRules.add(b);
					   }
			   }
		   }
	   }
   }
   public void runApriori() throws IOException
   {
	   FileWriter ofstream = new FileWriter("out.txt");
	   BufferedWriter out = new BufferedWriter(ofstream);
	   System.out.println("Atomic Sets ------------------");
	   List<List<Atomic>> cas= new ArrayList<List<Atomic>>(); // Candidate action set
	   List<List<Atomic>> last= new ArrayList<List<Atomic>>(); // Candidate action set
	   // add the k= 1
	   for(Atomic a: atomicRules)
	   {
		   List<Atomic> actionItems=new ArrayList<Atomic>();
		   actionItems.add(a);
		   cas.add(actionItems);
	   }
	   cas= candidatePruning(cas, out);
	   do
	   {
		   double time1 = (double) System.currentTimeMillis();
		   System.out.println("------------------------------[Iteration]");
		   last= cas;
		   cas= candidateGeneration(cas);
		   System.out.print("[Done with the Generation] Candidats#"+ cas.size()+" ");
		   outputDuration(time1,(double)System.currentTimeMillis());
		   time1 = (double) System.currentTimeMillis();
		   cas= candidatePruning(cas, out);
		   System.out.print("[Done with the Pruning] Frequent#"+ cas.size()+" ");
		   outputDuration(time1,(double)System.currentTimeMillis());
		   out.write("------------------------[Iteration]\n");
		   out.flush();
	   }while (carryon && cas.size()!=0);
	   System.out.println("Action Rules generation -----------------------");
	   System.out.println("Rules:");
	   out.write("Action Rules generation -----------------------\n");
	   out.write("Rules:\n");
	   generateAR(out);
	   System.out.println("End -----------------------");
	   out.flush();
   }
   
   public void runApriori(BufferedWriter trace) throws IOException
   {
//	   FileWriter ofstream = new FileWriter("out.txt");
	   FileWriter ofstream = new FileWriter(outputStem+".aar");
	   BufferedWriter out = new BufferedWriter(ofstream);
//	   System.out.println("Atomic Sets ------------------");
	   trace.write("Atomic Sets ------------------\n");
	   List<List<Atomic>> cas= new ArrayList<List<Atomic>>(); // Candidate action set
	   List<List<Atomic>> last= new ArrayList<List<Atomic>>(); // Candidate action set
	   // add the k= 1
	   for(Atomic a: atomicRules)
	   {
		   List<Atomic> actionItems=new ArrayList<Atomic>();
		   actionItems.add(a);
		   cas.add(actionItems);
	   }
	   cas= candidatePruning(cas, out);
	   do
	   {
		   double time1 = (double) System.currentTimeMillis();
		   //System.out.println("------------------------------[Iteration]");
		   trace.write("------------------------------[Iteration]\n");
		   last= cas;
		   cas= candidateGeneration(cas);
//		   System.out.print("[Done with the Generation] Candidats#"+ cas.size()+" ");
		   trace.write("[Done with the Generation] Candidats#"+ cas.size()+" ");
		   outputDuration(time1,(double)System.currentTimeMillis(),trace);
		   time1 = (double) System.currentTimeMillis();
		   cas= candidatePruning(cas, out);
//		   System.out.print("[Done with the Pruning] Frequent#"+ cas.size()+" ");
		   trace.write("[Done with the Pruning] Frequent#"+ cas.size()+" ");
		   outputDuration(time1,(double)System.currentTimeMillis(),trace);
		   //Ryan Remove
//		   out.write("------------------------[Iteration]\n");
//		   out.flush();
		   //End Ryan Remove
	   }while (carryon && cas.size()!=0);
	   //System.out.println("Action Rules generation -----------------------");
	   //System.out.println("Rules:");
	   trace.write("Action Rules generation -----------------------\n");
	   trace.write("Rules:\n");
	   //Ryan Remove
	   //out.write("Action Rules generation -----------------------\n");
	   //out.write("Rules:\n");
	   //End Ryan Remove
	   generateAR(out);
	   //System.out.println("End -----------------------");
	   trace.write("End -----------------------\n");
	   out.flush();
	   trace.flush();
   }
   @SuppressWarnings("unchecked")
   public static List<List<Atomic>> candidateGeneration(List<List<Atomic>> cas)
   {
	   int count=0;
	   List<List<Atomic>> cand= new ArrayList<List<Atomic>>();
	   //Join
	   for(int i=0; i<cas.size(); i++)
	   {
		   List<Atomic> a=cas.get(i);
		   for(int j=i+1; j< cas.size(); j++)
		   {
			   List<Atomic> b=cas.get(j); 
			   List<Atomic> join= atomicJoin(a,b);
			   if(join != null)
			   {
				   boolean check= true;
				   for(int k=0; k<join.size();k++)
				   {
					   List<Atomic> temp= new ArrayList<Atomic>(join);
					   temp.remove(k);
					   if(!cas.contains(temp))
					   {
						   check= false; 
						   break;
					   }
				   }
				   if(check)
				   {	
					   Collections.sort(join);
					   cand.add(join);
				   }
			   }
			   else count++;
		   }
	   }
	   //For Debug Purpose
	   //System.out.print(" Ejected#"+ count+" ");
	   return cand;
   }
   public static List<Atomic> atomicJoin(List<Atomic> a, List<Atomic> b)
   {
	   if(a.size()>2)
	   {
		   List<Atomic> asub= a.subList(0,a.size()-1);
		   List<Atomic> bsub= b.subList(0,b.size()-1);
		   int s= asub.size();
		   if (compareActionSet(asub,bsub))
		   {
			   if(! a.get(a.size()-1).equals(b.get(b.size()-1)))
			   {
				   List<Atomic> join = new ArrayList<Atomic>();
				   join.addAll(a);
				   join.add(b.get(b.size()-1));
				   Collections.sort(join);
				   return join;
			   }
		   }
	   }
	   else if(a.size()==2)
		   {
			   Atomic asub= a.get(0);
			   Atomic bsub= b.get(0);
			   if (asub.equals(bsub))
			   {
				   if(!a.get(1).equals(b.get(1)))
				   {
					   List<Atomic> join = new ArrayList<Atomic>();
					   join.addAll(a);
					   join.add(b.get(1));
					   Collections.sort(join);
					   return join;
				   }
			   }
		   }
	   else
	   {
		   Atomic x, y;
		   x=a.get(0);
		   y=b.get(0);
		   if (x.compareTo(y)!=0)
		   {
			   List<Atomic> join = new ArrayList<Atomic>();
			   join.addAll(a);
			   join.add(b.get(b.size()-1));
			   return join;
		   }
	   }
	   return null;
   }
   public List<List<Atomic>> freq= new ArrayList<List<Atomic>>();
   public List<List<Atomic>> candidatePruning(List<List<Atomic>> cas, BufferedWriter out) throws IOException
   {
	   carryon= false;
	   List<List<Atomic>> ret= new ArrayList<List<Atomic>>();
	   for(List<Atomic> a: cas)
	   {
		   boolean freqDecision= false;
		   if(hasADecision(a))
		   {
			   carryon=true;
			   freqDecision=true;
		   }
		   int support= getSupport(a);
		   if(support>=minSupp)
		   {
			   ret.add(a);
			   //displayFrequentActionRule(a, support, out);
			   if(freqDecision) freq.add(a);
		   }
	   }
	   return ret;
   }
   public static boolean hasADecision(List<Atomic> list)
   {
	   for(Atomic a: list)
		   if(a.type==Type.CLASS)
			   return true;
	   return false;
   }
   public static List<Atomic> trimDecision(List<Atomic> list)
   {
	   List<Atomic> out= new ArrayList<Atomic>();
	   for(Atomic a: list)
		   if(a.type!=Type.CLASS)
			   out.add(a);
	   return out;
   }
   public static List<Atomic> getDecision(List<Atomic> list)
   {
	   List<Atomic> out= new ArrayList<Atomic>();
	   for(Atomic a: list)
		   if(a.type==Type.CLASS)
			   out.add(a);
	   return out;
   }
   public static boolean carryon= true;
   public int getSupport(List<Atomic> actions)
   {
	   int count_in=0;
	   int count_out=0;
	   int count= 0;
	   for(HashMap<String, String> m: rules)
	   {
		   boolean check_in= true;
		   boolean check_out= true;
		   for(Atomic a: actions)
		   {
			   if(m.containsKey(a.att))
			   {
				  String value= (String) m.get(a.att);
				  if(!value.equals(a.in))
				  {
					  check_in=false;
				  }
				  String out= a.out.equals("-")? a.in: a.out;
				  if(!value.equals(out))
				  {
					  check_out=false;
				  }
			   }
			   else
			   {
				   check_in=false;
				   check_out=false;
			   }
		   }
		   if(check_in)
			   count_in++;
		   if(check_out)
			   count_out++;
	   }
	   /* Support as per the AAR paper */
	   if(originalSupport) 
		   count= min(count_in,count_out);
	   /* Support as per the FAARM paper*/
	   else 
		   count= count_in * count_out;
	   // Eliminate the action if it is less than the support
	   return count;
   }

   public int getOccurance(List<Atomic> actions, boolean getCheckIn)
   {
	   int count_in=0;
	   int count_out=0;
	   int count= 0;
	   for(HashMap<String, String> m: rules)
	   {
		   boolean check_in= true;
		   boolean check_out= true;
		   for(Atomic a: actions)
		   {
			   if(m.containsKey(a.att))
			   {
				  String value= (String) m.get(a.att);
				  if(!value.equals(a.in))
				  {
					  check_in=false;
				  }
				  String out= a.out.equals("-")? a.in: a.out;
				  if(!value.equals(out))
				  {
					  check_out=false;
				  }
			   }
			   else
			   {
				   check_in=false;
				   check_out=false;
			   }
		   }
		   if(check_in)
			   count_in++;
		   if(check_out)
			   count_out++;
	   }
	   /*Get the number of times check in occurred*/
	   if(getCheckIn) 
		   count= count_in;
	   /*Get the number of times check out occurred*/
	   else 
		   count= count_out;
	   // Eliminate the action if it is less than the support
	   return count;
   }

   public static int min(int a, int b)
   {
	   if (a<b) return a;
	   else return b;
   }

   public static int max(int a, int b)
   {
	   if (a>b) return a;
	   else return b;
   }

   private static boolean compareActionSet(List<Atomic> asub, List<Atomic> bsub)
   {
	   for(int i=0; i < asub.size();i++)
		   if(!asub.get(i).compare(bsub.get(i)))				
			   return false;
	   return true;
   }
   
   private static void displayFrequentActionRule(List<Atomic> list, int support, BufferedWriter out) throws IOException
   {
		   String toPrint="";
		   for(Atomic c: list)
		   {
		    	if(c.out.contains("-"))
		    		toPrint+="["+c.att+","+c.in+"]";
		    	else	    
		    		toPrint+="["+c.att+","+c.in+"->"+c.out+"]";
		   }
		   toPrint=toPrint+"("+support+")";
		   System.out.println(toPrint);
		   out.write(toPrint+"\n");
   }

   private static void displayActionRule(int count, List<Atomic> antecedent, List<Atomic> decision, 
		   int supportForAR, int supportForAntecedent, int countA1, int countA2, 
		   int countR1, int countR2, double conf, BufferedWriter out) throws IOException
   {
	   String ante="";
	   String post="";
	   for(Atomic c: antecedent)
	   {
		   if(c.out.contains("-"))
			   ante+="["+c.att+","+c.in+"]";
		   else	    
			   ante+="["+c.att+","+c.in+"->"+c.out+"]";
	   }
	   for(Atomic c: decision)
	   {
		   if(c.out.contains("-"))
			   post+="["+c.att+","+c.in+"]";
		   else	    
			   post+="["+c.att+","+c.in+"->"+c.out+"]";
	   }
	   
	   int indexCheck = ante.indexOf("->");
	   if (indexCheck != -1)
	   {
		   //String toPrint= "("+count+") {"+ante+"}("+supportForAntecedent+")  -> {"+ post+"}("+supportForAR+") conf=("+twoDecPlaces(conf)+"%)";
		   String toPrint= "("+count+")  "+ante+"  ->  "+post+"  "+supportForAntecedent+" "+supportForAR+" "+twoDecPlaces(conf*100.0)+"% "+
		   countA1+" "+countR1+" "+countA2+" "+countR2;
		   //System.out.println(toPrint);
		   out.write(toPrint+"\n");
	   }
   }
   
   private static void displayActionRule(int count, List<Atomic> antecedent, List<Atomic> decision, int supportForAR, int supportForAntecedent, double conf, BufferedWriter out) throws IOException
   {
	   String ante="";
	   String post="";
	   for(Atomic c: antecedent)
	   {
		   if(c.out.contains("-"))
			   ante+="["+c.att+","+c.in+"]";
		   else	    
			   ante+="["+c.att+","+c.in+"->"+c.out+"]";
	   }
	   for(Atomic c: decision)
	   {
		   if(c.out.contains("-"))
			   post+="["+c.att+","+c.in+"]";
		   else	    
			   post+="["+c.att+","+c.in+"->"+c.out+"]";
	   }
//	   String toPrint= "("+count+") {"+ante+"}("+supportForAntecedent+")  -> {"+ post+"}("+supportForAR+") conf=("+twoDecPlaces(conf)+"%)";
	   String toPrint= "("+count+")  "+ante+"  ->  "+post+"  "+supportForAntecedent+" "+supportForAR+" "+twoDecPlaces(conf*100.0)+"%";
	   //System.out.println(toPrint);
	   out.write(toPrint+"\n");
   }
	public static String getAttName(int pos)
	{
		for(Attribute a: atts)
			if(a.position==pos)
				return a.att;
		return "";
	}
	public void generateAR(List<List<Atomic>> rules, BufferedWriter out) throws IOException
	{
		int count=1;
		for(List<Atomic> rule:rules)
		{
			if(hasADecision(rule))
			{
				List<Atomic> decision= getDecision(rule);
				List<Atomic> antecedent= trimDecision(rule);
				Atomic[][] combine=combinations(antecedent);
				for(int i=0; i< combine.length; i++)
				{
					List<Atomic> temp= new ArrayList<Atomic>(Arrays.asList(combine[i]));
					temp.addAll(decision);
					int supportForAR=getSupport(temp);
					int supportForAntecedent=getSupport(Arrays.asList(combine[i]));
					double conf= (double) supportForAR/supportForAntecedent;
					if(conf>=minConf)
						displayActionRule(count++, Arrays.asList(combine[i]), decision, supportForAR, supportForAntecedent, conf, out);
				}
			}
		}
	}
	public void generateAR(BufferedWriter out) throws IOException
	{
		int count=1;
		for(List<Atomic> rule:freq)
		{
			List<Atomic> decision= getDecision(rule);
			List<Atomic> antecedent= trimDecision(rule);
			if (originalSupport)
			{
				int supportForAR=getSupport(rule);
				int supportForAntecedent=getSupport(antecedent);
				int ruleA1=getOccurance(rule,true);
				int ruleA2=getOccurance(rule,false);
				int supportA1=getOccurance(antecedent,true);
				int supportA2=getOccurance(antecedent, false);
				double confA1= (double) ruleA1/supportA1;
				double confA2= (double) ruleA2/supportA2;
				double conf = 0.0;
				//Ryan Add and Modify
				if (tomConfMeas == true)
				{
					conf= (double) confA2;
				}
				else
				{
					conf= (double) confA1 * confA2;
				}
				//double conf= (double) confA1 * confA2;
				//End Ryan Add and Modify
				if(conf>=minConf)
					displayActionRule(count++, antecedent, decision,  supportForAR, supportForAntecedent,
							supportA1, supportA2, ruleA1, ruleA2, conf, out);
					//displayActionRule(count++,antecedent, decision, supportForAR, supportForAntecedent, conf, out);
			}
			else
			{
				int supportForAR=getSupport(rule);
				int supportForAntecedent=getSupport(antecedent);
				double conf= (double) supportForAR/supportForAntecedent;
				if(conf>=minConf)
					displayActionRule(count++,antecedent, decision, supportForAR, supportForAntecedent, conf, out);
			}
		}
	}
    protected static double twoDecPlaces(double number) {
    	int numInt = (int) ((number+0.005)*100.0);
	number = ((double) numInt)/100.0;
	return(number);
	}  
    /*
     * Create combination of the largest rules
     */
    protected static Atomic[][] combinations(List<Atomic> antecedent) {
    	if (antecedent == null) return(null);
    	else {
    		Atomic[][] outputSet = new Atomic[getCombinations(antecedent)][];
    	    combinations(antecedent,0,null,outputSet,0);
    	    return(outputSet);
    	    }
    	}
    private static int combinations(List<Atomic> inputSet, int inputIndex,
    		Atomic[] sofar, Atomic[][] outputSet, int outputIndex) {
    	Atomic[] tempSet;
	int index=inputIndex;

    	// Loop through input array

	while(index < inputSet.size()) {
            tempSet = realloc1(sofar,inputSet.get(index));
            outputSet[outputIndex] = tempSet;
	    outputIndex = combinations(inputSet,index+1,
	    		copyItemSet(tempSet),outputSet,outputIndex+1);
    	    index++;
	    }

    	// Return

    	return(outputIndex);
    	}  
    private static int getCombinations(List<Atomic> antecedent) {
    	int numComb;	

	numComb = (int) Math.pow(2.0,antecedent.size())-1;
	    
    	// Return

        return(numComb);
        }
    protected static Atomic[] copyItemSet(Atomic[] itemSet) {
    	
    	// Check whether there is a itemSet to copy
    	if (itemSet == null) return(null);
    	
    	// Do copy and return
    	Atomic[] newItemSet = new Atomic[itemSet.length];
    	for(int index=0;index<itemSet.length;index++) {
    	    newItemSet[index] = itemSet[index];
    	    }
            
    	// Return
    	return(newItemSet);
    	}
    protected static Atomic[] realloc1(Atomic[] oldItemSet, Atomic inputSet) {

    	// No old item set

    	if (oldItemSet == null) {
    		Atomic[] newItemSet = {inputSet};
    	    return(newItemSet);
    	    }

    	// Otherwise create new item set with length one greater than old
    	// item set

    	int oldItemSetLength = oldItemSet.length;
    	Atomic[] newItemSet = new Atomic[oldItemSetLength+1];

    	// Loop

    	int index;
    	for (index=0;index < oldItemSetLength;index++)
    		newItemSet[index] = oldItemSet[index];
    	newItemSet[index] = inputSet;

    	// Return new item set

    	return(newItemSet);
    	}
    public static double outputDuration(double time1, double time2) {
        double duration = (time2-time1)/1000;
	System.out.println("Time = " + twoDecPlaces(duration) + 
			" seconds (" + twoDecPlaces(duration/60) + " mins)");
        
	// Return
	return(duration);
	}

    public static double outputDuration(double time1, double time2, BufferedWriter trace) throws IOException {
        double duration = (time2-time1)/1000;
//	System.out.println("Time = " + twoDecPlaces(duration) + 
//			" seconds (" + twoDecPlaces(duration/60) + " mins)");
	trace.write("Time = " + twoDecPlaces(duration) + 
			" seconds (" + twoDecPlaces(duration/60) + " mins)\n");
        
	// Return
	return(duration);
	}
}
