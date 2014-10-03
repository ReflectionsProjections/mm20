package edu.acm.uiuc.mm20;

public class MainClass {

	public static void main(String[] args) {
		int port = 8080;
		String hostname = "127.0.0.1";
		if(args.length > 1){
			hostname = args[0];
			port = Integer.parseInt(args[1]);
		}
		MM20AI myAI = new MM20AI();
		NetCommunicator nc = new NetCommunicator(hostname, port, myAI);
		nc.run();
	}
}
