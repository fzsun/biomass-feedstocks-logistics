package org.vt.services;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

import javax.ws.rs.Consumes;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;

import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

@Path("/services")
public class Services {
	
	  @SuppressWarnings("unchecked")
	  @POST
	  @Produces(MediaType.TEXT_PLAIN)
	  @Consumes(MediaType.APPLICATION_JSON)
	  //@Path("/algorithm1")
	  public String algorithm1(String input) {
		  System.out.println("Executing Algorithm!");
		  JSONObject response = new JSONObject();
	    try {
	    	//Parse the JSON data present in the string format
	        JSONParser parse = new JSONParser();
	        //Typecast the parsed json data in json object
	        JSONObject jobj = (JSONObject)parse.parse(input);
		    String s = null;
		    StringBuffer sb = new StringBuffer();
		    StringBuffer result = new StringBuffer();
		    // Build a process to run Python Algo.
			Process p = Runtime.getRuntime().exec("python F:\\biomass\\MS1M_gurobi.py "+jobj.get("sysnum")+' '+jobj.get("t_time"));
			BufferedReader stdInput = new BufferedReader(new InputStreamReader(p.getInputStream()));
	        BufferedReader stdError = new BufferedReader(new InputStreamReader(p.getErrorStream()));
	        
	        //read the output from the command
            while ((s = stdInput.readLine()) != null) {
                //System.out.println(s);
            	//if(s.startsWith("[Sys13]") || s.startsWith("LB") || s.startsWith(" UB") || s.startsWith("op.") || s.startsWith("loc") || s.startsWith("trans") || s.startsWith("inv") || s.startsWith("Gap") || s.startsWith("NumSSL") || s.startsWith("K_cnt") || s.startsWith("\"") ){
            		sb.append(s);
            		sb.append("\n");
            	//}
            }
            String text = sb.toString();
            String[] lines = text.split("\n");
            for (int i=0;i<lines.length;i++){
            	String line = lines[i];
            if (line.startsWith("[Sys13]")) {
                // Reverse the for loop to print "forwards"
                for (int j = i; j < lines.length; j++) {
                    // Make sure there is something there
                    //if (i - j >= 0) {
                        // Simply print it
                        System.out.println(lines[j]);
                        result.append(lines[j]);
                    //}
                }}}
            // read any errors from the attempted command
            while ((s = stdError.readLine()) != null) {
                System.out.println(s);
            }
            System.out.println("original"+ sb);
            System.out.println(result);
	        response.put("Result", result.toString());
	        stdInput.close();
	        stdError.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (ParseException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} 
	    return response.toString() ;
	  }
	  
	  @SuppressWarnings("unchecked")
	  @POST
	  @Produces(MediaType.TEXT_PLAIN)
	  @Consumes(MediaType.APPLICATION_JSON)
	  @Path("/tsp")
	  public String tsp(String input) {
		  System.out.println("Executing tsp!");
		  JSONObject response = new JSONObject();
	    try {
	    	//Parse the JSON data present in the string format
	        JSONParser parse = new JSONParser();
	        //Typecast the parsed json data in json object
	        JSONObject jobj = (JSONObject)parse.parse(input);
		    String s = null;
		    StringBuffer sb = new StringBuffer();
		    StringBuffer result = new StringBuffer();
		    // Build a process to run Python Algo.
			Process p = Runtime.getRuntime().exec("python F:\\biomass\\tsp.py "+jobj.get("t_time"));
			BufferedReader stdInput = new BufferedReader(new InputStreamReader(p.getInputStream()));
	        BufferedReader stdError = new BufferedReader(new InputStreamReader(p.getErrorStream()));
	        
	        //read the output from the command
            while ((s = stdInput.readLine()) != null) {
                //System.out.println(s);
                sb.append(s);
                sb.append("\n");
            }
            String text = sb.toString();
            String[] lines = text.split("\n");
            for (int i=0;i<lines.length;i++){
            	String line = lines[i];
            if (line.startsWith("Best")) {
                // Reverse the for loop to print "forwards"
                for (int j = i; j < lines.length; j++) {
                    // Make sure there is something there
                    //if (i - j >= 0) {
                        // Simply print it
                        System.out.println(lines[j]);
                        result.append(lines[j]);
                    //}
                }}}
            // read any errors from the attempted command
            while ((s = stdError.readLine()) != null) {
                System.out.println(s);
            }
            System.out.println(result);
	        response.put("Result", result.toString());
	        stdInput.close();
	        stdError.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (ParseException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} 
	    return response.toString() ;
	  }
}
