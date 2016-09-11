function init(e) {
		var button = document.getElementById('submit');
		button.addEventListener('click', requestData);
		
		function requestData() {
	  var codeNode = document.getElementById('code');
	  var code = codeNode.value;
	  $.ajax({
	    url: "http://115.159.121.127/stock/?code=" + code + "&cnt=10",
		success: function(rawData) {
		    var myChart = echarts.init(document.getElementById('chart'));
		}}
	   )
	}
}
document.addEventListener('DOMContentLoaded', init);