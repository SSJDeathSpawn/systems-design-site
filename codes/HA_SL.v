module HA_SL(S, C, a, b);
    input a, b;
    output S, C;

    xor xor1(S, a, b);
    and and1(C, a, b);

endmodule

module HA_SL_tb;
    reg a,b;
    wire S,C;
    integer i;

    HA_SL inst(S, C, a, b);

    initial begin
        $monitor("A=%0b|B=%0b|S=%0b|C=%0b", a,b,S,C);
        for(i=0;i<4;i=i+1) begin
            {a,b} = i;
            #10;
        end
    end

endmodule

