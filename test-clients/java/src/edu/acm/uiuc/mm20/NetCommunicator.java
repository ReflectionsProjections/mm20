package edu.acm.uiuc.mm20;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.ArrayList;

import com.google.gson.Gson;

import edu.acm.uiuc.mm20.objects.receive.ConnectionValidation;
import edu.acm.uiuc.mm20.objects.receive.GameState;
import edu.acm.uiuc.mm20.objects.send.Action;

public class NetCommunicator extends Thread {

	Socket requestSocket;
	PrintWriter out;
	BufferedReader in;
	boolean alive;
	String message;
	int port;
	private String IP;
	private MM20AI ai;
	Gson gson = new Gson();

	public NetCommunicator(String IP, int port, MM20AI ai) {
		// this.master = master;
		this.IP = IP;
		this.port = port;
		this.ai = ai;
	}

	@Override
	public void run() {
		this.alive = true;
		System.out.println("running");
		try {
			System.out.println("Connecting to " + IP);
			// 1. creating a socket to connect to the server
			requestSocket = new Socket(IP, port);
			System.out.println("Connected to localhost in port" + port);
			// 2. get Input and Output streams
			out = new PrintWriter(requestSocket.getOutputStream());
			out.flush();
			in = new BufferedReader(new InputStreamReader(
					requestSocket.getInputStream()));
			// 3: set up the game
			this.sendMessage(this.initialConnection());
			message = in.readLine();
			if (message != null)
			{
				validateConnection(message);
			}
			// 4: Main Game Loop communicating with the server
			do {
				message = in.readLine();
				if (message == null) {
					break;
				}
				// System.out.println(message);
				receiveTurn(message);
			} while (this.alive);
			in.close();
			out.close();
			requestSocket.close();
		} catch (UnknownHostException unknownHost) {
			System.err.println("You are trying to connect to an unknown host!");
		} catch (IOException ioException) {
			ioException.printStackTrace();
		} finally {
			// 4: Closing connection
			try {
				in.close();
				out.close();
				requestSocket.close();
			} catch (IOException ioException) {
				ioException.printStackTrace();
			}
		}
	}
	
	public void validateConnection(String message) {
		ConnectionValidation connect = gson.fromJson(message, ConnectionValidation.class);
		if (connect.status.equals("Success"))
		{
			System.out.println("Connected to Server");
			ArrayList<Action> actions = ai.firstTurn(connect);
			sendMessage(gson.toJson(actions));
		}
		else
		{
			System.out.println("Could not connect to Server");
			kill();
		}
	}

	public void sendMessage(String msg) {
		synchronized (out) {
			out.println(msg);
			out.flush();
			System.out.println("client>" + msg);
		}
	}
	
	public void receiveTurn(String message) {
        // System.out.print(message);
		ArrayList<Action> actions = ai.processTurn(gson.fromJson(message, GameState.class));
		Object toSend = actions;
		if (toSend != null){
			sendMessage(gson.toJson(toSend));
		} else {
			this.kill();
		}
	}
	
	private String initialConnection() {
		return gson.toJson(ai.makeTeam());
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see com.hex.pc.network.NetComunicaiton#kill()
	 */
	public void kill() {
		alive = false;
	}

}
