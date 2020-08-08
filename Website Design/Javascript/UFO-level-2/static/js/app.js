var button = d3.select("#filter-btn");
var inputField = [d3.select("#datetime"), d3.select("#city"), d3.select("#state"), d3.select("#country"), d3.select("#shape")];
var tbody = d3.select("tbody");

function handleClick() {
	//the following code prevents the page from reloading using d3
  d3.event.preventDefault();
	// The following code finds the values in the input boxes
  var inputfieldvalue = [];
  for (i=0; i<inputField.length; i++){
	  inputfieldvalue.push(inputField[i].property('value'));
  }
  // The following code removes the old rows
  tbody.selectAll("tr").remove();
  // The following code finds the index locations of the entries that do NOT meet the users filter requests:
  var indexlocations=[]; //this variable will store the aforementioned index locations
  for (var i=0; i<data.length; i++){
	//the following code grabs the values of an individual object in the array named data
	var	 dictionaryvalues = Object.values(data[i]);
	//The following code loops through the five input field entries that are being filtered
	for (var j=0;j<inputField.length;j++) {
		// The following code checks if an input box is empty, if so it will skip filtering the objects by that input box
		if (inputfieldvalue[j]=="") {
			continue;
		} else if (dictionaryvalues[j]!=inputfieldvalue[j]){
			indexlocations.push(i);
			break;
			}}};
  for (i=0;i<data.length; i++) {
	  //the following code checks if an index location is not contained in the array named indexlocations
	  if (indexlocations.includes(i)==false) {
		  // The following code generates the individual table rows
		var row = tbody.append("tr");
		Object.entries(data[i]).forEach(function([key, value]) {
			var cell = row.append("td");
			cell.text(value);	
	  })}}};

for (i=0;i<data.length;i++){
	var row = tbody.append("tr");
	Object.entries(data[i]).forEach(function([key, value]) {
	var cell = row.append("td");
	cell.text(value);
})};

button.on("click", handleClick);