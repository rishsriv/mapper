from fuzzywuzzy import process

def transform_state(state):
	states = ['Jammu and Kashmir', 'Kerala', 'Lakshadweep', 'Mizoram', 'Tripura', 'Goa', 'Delhi', 'Andaman and Nicobar Islands',
	'Himachal Pradesh', 'Maharashtra', 'Sikkim', 'Tamil Nadu', 'Nagaland', 'Manipur', 'Uttaranchal', 'Gujarat', 'West Bengal', 'Punjab',
	'Haryana', 'Karnataka', 'Meghalaya', 'Orissa', 'Assam', 'Chhattisgarh', 'Madhya Pradesh', 'Uttar Pradesh', 'Andhra Pradesh', 
	'Jharkhand', 'Rajasthan', 'Arunachal Pradesh' 'Bihar']
	state = process.extractOne(state, states)
	print state
	if state[1] > 0.8:
		return state[0]
	else:
		return False

a = transform_state('Uttarakhand')
print a