{% block content %}
		
		

			{% if election.ownedby.username == current_user.username and not result: %}
			$("#updateElection").on('click', function() {
       			 $("#electionform").submit();
    		});

			$('#deleteModal').on('show.bs.modal', function(e) {
				var choice = $(e.relatedTarget).data('choice');
				var href = $(e.relatedTarget).data('href');
				$("#deleteModal .modal-body").html('Are you sure you want to delete choice <strong>' + choice + '</strong>?');
				$("#deleteBtn").attr('href', href);
				
			});

			$('#electionStatusModal').on('show.bs.modal', function(e){ 
				var status = $(e.relatedTarget).data('status');
				var href = $(e.relatedTarget).data('href');
				if (status == 'open') {
					$("#electionStatusModal .modal-title").html('Open election');
					$("#electionStatusModal .modal-body").html('Are you sure you want to open this election to voting?');
					$("#electionStatusBtn").html('Open');
					$("#electionStatusBtn").attr('href', href);
				} else {
					$("#electionStatusModal .modal-title").html('Close election');
					$("#electionStatusModal .modal-body").html('Are you sure you want to close this election to voting?');
					$("#electionStatusBtn").html('Close');
					$("#electionStatusBtn").attr('href', href);
				}


			});
			{% endif %}


			var bar = document.getElementById("barChart").getContext('2d');
			var pie = document.getElementById("pieChart").getContext('2d');
			//fooo
			var barChart = new Chart(bar, {
			    type: 'bar',
			    data: {
			    	labels: [{% for choice in choices %}"{{choice.choice}}",{% endfor %}],					        
			        datasets: [{
			            label: '# of Votes',
			            data: [{% for choice in choices %}{{choice.votes|length}},{% endfor %}],

			            backgroundColor: [
			            	{% for color in colors %}
			                'rgba({{ color|join(',')}}, 1)',
			               	{% endfor %}
			            ],
			            borderColor: [
			            	
			            	{% for color in colors %}
			                'rgba({{ color|join(',')}}, 1)',
			               	{% endfor %}
			            ],
			            borderWidth: 1
			        }]
			    },
			    options: {
			        scales: {
			            yAxes: [{
			                ticks: {
			                    beginAtZero:true,
			                    callback: function (value) { if (Number.isInteger(value)) { return value; } },
                				stepSize: 1
			                }
			            }]
			        }
			    }
			});
			

			var pieChart = new Chart(pie, {
			    type: 'pie',
			    data: {
			    	labels: [{% for choice in choices %}"{{choice.choice}}",{% endfor %}],					        
			    	datasets: [{
			    		label: '# of Votes',
			    		data: [{% for choice in choices %}{{choice.votes|length}},{% endfor %}],
						backgroundColor: [
			            	{% for color in colors %}
			                'rgba({{ color|join(',')}}, 1)',
			               	{% endfor %}
			            ],
			            borderColor: [
			            	
			            	{% for color in colors %}
			                'rgba({{ color|join(',')}}, 1)',
			               	{% endfor %}
			            ],
			            borderWidth: 1
			    	}]
			    }

			});
		


{% endblock %}


