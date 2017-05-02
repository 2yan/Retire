from ryan_tools import * 



def apply_bracket( data_in, bracket ):
    data = pd.DataFrame(index= data_in.index )
    data['tax'] = 0
    for tax_rate in bracket.index:
        start = bracket.loc[tax_rate, 'start']
        end = bracket.loc[tax_rate, 'end']
        if end == 'inf':
            end = len(data)
        data.loc[start:end, 'tax'] = data.loc[start:end, 'tax'] + tax_rate
    return data['tax']

def gen_bracket( rates, end_vals ):
    bracket = pd.DataFrame( index = rates , columns  = ['start', 'end' ])
    bracket['end'] = end_vals
    i = 0
    last = None
    for index in bracket.index:
        if i == 0:
            bracket.loc[index, 'start'] = 0
            last = bracket.loc[index, 'end'] + 1
        if i > 0 :
            bracket.loc[index, 'start'] = last
            if bracket.loc[index, 'end'] != 'inf':
                last = bracket.loc[index, 'end'] + 1
        i = i + 1
    return bracket
            


def apply_social_security( data_in ):
    data = pd.DataFrame(index= data_in.index )
    data['tax'] = 0
    data.loc[0:127200,'tax'] = 0.062
    return data['tax']


data = pd.DataFrame(index = np.arange(1, 60001))

oregon_bracket = gen_bracket( [0.05, 0.07, 0.09, 0.099] ,[3350, 8400, 125000, 'inf']  )
federal_bracket = gen_bracket([0.01, 0.15, 0.25, 0.28, .33, .35, .396], [9275, 37650,91150,190150,413350,415050, 'inf'])
data['oregon_tax'] = apply_bracket( data, oregon_bracket )
data['federal_tax'] = apply_bracket( data, federal_bracket )
data['medicare'] = 0.0145
data['social_security'] = apply_social_security( data )



data['total'] = data.sum(axis = 1 )
for key, value in data.groupby('total').groups.items():
	print('bracket ', key)
	minimum = min(value)
	maximum = max(value )
	print('min ', minimum , 'max ', maximum  )
	print('paid in value', (maximum - minimum) * key )
	print('________')
