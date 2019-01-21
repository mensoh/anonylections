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

			$('#shareResult').change(function() {
				console.log('changed');
				$("#shareResultForm").submit();
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
		


{% endblock %}


