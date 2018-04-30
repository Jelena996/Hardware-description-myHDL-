from myhdl import *

def bin2bcd(reset,clk, bin_in,bcd):

    shift_reg = Signal(modbv(0, min = 0, max = 2**20))
    shift_cnt = Signal(intbv(7)[8:])
    state_t =  enum('Idle', 'Shift', 'Add')
    state = Signal(state_t.Idle)
    bin_int = Signal(intbv(0)[256:])

    @always_seq(clk.posedge, reset=reset)
    def bin2bcd_logic():
      if state==state_t.Idle:           
         if bin_int != bin_in:                       
            state.next = Signal(state_t.Shift)
            shift_reg.next=bin_in #podrayumijevamo da je ovdej cnt =7
            
            
      if state==state_t.Shift:
           if shift_cnt==0:
                shift_reg.next=shift_reg<<1
                state.next = Signal(state_t.Idle)
                shift_cnt.next=7
                bin_int.next=bin_in
           else:
             shift_reg.next=shift_reg<<1
             shift_cnt.next=shift_cnt-1
             state.next = Signal(state_t.Add)  
             
             
      if state==state_t.Add:
            correction=0  
            if shift_reg[20:16]>4:
              correction=correction+3*2**16 
            if shift_reg[16:12]>4:
              correction=correction+3*2**12
            if shift_reg[12:8]>4:
              correction=correction+3*2**8
            shift_reg.next=shift_reg+correction
            state.next = Signal(state_t.Shift)      
            
    @always_comb
    def output_logic():
      if bin_in==bin_int:
        bcd.next = shift_reg[19:8]

    return bin2bcd_logic, output_logic
      