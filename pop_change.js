/* pop_change.js */

/* Onload function which calls getPercentPopChangeData() 
and getTop10States() methods */
function onLoad() {
    getPercentPopChangeData();
    getTop10States();
}

/* Function which accepts a request URI, builds an XML http request, 
sends the request and handles the response by calling the response handler */
function sendXhr(requestURI, responseHandler) {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", requestURI);
    xhr.setRequestHeader("Accept", "application/json");
    xhr.onreadystatechange = responseHandler;
    xhr.send(null);
}

/* Function which sends an Xhr request to get the population change data from the csv file*/
function getPercentPopChangeData() {
    //var requestURI = 'https://s3-us-west-2.amazonaws.com/mycensusdata/visualize.csv';
    var requestURI = 'https://raw.githubusercontent.com/shreyasanand/data_analytics/master/processed_data/visualize.csv';
    sendXhr(requestURI, processPopChangeData);
}

/* Function which processes population change data from csv and represents it on a geo chart*/
function processPopChangeData() {
    if (this.readyState == 4) {
        var csv_data = this.responseText;
        var array_data = $.csv.toArrays(csv_data, {onParseValue: $.csv.hooks.castToScalar});
        var table_data = google.visualization.arrayToDataTable(array_data);
            
        var chart_options = {
            title: 'US states by population change: 2010-2011',
            width: 900,
            height: 600,
            region: "US",
            resolution: "provinces",
            legend: {text: 'Percentage Population Growth'}
        };
                
        var geochart = new google.visualization.GeoChart(document.getElementById('geochart_div'));
        geochart.draw(table_data, chart_options);
    } else {
        var error_msg = "Server not responding! Try again later";
        document.getElementById('geochart_div').innerHTML = error_msg;
    }
}

/* Function which sends an Xhr request to get the top 10 states data from the csv file*/
function getTop10States() {
    //var requestURI = 'https://s3-us-west-2.amazonaws.com/mycensusdata/top10.csv';
    var requestURI = 'https://raw.githubusercontent.com/shreyasanand/data_analytics/master/processed_data/top10.csv';
    sendXhr(requestURI, processTop10StatesData);
}

/* Function which processes top 10 states data from csv and represents it on a bar chart*/
function processTop10StatesData() {
    if (this.readyState == 4) {
        var csv_data = this.responseText;
        var array_data = $.csv.toArrays(csv_data, {onParseValue: $.csv.hooks.castToScalar});
        var table_data = google.visualization.arrayToDataTable(array_data);
            
        var chart_options = {
            title: 'Fastest Growing States: 2010-2011',
            hAxis: {title: 'US States', titleTextStyle: {color: 'green'}},
            vAxis: {title: 'Percentage Population Growth', titleTextStyle: {color: 'green'}}
        };

        var bar_chart = new google.visualization.ColumnChart(document.getElementById('barchart_div'));
        bar_chart.draw(table_data, chart_options);
                
    } else {
        var error_msg = "Server not responding! Try again later";
        document.getElementById('barchart_div').innerHTML = error_msg;
    }
}