from myhdl import * 
from bin2bcd import bin2bcd


def test_bin2bcd():
    clk = Signal(bool(0))
    bin_in = Signal(intbv(0)[8:])
    reset = ResetSignal(1, active = 0, async = True)
    bcd = Signal(modbv(0, min = 0, max = 2**12))
    bin2bcd_inst = bin2bcd(reset,clk, bin_in,bcd)
    half_clk_period = 1
    clk_period = 2*half_clk_period
    @always(delay(half_clk_period))
    def clk_gen():
        clk.next = not clk    
    
    @instance   
    def stimulus():
        reset.next = 0
        bin_in.next = 0b10110010
        yield delay(clk_period)
        reset.next = 1
        yield delay(clk_period)
        reset.next = 1
       
        yield delay(clk_period)
        
        yield delay(3*clk_period)
        yield delay(3*clk_period)
        yield delay(3*clk_period)
        yield delay(3*clk_period)
        yield delay(3*clk_period)
        yield delay(3*clk_period)
        yield delay(3*clk_period)
        yield delay(3*clk_period)
        yield delay(3*clk_period)
        raise StopSimulation    
    return bin2bcd_inst, clk_gen, stimulus
tb = traceSignals(test_bin2bcd)
Simulation(tb).run()