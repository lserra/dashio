queue()
    .defer(d3.json, "static/json/demographics/devices.json")
//    .defer(d3.json, "static/geojson/china_provinces_en.json")
    .await(makeGraphs);

//function makeGraphs(error, devicesJson, statesJson) {
function makeGraphs(error, devicesJson) {
	
	//Clean devicesJson data
	//Source:https://bl.ocks.org/zanarmstrong/ca0adb7e426c12c06a95
	var demographicsDevices = devicesJson;
    var dateFormat = d3.time.format("%Y-%m-%d");

	demographicsDevices.forEach(function(d) {
		d["date_device"] = dateFormat.parse(d["date_device"]);
		d["date_device"].setDate(1);
		d["qty"] = +d["qty"];
	});

	//Create a Crossfilter instance
	var ndx = crossfilter(demographicsDevices);

	//Define Dimensions
	var dateDim = ndx.dimension(function(d) { return d["date_device"]; });
	var brandDeviceDim = ndx.dimension(function(d) { return d["phone_brand_en"]; });
	var ageSegmentDim = ndx.dimension(function(d) { return d["age_segment"]; });
	var genderDim = ndx.dimension(function(d) { return d["gender"]; });
	var totalDevicesDim  = ndx.dimension(function(d) { return d["qty"]; });


	//Calculate metrics
	var all = ndx.groupAll();
	var numDevicesByDate = dateDim.group();
	var numDevicesByBrand = brandDeviceDim.group();
	var numDevicesByAge = ageSegmentDim.group();
	var numDevicesByGender = genderDim.group();

	var totalDevices = ndx.groupAll().reduceSum(function(d) {return d["qty"];});

	//Define values (to be used in charts)
	var max_gender = numDevicesByGender.top(1)[0].value;
	var minDate = dateDim.bottom(1)[0]["date_device"];
	var maxDate = dateDim.top(1)[0]["date_device"];

    //Charts
	var timeChart = dc.lineChart("#time-chart");
	var genderChart = dc.rowChart("#gender-chart");
	var deviceBrandChart = dc.rowChart("#device-brand-row-chart");
	var ageSegmentChart = dc.rowChart("#age-segment-row-chart");
	var numberDevicesND = dc.numberDisplay("#number-projects-nd");
	var totalDevicesND = dc.numberDisplay("#total-donations-nd");
//	var chChart = dc.geoChoroplethChart("#ch-chart");

	//Source:https://github.com/d3/d3-format
	numberDevicesND
		.formatNumber(d3.format(",.2r"))
		.valueAccessor(function(d){return d; })
		.group(all);

	totalDevicesND
		.formatNumber(d3.format("d"))
		.valueAccessor(function(d){return d; })
		.group(totalDevices)
		.formatNumber(d3.format(".3s"));

	timeChart
		.width(600)
		.height(160)
		.margins({top: 10, right: 50, bottom: 30, left: 50})
		.dimension(dateDim)
		.group(numDevicesByDate)
		.transitionDuration(500)
		.x(d3.time.scale().domain([minDate, maxDate]))
		.elasticY(true)
		.xAxisLabel("Period")
		.yAxis().ticks(4);

    genderChart
        .width(600)
        .height(160)
        .dimension(genderDim)
        .group(numDevicesByGender)
        .xAxis().ticks(4);

	deviceBrandChart
        .width(300)
        .height(250)
        .dimension(brandDeviceDim)
        .group(numDevicesByBrand)
        .xAxis().ticks(4);

	ageSegmentChart
		.width(300)
		.height(250)
        .dimension(ageSegmentDim)
        .group(numDevicesByAge)
        .xAxis().ticks(4);

//	chChart.width(1000)
//		.height(330)
//		.dimension(genderDim)
//		.group(numDevicesByGender)
//		.colors(["#E2F2FF", "#C4E4FF", "#9ED2FF", "#81C5FF", "#6BBAFF", "#51AEFF", "#36A2FF", "#1E96FF", "#0089FF", "#0061B5"])
//		.colorDomain([0, max_gender])
//		.overlayGeoJson(statesJson["features"], "state", function (d) {
//			return d.properties.name;
//		})
//		.projection(d3.geo.albersUsa()
//    				.scale(600)
//    				.translate([340, 150]))
//		.title(function (p) {
//			return "State: " + p["key"]
//					+ "\n"
//					+ "Total Donations: " + Math.round(p["value"]) + " $";
//		})

    dc.renderAll();

};