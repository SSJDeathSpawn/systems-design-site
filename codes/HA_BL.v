module HA_BL(S, C, a, b);
    input a,b;
    output reg S,C;

    always @({a,b}) begin
        {S,C} = a + b;
    end
endmodule

module HA_BL_tb;
    reg a,b;
    wire S,C;
    integer i;

    HA_BL inst(S, C, a, b);

    initial begin
        $monitor("A=%0b|B=%0b|S=%0b|C=%0b", a,b,S,C);
        for(i=0;i<4;i=i+1) begin
            {a,b} = i;
            #10;
        end
    end

endmodule
    
