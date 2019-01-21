{% block content %}

			$('#voteModal').on('show.bs.modal', function(e) {
				var choice = $(e.relatedTarget).data('choice');
				var href = $(e.relatedTarget).data('href');
				$("#voteModal .modal-body").html('Are you sure you want to vote for choice <strong>' + choice + '</strong>?');
				$("#voteBtn").attr('href', href);
				
			});
		


{% endblock %}


