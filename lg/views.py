# Create your views here.
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.core.mail import EmailMultiAlternatives, get_connection
from django.http import HttpResponseRedirect
from django.conf import settings

from mainsite.models import Setting
from lg.forms import LivingGroupForm
from lg.models import LivingGroup


def lgform(request):    
    if request.method == 'POST':
        form = LivingGroupForm(request.POST)
        if form.is_valid():
            lg = form.save(commit = False)
            lg.year = Setting.objects.get(tag="tnq_year").value
            lg.save()
            
            sendemail(lg)
            
            return HttpResponseRedirect(reverse('lg_success'))
    else:
        form = LivingGroupForm()
    
    context = {'form':form}
    context.update(csrf(request))
    
    return render_to_response('tnq_site/lg/lg_form.html', context)
    

plain_message = """Dear %s,
Thank you for signing up for a portrait for your living group. Just as a confirmation for your records, here is the information we received:

Living group name: %s
Contact phone number: %s

First time choice: %s
Second time choice: %s
Third time choice: %s
Alternative time choice: %s

Location: %s
Comments: %s

We will be contacting you in the next few days to schedule the portrait. Once we finalize the date and time, please make sure to remind the other members of your group multiple time.

While getting the portrait in the yearbook is free, consider these optional packages:
* A full page dedicated to your group with a diagram labeling every member for %s
* Your group's logo or crest next to your photo for %s
* A digital copy of your photo for %s
Let us know if you would like to pursue any of these options. Payment can be made by SAO account transfer, cash, or check made out to "MIT Technique" and can be given to the photographer on the day of your portrait.

Please don't hesitate to email us at tnq-lg@mit.edu if you have any questions.
Sincerely,
The Staff of Technique %s
"""

html_message = """<div><b><font size='4'>Dear %s,</font></b></div>
	<div>
		Thank you for signing up for a portrait for your living group. Just as a confirmation for your records, here is the information we received:
	</div>
	<div>
		<br>
	</div>
	<div>
		<b>Living group name:</b> %s
	</div>
	<div>
		<b>Contact phone number:</b> %s
	</div>
	<div>
		<br>
	</div>
	<div>
		<b>First time choice:</b> %s
	</div>
	<div>
		<b>Second time choice:</b> %s
	</div>
	<div>
		<b>Third time choice:</b> %s
	</div>
	<div>
		<b>Alternative time choice:</b> %s
	</div>
	<div>
		<br>
	</div>
	<div>
		<b>Location:</b> %s
	</div>
	<div>
		<b>Comments:</b> %s
	</div>
	<div>
		<br>
	</div>
	<div>
		We will be contacting you in the next few days to schedule the portrait. Once we finalize the date and time, please <b>make sure to remind the other members of your group</b> multiple times.
	</div>
	<div>
		<br>
	</div>
	<div>
		While getting the portrait in the yearbook is free, consider these optional packages:
	</div>
	<div>
		<ul>
			<li>A full page dedicated to your group with a diagram labeling every member for $%s<br>
			</li>
			<li>Your group&#39;s logo or crest next to your photo for $%s<br>
			</li>
			<li>A digital copy of your photo for $%s<br>
			</li>
		</ul>
	</div>
	<div>
		Let us know if you would like to pursue any of these options. Payment can be made by SAO account transfer, cash, or check made out to &quot;MIT Technique&quot; and can be given to the photographer on the day of your portrait.
	</div>
	<div>
		<br>
	</div>
	<div>
		Please don&#39;t hesitate to email us at <a href="mailto:tnq-lg@mit.edu" target="_blank">tnq-lg@mit.edu</a> if you have any questions.
	</div>
	<div>
		<br>
	</div>
	<div>
		Sincerely,
	</div>
	<div>
		The Staff of <i>Technique %s</i>
	</div>"""

def sendemail(lg):
    connection = get_connection()
    connection.open()
    
    tf = lambda x: x.__format__("%a, %b %d at %I:%M %p")
    
    subject = "Portrait of %s for the %s yearbook" % (lg.lg_name, lg.year)
    
    plugin = (lg.rep_name,
              lg.lg_name,
              lg.rep_phone, 
              tf(lg.first_choice), 
              tf(lg.second_choice), 
              tf(lg.third_choice), 
              lg.alternative_choice, 
              lg.location, 
              lg.comments, 
              Setting.objects.get(tag="lg_ghostie_cost").value,
              Setting.objects.get(tag="lg_crest_cost").value,
              Setting.objects.get(tag="lg_file_cost").value,
              lg.year)
    
    text_email = (plain_message % plugin).encode('utf-8')
    html_email = (html_message % plugin).encode('utf-8')
    
    headers = {}
    headers['To'] = lg.rep_name + " <" + lg.rep_email + ">, " + "MIT Technique <tnq-lg@mit.edu>"
    headers['From'] = "MIT Technique <tnq-lg@mit.edu>"
    message = EmailMultiAlternatives(subject, text_email, "tnq-lg@mit.edu", [lg.rep_email, "tnq-lg@mit.edu"], connection=connection, headers = headers)
    message.attach_alternative(html_email,"text/html");
        
    while message.send() < 1:
        connection = get_connection()
        connection.open()
                                
    connection.close()