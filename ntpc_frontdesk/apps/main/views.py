from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from models import Application

# Create your views here.
@login_required
def index(request):
    return render_to_response('app.html')

@login_required
def case_print(request, application_id):
    application = Application.objects.get(id=application_id)

    required_forms = application.application_case.required_forms.all()
    handovered_forms = application.handovered_forms.all()

    handovered_ids = map(lambda x: x.form_type.id, handovered_forms)

    still_required_forms = filter(lambda x: x.id not in handovered_ids, required_forms)

    return render_to_response('case-print.html', {
        'application': application,
        'still_required_forms': still_required_forms
    })

