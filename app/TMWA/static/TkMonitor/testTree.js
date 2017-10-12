$( "#start-date" ).datepicker();
$( "#end-date" ).datepicker();
$( "#submit" ).button({
  icon: "ui-icon-gear"
});

function makeRequest(){
  var url = "/ltmon/getObj/";

  var tkid = $( "#tkid" ).val();
  console.log(tkid);
  var dat = JSON.stringify(
    {
      "var"  : "Pedestal",
      "TkId" : tkid,
      "side" : "0"
    }
  );
  // alert("I am about to POST this:\n\n" + dat);

  var dataToPlot;
  $.post(
    url,
    dat,
    function(data) {
      dataToPlot = data;
      var obj = JSROOT.parse( dataToPlot );
      JSROOT.redraw("ltmondrawing", obj, "colz");
    }
  );
}

$( "#submit" ).click( function(){
  makeRequest();
} );
