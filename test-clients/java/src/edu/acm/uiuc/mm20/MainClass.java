package edu.acm.uiuc.mm20;

import com.google.gson.Gson;

public class MainClass {

	public static void main(String[] args) {
		MM20AI myAI = new MM20AI();
		NetCommunicator nc = new NetCommunicator("127.0.0.1", 8080, myAI);
		nc.run();
		
	}
}
