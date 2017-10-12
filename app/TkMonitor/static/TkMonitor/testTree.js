var activePanels = 1;
var ws_socket;

function makeid(length) {
  var text = "";
  var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

  for (var i = 0; i < length; i++)
    text += possible.charAt(Math.floor(Math.random() * possible.length));

  return text;
}

var progressTimer,
progressbar = $( "#progressbar" ),
progressLabel = $( ".progress-label" ),
dialog = $( "#dialog" ).dialog({
  autoOpen: false,
  closeOnEscape: false,
  resizable: false,
  show: {
    effect: "fade",
    duration: 150
  },
  position: {
    my: "center center",
    at: "center center",
    of: $("#ltmondrawing"),
  },
});

progressbar.progressbar({
  value: false,
  change: function() {
    progressLabel.text( "Loading plot... " + progressbar.progressbar( "value" ) + "%" );
  }
});

$( "#start-date" ).datepicker({
  dateFormat: 'dd/mm/yy',
  minDate: new Date(firstFile*1000),
  maxDate: new Date(lastFile*1000),
  onClose: function(sdate){
    var date = new Date(sdate)
    console.log("Start: " + date.getTime()/1000)
  }
});
$( "#start-date" ).datepicker( "setDate", new Date((lastFile-7*86400)*1000) );

$( "#end-date" ).datepicker({
  dateFormat: 'dd/mm/yy',
  minDate: new Date(firstFile*1000),
  maxDate: new Date(lastFile*1000),
  onClose: function(sdate){
    var date = new Date(sdate)
    console.log("End: " + date.getTime()/1000)
  }
});
$( "#end-date" ).datepicker( "setDate", new Date(lastFile*1000) );

$( ".det-checkbox" ).checkboxradio({
  icon: false,
  padding: 0
});

$( "#sliding-controls1" ).slideDown();

$( "#slider1" ).data( 'nextblock', $( "#sliding-controls2" ) );
$( "#slider2" ).data( 'nextblock', $( "#sliding-controls3" ) );

$( "#slider1-add" ).data( 'slider', $( "#slider1" ) );
$( "#slider1-rm" ).data( 'slider', $( "#slider1" ) );
$( "#slider2-add" ).data( 'slider', $( "#slider2" ) );
$( "#slider2-rm" ).data( 'slider', $( "#slider2" ) );
$( "#slider3-add" ).data( 'slider', $( "#slider3" ) );
$( "#slider3-rm" ).data( 'slider', $( "#slider3" ) );


function activateSlider( slider ){
  console.log("Add clicked!")
  activePanels++;
  slider.slideDown();
  if( slider.data('nextblock') ){
    slider.data('nextblock').slideDown();
  }
}

function deactivateSlider( slider ){
  console.log("Rm clicked!")
  activePanels--;
  slider.slideUp();
  if( slider.data('nextblock') ){
    slider.data('nextblock').slideUp();
  }
}

$( ".slide-selector-icon-add" ).click( function(){
  console.log( "click! (add)" );
  activateSlider( $(this).data('slider') );
});

$( ".slide-selector-icon-rm" ).click( function(){
  console.log( "click! (rm)" );
  deactivateSlider( $(this).data('slider') );
});

var varNames = [
  ["Pedestal"      , "Pedestal"],
  ["Sigma"         , "Sigma"],
  ["RMS(Sigma)"    , "RMS"],
  ["Sigma_raw"     , "Sigma_raw"],
  ["RMS(Sigma_raw)", "RMS_raw"],
  ["Bad strips"    , "Nbad"],
  ["Masked strips" , "Nmasked"],
  ["Dead strips"   , "Ndead"],
  ["Noisy strips"  , "Nnoisy"]
]

var typeNames = [
  ["TkId", "tkid"],
  ["Plane", "plane"],
  ["Whole Tracker", "tracker"]
]

var sideNames = [
  ["X" , 0],
  ["Y" , 1],
  ["XY", 2],
]

function populateSelect(classname, array){

  if( !classname ){
    return false;
  } else {
    var elementList = document.getElementsByClassName( classname );

    for( var ielement = 0; ielement < elementList.length; ielement++ ){
      var element = elementList[ielement];
      for( var ichoice = 0; ichoice < array.length; ichoice++ ){
        var choice = array[ichoice];

        var opt = document.createElement('option');
        opt.value = choice[1];
        opt.innerHTML = choice[0];
        element.appendChild( opt );
      }
    }
  }

}

