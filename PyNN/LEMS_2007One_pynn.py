'''
PyNN simulator compliant export for:

Components:
    RS (Type: izhikevich2007Cell:  v0=-0.06 (SI voltage) k=7.0E-7 (SI conductance_per_voltage) vr=-0.06 (SI voltage) vt=-0.04 (SI voltage) vpeak=0.035 (SI voltage) a=30.0 (SI per_time) b=-2.0E-9 (SI conductance) c=-0.05 (SI voltage) d=1.0E-10 (SI current) C=1.0E-10 (SI capacitance))
    RS_Iext (Type: pulseGenerator:  delay=0.0 (SI time) duration=0.52 (SI time) amplitude=1.0E-10 (SI current))
    net1 (Type: network)
    sim1 (Type: Simulation:  length=0.52 (SI time) step=1.0E-6 (SI time))


    This PyNN file has been generated by org.neuroml.export (see https://github.com/NeuroML/org.neuroml.export)
         org.neuroml.export  v1.5.1
         org.neuroml.model   v1.5.1
         jLEMS               v0.9.8.8

'''
# Main PyNN script for: net1

from pyNN.utility import get_simulator, init_logging
import numpy as np
import time
import sys

if not 'neuron' in sys.argv and not 'nest' in sys.argv and not 'brian' in sys.argv: 
    sys.argv.append('neuron')

if 'nrniv' in sys.argv:
    sys.argv.remove('nrniv')  # Might be there if run by nrniv -python
if '-python' in sys.argv:
    sys.argv.remove('-python')  # Might be there if run by nrniv -python
if '-mpi' in sys.argv:
    sys.argv.remove('-mpi')  # Might be there if run by nrniv -python

sim, options = get_simulator(("--plot-figure", "Plot the simulation results to a file.", {"action": "store_true"}),
                             ("--debug", "Print debugging information"))

if options.debug:
    init_logging(None, debug=True)


#   ---------------------------------------------
#   Cell parameters

cell_params_RS = {
     'v0':-60.0, 
     'k':7.0E-4, 
     'vr':-60.0, 
     'vt':-40.0, 
     'vpeak':35.0, 
     'a':0.030000001, 
     'b':-0.0019999999, 
     'c':-50.0, 
     'd':0.1, 
     'C':1.00000005E-4, 
} 

#   ---------------------------------------------
#   Populations


# Population: RS_pop, size: 1, component: RS
from RS_celldefinition import RSType
RS_pop = sim.Population(1, RSType(**cell_params_RS), label="pop_RS_pop")



#   ---------------------------------------------
#   Projections



#   ---------------------------------------------
#   Inputs

# Input: RS_Iext0 which is RS_Iext on cell 0 in RS_pop
from RS_Iext_inputdefinition import RS_Iext
RS_Iext0_RS_pop_0 = RS_Iext(  delay=0.0,  duration=520.0,  amplitude=0.1,  )
RS_Iext0_RS_pop_0.inject_into([RS_pop[0]])




#   ---------------------------------------------
#   Record values for plotting/saving

# Display: d1
# Line: RS v: Pop: RS_pop; cell: 0; value: RS_pop
RS_pop[[0]].record('soma(0.5).v', sampling_interval=0.001)

# Output file: exIzh.dat
# Column: v: Pop: RS_pop; cell: 0; value: v
RS_pop[[0]].record('soma(0.5).v', sampling_interval=0.001)


#   ---------------------------------------------
#   Run simulation

sim.tstop = 520.0
sim.setup(timestep=0.001)

sim_start = time.time()
print("Running a PyNN based simulation in %s for %sms (dt: %sms) on node %i"%(options.simulator.upper(), sim.tstop, sim.get_time_step(), sim.rank()))

sim.run(sim.tstop)

sim_end = time.time()
sim_time = sim_end - sim_start
print("Finished simulation in %f seconds (%f mins) on node %i"%(sim_time, sim_time/60.0, sim.rank()))


#   ---------------------------------------------
#   Saving data

if sim.rank() == 0:
    print("Saving to file: exIzh.dat (ref: of0)")
 
    # Column: t
    t = np.arange(0,(sim.tstop+(0.001/2))/1000.,0.001/1000.)
    of0_data = np.array([t])
    # Column: v: Pop: RS_pop; cell: 0; value: v
    RS_pop_segment =  RS_pop.get_data().segments[0]
    RS_pop_v_data = next((x for x in RS_pop_segment.analogsignalarrays if x.name == 'soma(0.5).v'), None)
    of0_v_v = [RS_pop_v_data.T[0].simplified] # 'simplified' converts to SI units
    of0_data = np.concatenate((of0_data, of0_v_v))
    np.savetxt('exIzh.dat', of0_data.T, delimiter='\t',fmt='%s')

    save_end = time.time()
    save_time = save_end - sim_end
    print("Saved data in %f seconds (%f mins) on node %i"%(save_time, save_time/60.0, sim.rank()))


#   ---------------------------------------------
#   Plotting data

if options.plot_figure:
    import matplotlib.pyplot as plt
    mp = 'Membrane potential (mV) '
    # Display: d1: RS v
    print("Display (d1): RS v")
    plt.figure("RS v")
    plt.xlabel('Time (ms)')
    ylabel = ''

    # Line: RS v: Pop: RS_pop; cell: 0; value: v
    segment =  RS_pop.get_data().segments[0]
    vm = next((x for x in segment.analogsignalarrays if x.name == 'soma(0.5).v'), None).T[0]
    if not mp in ylabel: ylabel += mp
    ts = [i*sim.get_time_step() for i in xrange(len(vm))]
    plt.plot(ts, vm, '-', label='RS v')
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()

sim.end()