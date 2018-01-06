var five = require("johnny-five");
var board = new five.Board();

board.on("ready", () => {
	var accelerometer = new five.Accelerometer({
		controller: "ADXL335",
		pins: ["A0", "A1", "A2"],
		zeroV: [ 329.2, 321.2, 332.8 ]
	  });	
	
	accelerometer.on("change", function() {
		console.log(this.acceleration);
		
	  });
});
