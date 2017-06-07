package aar;

import aar.AAR.Type;

public class Atomic implements Comparable<Object>
{
	Atomic(String att)
	{
		this.att= att;
	}
	public Type type;
	public int position;
	public String att;
	public String in;
	public String out;
	@Override
	public int compareTo(Object o) throws ClassCastException{
		if(!(o instanceof Atomic))
			throw new ClassCastException();
		Atomic a=(Atomic)o;
		return -a.att.compareTo(this.att);
	}
	public boolean compare(Atomic a)
	{
		if(a.att.equals(this.att) && a.in.equals(this.in) && a.out.equals(this.out))
			return true;
		else 
			return false;
	}
}