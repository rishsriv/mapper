import webapp2
import csv
import jinja2
import os
from StringIO import StringIO
import logging
from fuzzywuzzy import process

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = False)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

def transform_state(state):
    states = ['Jammu and Kashmir', 'Kerala', 'Lakshadweep', 'Mizoram', 'Tripura', 'Goa', 'Delhi', 'Andaman and Nicobar Islands',
    'Himachal Pradesh', 'Maharashtra', 'Sikkim', 'Tamil Nadu', 'Nagaland', 'Manipur', 'Uttaranchal', 'Gujarat', 'West Bengal', 'Punjab',
    'Haryana', 'Karnataka', 'Meghalaya', 'Orissa', 'Odisha', 'Assam', 'Chhattisgarh', 'Madhya Pradesh', 'Uttar Pradesh', 'Andhra Pradesh', 
    'Jharkhand', 'Rajasthan', 'Arunachal Pradesh', 'Bihar', 'Uttarakhand', 'Pondicherry', 'Puducherry']
    if state in states:
        if state == 'Odisha':
            state = 'Orissa'
        elif state == 'Uttarakhand':
            state = 'Uttaranchal'
        return state
    else:
        new_state = process.extractOne(state, states)
        if new_state[0] == 'Odisha':
            new_state = ('Orissa', state[1])
        elif new_state[0] == 'Uttarakhand':
            new_state = ('Uttaranchal', state[1])
        if new_state[1] > 0.9:
            return new_state[0]
        else:
            return state

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(lambda app: jinja2.Jinja2(app=app,config={'environment_args':{'autoescape':False}}))


class Main(Handler):
    def get(self):
        self.render('index.html')

    def post(self):
        d_str = self.request.get('data').encode('ascii', 'xmlcharrefreplace')
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(d_str)
        delim = dialect.delimiter
        d = StringIO(d_str)
        reader = csv.reader(d, delimiter=delim)
        i = 0
        rows = []
        rows = [row for row in reader]
        header_row = xrange(len(rows[0]))
        self.render('check.html', header_row=header_row, rows=rows, data=d_str, num_f = len(header_row), delim=delim)

