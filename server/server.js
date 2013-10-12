Datapoints = new Meteor.Collection("data");

Datapoints.getHostnames = function() {
    return Datapoints.find({}, { hostname: 1 }).fetch();
}

if (Meteor.isClient) {
    Template.datapoints.latest = function() {
	var d = Datapoints.find({}, { sort: { time: -1} } ).fetch();
	// console.log(d);
	// d[0].time = Date(d[0].time);
	return d[0];
    }
    getData = function(hostname, plugin, datapoint_spec) {
	var data = Datapoints.find({hostname: hostname}, {sort: {time: -1}}).fetch();
	var dpts = [];
	for(dpt in data) {
	    dpts.push([data[dpt].time, data[dpt][plugin][datapoint_spec]]);
	}
	return dpts;
    };
	
}

if (Meteor.isServer) {

    // fibers = Npm.require("fibers"); 
    //connect = Npm.require("connect");

  Meteor.startup(function () {
      console.log("starting");
      HTTP.publish(Datapoints);
      console.log("published");
  });
}
