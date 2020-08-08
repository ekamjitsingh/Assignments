//see UFO-level-2's app.js for a fully commented javascript file
var button = d3.select("#filter-btn");
var inputField = d3.select("#datetime");
var tbody = d3.select("tbody");

function handleClick() {
  d3.event.preventDefault();
  var inputfieldvalue = inputField.property('value');
  tbody.selectAll("tr").remove();
  for (i=0; i<data.length; i++){
    if (data[i].datetime==inputfieldvalue || inputfieldvalue==""){
		console.log(data[i].city);
    	var row = tbody.append("tr");
		Object.entries(data[i]).forEach(function([key, value]) {
			console.log(key,value);
			var cell = row.append("td");
			cell.text(value);
		});
    }

}
}

for (i=0;i<data.length;i++){
	var row = tbody.append("tr");
	Object.entries(data[i]).forEach(function([key, value]) {
	var cell = row.append("td");
	cell.text(value);
})};

button.on("click", handleClick);