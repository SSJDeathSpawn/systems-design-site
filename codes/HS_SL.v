module HS_SL(B,D,a,b);
	input a, b;
	output B, D;

	wire a_not;
	xor xor1(D,a,b);
	not not1(a_not,a);
	and and1(B,a_not,b);
endmodule

module HS_SL_tb;
    reg a,b;
    wire B,D;
    integer i;

    HS_SL inst(B,D,a,b);
    
    initial begin
        $monitor("A=%0b|B=%0b|Borrow=%0b|Diff=%0b", a,b,B,D);
        for(i=0;i<4;i=i+1) begin
            {a,b} = i;
            #10;
        end
    end
endmodule
