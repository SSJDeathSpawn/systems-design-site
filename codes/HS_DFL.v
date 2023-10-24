module HS_DFL(B,D,a,b);
    input a,b;
    output B,D;

    assign D = a ^ b;
    assign B = (~a) & b;
    
endmodule

module HS_DFL_tb;
    reg a,b;
    wire B,D;
    integer i;

    HS_DFL inst(B,D,a,b);
    
    initial begin
        $monitor("A=%0b|B=%0b|Borrow=%0b|Diff=%0b", a,b,B,D);
        for(i=0;i<4;i=i+1) begin
            {a,b} = i;
            #10;
        end
    end
endmodule
