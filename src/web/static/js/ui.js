(function (window, document) {

  var layout   = document.getElementById('layout'),
      menu     = document.getElementById('menu'),
      menuLink = document.getElementById('menuLink');

  function toggleClass(element, className) {
    var classes = element.className.split(/\s+/),
        length = classes.length,
        i = 0;

    for(; i < length; i++) {
      if (classes[i] === className) {
        classes.splice(i, 1);
        break;
      }
    }
    // The className is not found
    if (length === classes.length) {
      classes.push(className);
    }

    element.className = classes.join(' ');
  }

  menuLink.onclick = function (e) {
    var active = 'active';

    e.preventDefault();
    toggleClass(layout, active);
    toggleClass(menu, active);
    toggleClass(menuLink, active);
  };

  function get_db_info() {
    $.getJSON( "/db_info", function(resp) {
      if (resp['db_size'] == 0) {
        $('#db_size').text(0);
        $('#db_created').text('Database not yet created.');
        $('#db_modified').text('Database not yet created.');
      } else {
        $('#db_size').text(resp['db_size']);
        $('#db_created').text(resp['db_created']);
        $('#db_modified').text(resp['db_modified']);
      }
    });
  }


  function draw_chart(id, title, d) {
    var data = new google.visualization.DataTable();
    data.addColumn('date', 'Time');
    data.addColumn('number', 'Spot Price');
    data.addColumn('number', 'Bid Price');
    data.addColumn('number', 'Ask Price');

    $.each(d, function( index, value ) {
      data.addRow([new Date(value[0]), parseFloat(value[1]), parseFloat(value[2]), parseFloat(value[3])]);
    });

    var TimeFormater = new google.visualization.DateFormat({ 
         pattern: "HH:mm" 
    }); 
    TimeFormater.format(data, 0);

    var options = {
      title: title,
      //curveType: 'function',
      legend: {position: 'none'}
    };

    var chart = new google.visualization.LineChart(document.getElementById(id));
    chart.draw(data, options);
  };

  function make_price_chart() {
      google.load('visualization', '1', {packages:['corechart']});
      google.setOnLoadCallback(drawCharts);
      function drawCharts() {
        $.getJSON( '/exchanges', function(resp) {
          $.each(resp['result'], function( index, name ) {
            $.getJSON( '/exchange/' + name, function(resp) {
              div_id = name + '_chart'
              $('#charts').append('<div id="' + div_id + '" class="pure-u-1-2"></div>' );
              draw_chart(div_id, name + ' BTC Prices', resp.result);
            });
          });
        });
      }
  };

  get_db_info();
  make_price_chart();

}(this, this.document));

