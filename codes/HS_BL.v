module HS_BL(B,D,a,b);
    input a,b;
    output B,D;
    
    always @({a,b}) begin
        {B,D} = a - b;
    end
endmodule

module HS_BL_tb;
    reg a,b;
    wire B,D;
    integer i;

    HS_BL inst(B,D,a,b);
    
    initial begin
        $monitor("A=%0b|B=%0b|Borrow=%0b|Diff=%0b", a,b,B,D);
        for(i=0;i<4;i=i+1) begin
            {a,b} = i;
            #10;
        end
    end
endmodule