class Proc(Handler):
    def get(self):
        self.redirect('/')
    def post(self):
        data = self.request.get('data').encode('ascii', 'backslashreplace')
        num_f = int(self.request.get('num_f'))
        features = []
        state_index = int(self.request.get('state'))
        value_index = int(self.request.get('value'))
        has_header = self.request.get('has_header')
        delim = str(self.request.get('delim'))
        d = StringIO(data)
        reader = csv.reader(d, delimiter=delim)
        rows = []
        map_type = self.request.get('map_type')
        if map_type == 'state':
            region = self.request.get('country')
        elif map_type == 'country':
            region = self.request.get('region')
        countries = ['DZ', 'EG', 'EH', 'LY', 'MA', 'SD', 'TN', 'BF', 'BJ', 'CI', 'CV', 'GH', 'GM', 'GN', 'GW', 'LR', 'ML', 
        'MR', 'NE', 'NG', 'SH', 'SL', 'SN', 'TG', 'AO', 'CD', 'ZR', 'CF', 'CG', 'CM', 'GA', 'GQ', 'ST', 'TD', 'BI', 'DJ', 
        'ER', 'ET', 'KE', 'KM', 'MG', 'MU', 'MW', 'MZ', 'RE', 'RW', 'SC', 'SO', 'TZ', 'UG', 'YT', 'ZM', 'ZW', 'BW', 'LS', 
        'NA', 'SZ', 'ZA', 'GG', 'JE', 'AX', 'DK', 'EE', 'FI', 'FO', 'GB', 'IE', 'IM', 'IS', 'LT', 'LV', 'NO', 'SE', 'SJ', 
        'AT', 'BE', 'CH', 'DE', 'DD', 'FR', 'FX', 'LI', 'LU', 'MC', 'NL', 'BG', 'BY', 'CZ', 'HU', 'MD', 'PL', 'RO', 'RU', 
        'SU', 'SK', 'UA', 'AD', 'AL', 'BA', 'ES', 'GI', 'GR', 'HR', 'IT', 'ME', 'MK', 'MT', 'CS', 'RS', 'PT', 'SI', 'SM', 
        'VA', 'YU', 'BM', 'CA', 'GL', 'PM', 'US', 'AG', 'AI', 'AN', 'AW', 'BB', 'BL', 'BS', 'CU', 'DM', 'DO', 'GD', 'GP', 
        'HT', 'JM', 'KN', 'KY', 'LC', 'MF', 'MQ', 'MS', 'PR', 'TC', 'TT', 'VC', 'VG', 'VI', 'BZ', 'CR', 'GT', 'HN', 'MX', 
        'NI', 'PA', 'SV', 'AR', 'BO', 'BR', 'CL', 'CO', 'EC', 'FK', 'GF', 'GY', 'PE', 'PY', 'SR', 'UY', 'VE', 'TM', 'TJ', 
        'KG', 'KZ', 'UZ', 'CN', 'HK', 'JP', 'KP', 'KR', 'MN', 'MO', 'TW', 'AF', 'BD', 'BT', 'IN', 'IR', 'LK', 'MV', 'NP', 
        'PK', 'BN', 'ID', 'KH', 'LA', 'MM', 'BU', 'MY', 'PH', 'SG', 'TH', 'TL', 'TP', 'VN', 'AE', 'AM', 'AZ', 'BH', 'CY', 
        'GE', 'IL', 'IQ', 'JO', 'KW', 'LB', 'OM', 'PS', 'QA', 'SA', 'NT', 'SY', 'TR', 'YE', 'YD', 'AU', 'NF', 'NZ', 'FJ', 
        'NC', 'PG', 'SB', 'VU', 'FM', 'GU', 'KI', 'MH', 'MP', 'NR', 'PW', 'AS', 'CK', 'NU', 'PF', 'PN', 'TK', 'TO', 'TV', 'WF', 'WS']
        for row in reader:
            if region == 'IN':
                state = transform_state(row[state_index])
            else:
            	state = row[state_index]
            val = row[value_index]
            if val not in ['', 'N/A', 'NA', 'n/a', 'na']:
                a = (state, val)
                rows.append(a)
        if has_header == 'True':
            rows = rows[1:]
        def state(i):
            i = i.lower()
            if i == 'uttaranchal':
                return 'IN-UT'
            if 'taiwan' in i:
                return 'Taiwan'
            elif 'macau' in i:
                return 'Macau'
            elif 'china' in i:
                return 'China'
            elif 'congo' in i and 'democratic' not in i:
                return 'Congo'
            elif 'ivoire' in i:
                return 'Ivory Coast'
            elif 'burma' in i:
                return 'Myanmar'
            else:
                return i.replace("'", "&quot;").replace('flag ', '')
        rows = [(i[0].replace("'", "&quot;"), float(i[1].replace(',', '').replace('$', '')), state(i[0])) for i in rows]
        max_value = self.request.get('max_value')
        if max_value == '' or max_value == None:
            max_value = max([x[1] for x in rows])
        logging.info(max_value)
        min_value = self.request.get('min_value')
        if min_value == '' or min_value == None:
            min_value = min([x[1] for x in rows])
        
        title = self.request.get('title')
        attrib = self.request.get('attrib')
        domain = 'IN'
        if region in countries:
            resolution = 'provinces'
        else:
            resolution = 'countries'
        colors = ['green']
        interactive = True
        if region != '001':
            if interactive:
                self.render('map.html', rows = rows, title=title, attrib=attrib, region = region, domain = domain, resolution = resolution, 
                    colors = colors, interactive = True, min_value = min_value, max_value = max_value)
            else:
                self.render('map.html', rows = rows, title=title, attrib=attrib, region = region, domain = domain, resolution = resolution, 
                    colors = colors, min_value = min_value, max_value = max_value)
        else:
            if interactive:
                self.render('map.html', rows = rows, title=title, attrib=attrib, domain = domain, resolution = resolution, 
                    colors = colors, interactive = True, min_value = min_value, max_value = max_value)
            else:
                self.render('map.html', rows = rows, title=title, attrib=attrib, domain = domain, resolution = resolution, 
                    colors = colors, min_value = min_value, max_value = max_value)

app = webapp2.WSGIApplication([
    ('/', Main),
    ('/process', Proc)
], debug=True)