##Zad2 - Inkrementer i rotator
##
##Potrebno je projektovati modul koji u zavisnosti od kontrolnih signala
##ima mogucnost inkrementiranja, dekrementiranja, rotiranja u levo ili desno
##
##Potrebno je obezbediti mogucnost upisa podatka. Upis se obavlja aktiviranjem
##signala load. Za vreme aktivne vrednosti signala load izlaz se ne menja i jednak
##je signalima na data ulazu.

from myhdl import *

def counter(reset, clk, control, data, step, count):

    step_int = Signal(intbv(1)[4:])
    count_int = Signal(modbv(0, min = 0, max = 2**8))

    @always_seq(clk.posedge, reset=reset)
    def counter_logic():
        if control == 0:
            count_int.next = data
        elif control == 1:
            step_int.next= step
        elif control == 2:
            count_int.next = count_int + step_int
        elif control == 3:
            count_int.next = count_int - step_int
        
            

    @always_comb
    def output_logic():
        count.next = count_int

    return counter_logic, output_logic
