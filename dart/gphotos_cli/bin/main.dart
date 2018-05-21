import 'dart:io';
import 'dart:async';
import 'dart:convert';
import 'package:args/args.dart';
import 'package:http/http.dart' as http;
import 'package:googleapis_auth/auth_io.dart';
import 'package:googleapis_auth/src/auth_http_utils.dart';

File configFile = new File("config.json");
File cache = new File("cache.json");
ArgResults argResults;

var id = new ClientId("69729799135-ec3430qn9pur3o53v78l6munpghb1e28.apps.googleusercontent.com", "vdEL1N13UFnQ5q0XnmCKm7CR");
var scopes = [
	"https://www.googleapis.com/auth/photoslibrary.readonly",
	"https://www.googleapis.com/auth/photoslibrary.appendonly",
	"https://www.googleapis.com/auth/photoslibrary.readonly.appcreateddata",
	"https://www.googleapis.com/auth/photoslibrary.sharing"
];

// The authenticated http client to make the calls to the Google Photos Library API
var authClient;
// Base Client
var baseClient = new http.Client();

var albumId = null;

void prompt(String url) {
  print("Please go to the following URL and grant access:");
  print("  => $url");
  print("");
}

// Initial setup
// This will obtain credentials from the user to make calls to the API.
// This is done only once.
void setup() {
	var client = new http.Client();
	obtainAccessCredentialsViaUserConsent(id, scopes, client, prompt)
	    .then((AccessCredentials credentials) {
	    	// Saving the credentials in the config file [config.json]
	    	var cred = {
	    		"token": credentials.accessToken.data,
	    		"expiry": credentials.accessToken.expiry.toString(),
	    		"type": credentials.accessToken.type,
	    		"refreshToken": credentials.refreshToken,
	    		"scope": credentials.scopes
	    	};
	    	configFile.writeAsString(JSON.encode(cred));
		  client.close();
	});
}

void createAlbum(String albumTitle) {
	var payload = {
		"album": {
			"title": albumTitle
		}
	};
	authClient.post(
		"https://photoslibrary.googleapis.com/v1/albums",
		body: JSON.encode(payload))
	.then((response) {
		Map data = JSON.decode(response.body);
		print(response.body);
		if(response.statusCode == 200) {
			print("Successfully created the album: ${data['title']}");
			print("Open the album at: ${data['productUrl']}");
		}
		cache.writeAsString(JSON.encode(data));
	});
}

// Initializing the authClient
void init() async {
	// Read the creadentials from the configuration file
	var configJson = JSON.decode(await configFile.readAsString());
	// Creating accesstokens, refreshtoken and scopes from the configs
	var accessToken = new AccessToken(configJson['type'], configJson['token'], DateTime.parse(configJson['expiry']));
	String refreshToken = configJson['refreshToken'];
	List<String> scopes = configJson['scope'];
	// Creating the AccessCredentials 
	var credentials = new AccessCredentials(accessToken, refreshToken, scopes);
	// Getting an authenicated client from the credentials
	// This will automatically refresh 
	authClient = new AutoRefreshingClient(baseClient, id, credentials);
}

// For uploading raw bytes 
void upload(List<String> files) async {
	var tokens = new List<String>();
	var headers = new Map<String, String>();
	headers = {
		"Content-type": "application/octet-stream"
	};
	print("Uploading");
	await Future.wait(files.map((file) async {
		var bytes = await new File(file).readAsBytes();
		return authClient.post(
			"https://photoslibrary.googleapis.com/v1/uploads",
			body: bytes,
			headers: headers
		);
	}))
	.then((responses) {
		for (var res in responses) {
			tokens.add(res.body);
		}
		createItem(tokens);
	});
}

// For adding the item to the albums
void createItem(uploadTokens) async {
	Map currentalbum = JSON.decode(await cache.readAsString());

	var payload = {
		"albumId": currentalbum['id'],
	  	"newMediaItems": []
	};
	var items = new List();
	for (var token in uploadTokens) {
		items.add({ 
			"simpleMediaItem": {
		        "uploadToken": token
		      }
		});
	}
	payload['newMediaItems'] = items;

	authClient.post(
		"https://photoslibrary.googleapis.com/v1/mediaItems:batchCreate",
		body: JSON.encode(payload)
	).then((response) {
		print(response.body);
		Map data = JSON.decode(response.body);
		List result = data['newMediaItemResults'];
		// TODO
	});
}

void close() {
	authClient.close();
}

void main(List<String> arguments) async {

	final parser = new ArgParser();
	argResults = parser.parse(arguments);
	List<String> res = argResults.rest;
	await init();
	if(res.length > 0) {
		switch(res[0]) {
			case 'setup':
				print("Setup");
				setup();
				break;
			case 'upload':
				var count = res.length - 1;
				var files = new List<String>.generate(count, (int index) => res[index+1]);
				await upload(files);
				break;
			case 'new':
				if (res.length == 2) {
					print("Album name: ${res[1]}");
					createAlbum(res[1]);
				} else {
					print("Specify the album name");
				}
				break;
			default:
				print("Unknown command");
		}
	} else {
		print("GPhotos CLI - A command line tool for uploading images to the Google Photos library");
		print("Usage");
		print("To setup the tool, you have to signin with the Google account");
		print(r"$ dart bin/main.dart setup");
		print("To add new album");
		print(r"$ dart bin/main.dart new <album name>");
		print("To upload the images");
		print(r"$ dart bin/main.dart upload <files>");
	}
	close();
}