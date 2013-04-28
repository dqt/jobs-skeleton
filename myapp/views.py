from django.shortcuts import render
from jboard.myapp.forms import SearchForm
from lxml import etree


def etree_to_dict(t):
    d = {t.tag : map(etree_to_dict, t.iterchildren())}
    d.update(('@' + k, v) for k, v in t.attrib.iteritems())
    d['text'] = t.text
    return d

def home(request):
    return render(request, 'home.html')

def results(request):
    found = request.session.get('sesh')
    return render(request, 'results.html', {
            'found':found
            })

def search(request):
    if request.method == 'POST': # If the form has been submitted...
        form = SearchForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            jobtype = form.cleaned_data['jobtype']
            location = form.cleaned_data['location']
            tree = etree.parse("http://api.careerbuilder.com/v1/jobsearch?DeveloperKey=WDTX32V70CPWFS236BR0&Keywords="+str(jobtype)+"&Location="+str(location))
            cb = etree_to_dict(tree.getroot())
            numberfound = len(cb['ResponseJobSearch'][7]['Results'][1]['JobSearchResult'])
            found = []
            for j in cb['ResponseJobSearch'][7]['Results']:
                foundjob = {'company':j['JobSearchResult'][0]['text'],'url':j['JobSearchResult'][9]['text'],'location':j['JobSearchResult'][11]['text']}
                found.append(foundjob)

            request.session['sesh'] = found
            return render(request, 'optin.html', {
                'number':numberfound,
                }) # Redirect after POST
    else:
        form = SearchForm() # An unbound form

    return render(request, 'search.html', {
        'form': form,
    })
