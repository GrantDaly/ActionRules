package aar;

import java.util.ArrayList;
import java.util.List;

import aar.AAR.Type;

class Attribute
{
	public String att;
	public Type type; 
	public int position;
	public List<String> values= new ArrayList<String>();
	Attribute(String at, List<String> list, Type t, int pos)
	{
		att= at;
		values= list;
		type= t;
		position= pos;
	}
}