import read_in_file
import drivers_and_passengers as dp
import search
import answer_value as aw
import heapq

name = 'i_o_files/big_1000_500'


N, M, D, U, drivers, users = read_in_file.parse_in(name + '.in')
state = dp.DriversAndPassengersState(drivers=drivers, passengers=users)

#distances = state.distance_user_driver(5)
#print (heapq.nsmallest(7, distances))


for i in range(10):
    final = search.hill_climbing(dp.DriversAndPassengers(state))
    outName = name + '_closest_' + str(i)
    final.write_out_file(outName  + '.out')
    print(outName, ' Value: ', aw.answer_value(outName, name), ' Distance: ', aw.get_total_driven_distance(outName, name))


#print('result: ', aw.answer_value('i_o_files/ricard/medium_100_50', 'i_o_files/medium_100_50'))

"""
name = 'i_o_files/medium_100_300'
for i in range(10):
    outName = name + '_closest_' + str(i)
    print(outName, ' Value: ', aw.answer_value(outName, name), ' Distance: ', aw.get_total_driven_distance(outName, name))
"""
#print('final value: ', final.goodness())
#print(final)
