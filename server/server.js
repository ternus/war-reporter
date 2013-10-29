Datapoints = new Meteor.Collection("data");

Datapoints.getHostnames = function() {
    var dpts = Datapoints.find({}, { hostname: 1 }).fetch();
    var darr = _.uniq(dpts, false, function(d) {return d.hostname});
    return _.pluck(darr, 'hostname');
}

Datapoints.getPlugins = function(hostname) {
    var dpt = Datapoints.findOne({hostname: hostname}, { hostname: 1, plugins: 1 });
    return dpt.plugins;
}

Datapoints.getPluginDatapoints = function(hostname, plugin) {
    var dpt = Datapoints.findOne({hostname: hostname});
    return dpt[plugin];
}

function isNumber(n) {
  return !isNaN(parseFloat(n)) && isFinite(n);
}

if (Meteor.isClient) {
    Meteor.defer(function() {
	Template.datapoints.latest = function() {
	    return Datapoints.findOne({}, { sort: { time: -1} } );
	}
    });  
  
    Template.charts.hosts = function() {
	var darr = [];
	Datapoints.getHostnames().forEach(function(hostname) {
	    darr.push({ hostname: hostname, plugins: Datapoints.getPlugins(hostname)});
	});
	return darr;
    }

    Template.hostchart.datapoints = function(hostname, plugin) {
	var ret = Datapoints.getPluginDatapoints(hostname, plugin);
	return Object.keys(ret);
    }

    Template.hostchart.isNumeric = function(hostname, plugin, dpt_name) {
	return isNumber(Datapoints.getPluginDatapoints(hostname, plugin)[dpt_name]);
    }

    Template.hostchart.plotData = function(hostname, plugin, dpt_name) {
	Meteor.defer(function() {
	// console.log("plotting... " + hostname + " " + plugin + " " + dpt_name); 
	datapoints = getData(hostname, plugin, dpt_name);
	console.log(datapoints);
	// console.log($('#dpt_'+hostname.replace(/\./g,'\\.')+'_'+plugin+'_'+dpt_name).length);
	//console.log($('#dpt_'+hostname.replace('.','\\.')+'_'+plugin+'_'+dpt_name));
	$.plot($('#dpt_'+hostname.replace(/\./g,'\\.')+'_'+plugin+'_'+dpt_name), [datapoints], 
	       { xaxis: {
		   show: true,
		   mode: "time",
		   timeformat: "%H:%M:%S"
		   }
	       }
	      );
	});
    }

    getData = function(hostname, plugin, datapoint_spec) {
	var data = Datapoints.find({hostname: hostname}, {sort: {time: -1}}).fetch();
	var dpts = [];
	for(dpt in data) {
	    dpts.push([data[dpt].time * 1000.0, parseFloat(data[dpt][plugin][datapoint_spec])]);
	}
	return dpts;
    };
	
    getTwoLayerData = function(hostname, plugin, datapoint_spec, second_spec) {
	var data = Datapoints.find({hostname: hostname}, {sort: {time: -1}}).fetch();
	var dpts = [];
	for(dpt in data) {
	    dpts.push([data[dpt].time, data[dpt][plugin][datapoint_spec][second_spec]]);
	}
	return dpts;
    };
    // Meteor.defer(function() {
    // 	Datapoints.getHostnames().forEach(function(hostname) {
    // 	    $('#charts').append("<div class='host' id='host-"+hostname+"'></div>");
    // 	});
    // });

}

if (Meteor.isServer) {

    // fibers = Npm.require("fibers"); 
    //connect = Npm.require("connect");

  Meteor.startup(function () {
      console.log("starting");
      HTTP.publish(Datapoints, function(data) {
      console.log("Got datapoint from "+data.hostname);
      });
      console.log("published");
  });
}
