$(document).ready(function() {
  $('#button').click(function() {
	  var url = "/services/algorithm1";
	  var params = "somevariable=somevalue&anothervariable=anothervalue";
	  var http = new XMLHttpRequest();

	  http.open("GET", url+"?"+params, true);
	  http.onreadystatechange = function()
	  {
	      if(http.readyState == 4 && http.status == 200) {
	          alert(http.responseText);
	      }
	  }
	  http.send(null);
  });
});