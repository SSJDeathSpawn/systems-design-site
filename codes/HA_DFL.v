module HA_DFL(S, C, a, b);
    input a,b;
    output S,C;
    
    assign S = a ^ b;
    assign C = a & b;

endmodule

module HA_DFL_tb;
    reg a,b;
    wire S,C;
    integer i;

    HA_DFL inst(S, C, a, b);

    initial begin
        $monitor("A=%0b|B=%0b|S=%0b|C=%0b", a,b,S,C);
        for(i=0;i<4;i=i+1) begin
            {a,b} = i;
            #10;
        end
    end

endmodule
