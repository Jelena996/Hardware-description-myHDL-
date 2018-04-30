from myhdl import *
from counter import counter

def test_counter():

    clk = Signal(bool(0))
    reset = ResetSignal(1, active = 0, async = True)
    control = Signal(intbv(0)[2:])
    data = Signal(intbv(0)[8:])
    step = Signal(intbv(1)[4:])
    count = Signal(modbv(0, min = 0, max = 2**8))
    cnt_inst = counter(reset, clk, control, data, step, count)
    

    half_clk_period = 1
    clk_period = 2*half_clk_period

    @always(delay(half_clk_period))
    def clk_gen():
        clk.next = not clk

    @instance
    def stimulus():
        reset.next = 0
        yield delay(clk_period)
        reset.next = 1
        yield delay(clk_period)
        reset.next = 1
        step.next=3
        data.next = 0b11010010
        yield delay(clk_period)
        control.next = 1
        yield delay(3*clk_period)
        control.next = 2
        yield delay(3*clk_period)
        control.next = 2
        yield delay(3*clk_period)
        control.next = 3
        yield delay(3*clk_period)
        control.next = 3
        yield delay(3*clk_period)

        raise StopSimulation

    return cnt_inst, clk_gen, stimulus

tb = traceSignals(test_counter)
Simulation(tb).run()
        
        
