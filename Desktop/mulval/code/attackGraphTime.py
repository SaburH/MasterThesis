from timeit import default_timer as timer
import os
import calculate,draw

start = timer()
os.system("cd ~/Desktop/ && graph_gen.sh segmentTest.P -v -p ")
end = timer()
print(end - start)


# calculate.calcumprob()
# draw.JsonGen()
