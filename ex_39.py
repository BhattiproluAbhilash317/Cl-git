# Add states and Abbr
states= {
 'Florida':'FL',
 'Oregon':'OR',
 'California':'CA',
 'Illinois':'IL'
}
print states

#Add some more cities
cities={
 'CA':'San Francisco',
 'FL':'Jacksonville'
}
#Add more states
states['Newyork']="NY"
states['Tennessey']="TN"
print cities
#Add more cities
cities['NY']="New York",
cities['IL']="Chicago",
cities['OR']="Portland"
print cities
#print some cities
print"OR city has:", cities['OR']
print "NY has :",cities['NY']
#print some states

print "New York Abbr is:", states['Newyork']
print "California is abbr as:", states['California']

print "Michigan has cities:", cities[states["Florida"]]

