import requests
from json import loads,dumps
from api import politifact_allpeople
from api import politifact_api
from api import sunlight_api

def getMouthCoordinates(url):
    r = requests.get(
        'https://api.idolondemand.com/1/api/sync/detectfaces/v1',
        params = {
            'apikey': '31379774-e946-4bff-b26e-35e93ea7a67e',
            'url' : url,
        })
    try:
        face = loads(r.text)['face'][0]
        face['offset'] = face['left'] + face['width'], int(face['height'] * .3)
    except:
        return ''

    return face

def addAllPeopleToIdol():

    allPeople = politifact_allpeople.getAllPeople()
    count = 0
    
    for person in allPeople:
        first_name = person['first_name']
        last_name = person['last_name']
        name_slug = person['name_slug']

        print "trying " + first_name + " " + last_name
        if not first_name:
            continue
        elif not last_name:
            continue
        elif person['party']['party']=='None':
            continue
        elif person['party']['party']=='Organization':
            continue
        elif person['party']['party']=='Journalist':
            continue

        addTextToIdol(person)
    
def addTextToIdol(jsonDocument, index):
    try:
        print "------------------->adding text"
        
        r = requests.post("https://api.idolondemand.com/1/api/sync/addtotextindex/v1", 
        data = 
            {
                'apikey': '31379774-e946-4bff-b26e-35e93ea7a67e',
                'json': dumps({ 'document': jsonDocument }),
                'index': index
                
                # 'text': '*'
                # 'field_text': 'MATCH{Nancy Pelosi}:politician'
            })
        print r    
        print r.text
        print 'finished adding text'
    except Exception as e:
        print 'error'
        print e
        
def findRelatedStatements(FullName):
        r = requests.post("https://api.idolondemand.com/1/api/sync/findrelatedconcepts/v1",
            data = 
            {
                'apikey':'31379774-e946-4bff-b26e-35e93ea7a67e',
                'text': '*',
                'field_text': 'MATCH{' + FullName + '}:politician',
                'index': 'statements',
            })
        return r.text
            

def addDocumentToIdol(statements, politicianName):
    print "adding documents"
    
    documentArray = []
    
    for statement in statements:
        myDocument = {
            'reference':statement['url'],
            'title': statement['statement'],
            #parametric field
            'politician':'{0}'.format(politicianName),
            #index field
            'statement':statement['statement'],
            #extra fields
            'sentiment': 1,
        }
        documentArray.append(myDocument)
    
    json = documentArray
    addTextToIdol(json, 'statements')
    
    
def addPersonToIdol(person):
    print "adding person"
    print person
    print person['first_name'], person['last_name']
    id = sunlight_api.getID(person['first_name'].strip(),person['last_name'].strip())
    print id
    if id:
        print "getting results"
        results = politifact_api.randomStatements(person['name_slug'],1000)
        print "done getting results"
        if not results:
            print "no statements"
            return
            
        print len(results)
        print results
        addDocumentToIdol(results, '{0} {1}'.format(person['first_name'],person['last_name']))
        
        statements = [myResult['statement'] for myResult in results]
        
        image_url = sunlight_api.getImg(id)
        text_param = getMouthCoordinates(image_url)

        politicianDocument = {
        
            'reference':id,
            'title':'{0} {1}'.format(person['first_name'],person['last_name']),
            #parametric field
            'politician':'{0} {1}'.format(person['first_name'],person['last_name']),
            #index field
            'statement':statements,
            
            #extra json
            'party':person['party'],
            'image_url':image_url,
            #'source_url':person['statement_url'],
            'img_width':text_param['width'],
            'img_top':text_param['top'],
            'img_height':text_param['height'],
            'img_offset':text_param['offset'],
            'img_left':text_param['left'],
            
        }
        json = [ politicianDocument ]
        
        addTextToIdol(json, 'politicians')

# getRelatedConcepts('