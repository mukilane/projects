/*
* (C) Mukil Elango
* 
* A command line tool to check 
* 1. The current location of ISS
* 2. Expected overhead passing of ISS for the current user location
* 3. The current list of people in Space
* 
* Usage:
* $ dart spacewatch.dart -o isslocation
* $ dart spacewatch.dart -o issoverhead
* $ dart spacewatch.dart -o peopleinspace
* 
*/
import 'dart:io';
import 'dart:convert';
import 'dart:async';

import 'package:args/args.dart';
import 'package:http/http.dart' as http;

const object = "object";

ArgResults argResults;

void main(List<String> arguments) {
	final parser = new ArgParser()
		..addFlag(object, negatable: false, abbr: 'o');
	argResults = parser.parse(arguments);
	List<String> res = argResults.rest;
	if (res == true) {
		if (res[0] == "isslocation") {
			getIssLocation();
		} else if (res[0] == "issoverhead") {
			geolocate();
		} else if (res[0] == "peopleinspace") {
			peopleInSpace();
		}
	} else {
		print("SpaceWatch");
		print("A command-line tool for checking space status");
		print("Usage:");
		print("To get ISS location");
		print(r"$ dart spacewatch.dart -o isslocation");
		print("\nTo get the time of overhead passage of ISS");
		print(r"$ dart spacewatch.dart -o issoverhead");
		print("\nTo get a list of people in space");
		print(r"$ dart spacewatch.dart -o peopleinspace");
	}
}

void getIssLocation() {
	const issEndpoint = "http://api.open-notify.org/iss-now.json";
	http.read(issEndpoint)
		.then((response) {
			Map result = JSON.decode(response);
			String output_text = "The ISS is located at " + result['iss_position']['latitude'] 
				+ " latitude and " + result['iss_position']['longitude'] + " longitude.";
			print(output_text);
		});
}

void geolocate() {
	const geolocateEndpoint = "http://ip-api.com/json/";
	http.read(geolocateEndpoint)
		.then((response) {
			var location = new Map<String, String>();
			Map result = JSON.decode(response);
			location['latitude'] = result['lat'];
			location['longitude'] = result['lon'];
			issOverhead(location);
		});
}

void issOverhead(Map<String, String> location) {
	var issPassOverheadEndpoint = "http://api.open-notify.org/iss-pass.json?lat="
		+ location['latitude'].toString() + "&lon=" + location['longitude'].toString();
	http.read(issPassOverheadEndpoint)
		.then((response) {
			Map result = JSON.decode(response);
			DateTime date = new DateTime.fromMillisecondsSinceEpoch(result['response'][0]['risetime']*1000);
			
			String output_text = "The ISS will pass overhead for " +
				result['response'][0]['duration'].toString() + " seconds on " +  date.toString();
			print(output_text);
		});
}

void peopleInSpace() {
	var peopleOnIssEndpoint = "http://api.open-notify.org/astros.json";
	http.read(peopleOnIssEndpoint)
		.then((response) {
			Map result = JSON.decode(response);
			print("The people currently in the space are:");
			for (var person in result['people']) {
				print(person['name'] + " on " + person['craft']);
			}
		});
}