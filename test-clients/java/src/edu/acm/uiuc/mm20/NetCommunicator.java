package edu.acm.uiuc.mm20;


import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.Socket;
import java.net.UnknownHostException;



public class NetCommunicator extends Thread {

	Socket requestSocket;
	ObjectOutputStream out;
	BufferedReader in;
	boolean alive;
	String message;
	int port;
	private String IP;
	private MM20AI ai;

	public NetCommunicator(String IP, int port,MM20AI ai) {
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
			System.out.println("Connected to localhost in port 6969");
			// 2. get Input and Output streams
			out = new ObjectOutputStream(requestSocket.getOutputStream());
			out.flush();
			in = new BufferedReader(new InputStreamReader(requestSocket.getInputStream()));
			// 3: Communicating with the server
			do {
				message = in.readLine();
				System.out.println(message);
				ai.receivedMessage(message);
			} while (alive);
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

	public void sendMessage(String msg) {
		synchronized (out) {
			try {
				out.writeObject(msg);
				out.flush();
				System.out.println("client>" + msg);
			} catch (IOException ioException) {
				ioException.printStackTrace();
			}
		}
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