function makeRequest(){

  var requestId = makeid(12);
  console.log("Request id: " + requestId);

  var url = "/ltmon/getObj/";
  var var1, var2, var3, var4;
  var type1, type2, type3, type4;
  var num1, num2, num3, num4;
  var side1, side2, side3, side4;
  var mean1, mean2, mean3, mean4;
  var min1, min2, min3, min4;
  var max1, max2, max3, max4;

  var startdate = new Date($( "#start-date" ).datepicker("getDate"))
  var enddate   = new Date($( "#end-date" ).datepicker("getDate"))

  var1  = $('#var1').find(":selected").val();
  type1 = $('#type1').find(":selected").val();
  num1  = $('#num1').val();
  side1 = $('#side1').find(":selected").val();
  mean1 = $('#mean1').is(":checked");
  min1  = $('#min1').val();
  max1  = $('#max1').val();

  var jDat = {
    "requestId" : requestId,
    "startdate" : startdate.getTime()/1000,
    "enddate" : enddate.getTime()/1000,
    "nplots" : activePanels,
    "plot1" : {
      "var"  : var1,
      "type" : type1,
      "num"  : num1,
      "side" : side1,
      "mean" : mean1,
      "min"  : min1,
      "max"  : max1
    }
  }

  if( activePanels > 1 ){
    var2  = $('#var2').find(":selected").val();
    type2 = $('#type2').find(":selected").val();
    num2  = $('#num2').val();
    side2 = $('#side2').find(":selected").val();
    mean2 = $('#mean2').is(":checked");
    min2  = $('#min2').val();
    max2  = $('#max2').val();

    $.extend(jDat,
      {
        "plot2" : {
          "var"  : var2,
          "type" : type2,
          "num"  : num2,
          "side" : side2,
          "mean" : mean2,
          "min"  : min2,
          "max"  : max2
        }
      }
    );
  }
  if( activePanels > 2 ){
    var3  = $('#var3').find(":selected").val();
    type3 = $('#type3').find(":selected").val();
    num3  = $('#num3').val();
    side3 = $('#side3').find(":selected").val();
    mean3 = $('#mean3').is(":checked");
    min3  = $('#min3').val();
    max3  = $('#max3').val();

    $.extend(jDat,
      {
        "plot3" : {
          "var"  : var3,
          "type" : type3,
          "num"  : num3,
          "side" : side3,
          "mean" : mean3,
          "min"  : min3,
          "max"  : max3
        }
      }
    );
  }
  if( activePanels > 3 ){
    var4  = $('#var4').find(":selected").val();
    type4 = $('#type4').find(":selected").val();
    num4  = $('#num4').val();
    side4 = $('#side4').find(":selected").val();
    mean4 = $('#mean4').is(":checked");
    min4  = $('#min4').val();
    max4  = $('#max4').val();

    $.extend(jDat,
      {
        "plot4" : {
          "var"  : var4,
          "type" : type4,
          "num"  : num4,
          "side" : side4,
          "mean" : mean4,
          "min"  : min4,
          "max"  : max4
        }
      }
    );
  }

  var dat = JSON.stringify( jDat )
  alert("I am about to POST this:\n\n" + JSON.stringify(jDat, null, 2));

  var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
  console.log(ws_scheme + '://' + window.location.host + window.location.pathname + "getStatus/" + requestId);
  ws_socket = new WebSocket(ws_scheme + '://' + window.location.host + window.location.pathname + "getStatus/" + requestId);

  ws_socket.onopen = function() {
    // console.log("Sending...");
    ws_socket.send(dat);
    dialog.dialog("open");
  };

  ws_socket.onmessage = function(message) {
    var jMessage = JSON.parse(message.data)
    // console.log(jMessage.state);
    if( jMessage.state == "PROGRESS" ){
      // console.log(jMessage);
      progressbar.progressbar( "value", Math.round(100*jMessage.progress) );
    }
    if( jMessage.state == "SUCCESS" ){
      dialog.dialog("close");
      var obj = JSROOT.parse( jMessage.result );
      JSROOT.cleanup("ltmondrawing")
      JSROOT.draw("ltmondrawing", obj, "");
      ws_socket.onclose = function () {}; // disable onclose handler first
      ws_socket.close();
    }
  };

}



$( "#submit" ).click( function(){
  makeRequest();
} );


document.onload = populateSelect("vardropdown" , varNames);
document.onload = populateSelect("typedropdown" , typeNames);
document.onload = populateSelect("sidedropdown", sideNames);
