import dissasembler
import simulator

mydis = dissasembler.dissasembler()
output = {}
output = mydis.run()
mydis.print()

mysim = simulator.Simulator(**output)
mysim.run()